from abc import ABC, abstractmethod
import random
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Prefer package imports; fall back to backend-on-sys.path style
try:
    from backend.config import settings
    CONFIG_AVAILABLE = True
except ImportError:
    try:
        from config import settings
        CONFIG_AVAILABLE = True
    except ImportError:
        CONFIG_AVAILABLE = False
        logger.warning("Config not available; using environment variables directly")

try:
    from backend.models.direct_hf_manager import DirectHFManager
    MODEL_MANAGER_AVAILABLE = True
    logger.info("DirectHFManager (OpenRouter) loaded successfully")
except ImportError as e:
    try:
        from models.direct_hf_manager import DirectHFManager
        MODEL_MANAGER_AVAILABLE = True
        logger.info("DirectHFManager (OpenRouter) loaded successfully")
    except ImportError as e2:
        MODEL_MANAGER_AVAILABLE = False
        DirectHFManager = None  # type: ignore
        logger.warning("Model manager unavailable: %s. Using fallback responses.", e2)

# Global modellhanterareinstans (delad mellan alla agenter för effektivitet)
_global_model_manager = None

class BaseAgent(ABC):
    """
    Abstract base class for AI Decision Council agents. Handles model loading, response
    generation, discussion, and consensus helpers. Subclasses implement fallbacks and domain prompts.
    """
    def __init__(self, agent_name: str, system_prompt: str) -> None:
        """
        Initiera agenten med ett namn och systemprompt. Använder gratis modeller utan API-nycklar.
        """
        global _global_model_manager
        
        self.agent_name: str = agent_name
        self.system_prompt: str = system_prompt
        
        # Initiera global modellhanterare om inte redan gjort
        if _global_model_manager is None and MODEL_MANAGER_AVAILABLE:
            config = settings if CONFIG_AVAILABLE else None
            
            # Only DirectHFManager (OpenRouter/Mixtral) is available after cleanup
            _global_model_manager = DirectHFManager(config)
            logger.info("Using DirectHFManager with mistralai/mixtral-8x7b-instruct via OpenRouter API")
            
        self.model_manager = _global_model_manager
        
        if self.model_manager and self.model_manager.is_available():
            model_info = self.model_manager.get_model_info()
            logger.info(f"{self.agent_name} initierad med {model_info.get('model_type', 'unknown')} modell (ingen API-nyckel krävs)")
        else:
            logger.info(f"{self.agent_name} använder intelligent reservsvarssystem.")

    def generate_response(self, user_text: str) -> str:
        """
        Generera svar baserat på användartext. Använder modellhanterare om tillgänglig,
        annars faller tillbaka på intelligent reservsvarssystem.
        """
        try:
            if self.model_manager and self.model_manager.is_available():
                # Create context-aware prompt
                full_prompt = f"{self.system_prompt}\n\nUser: {user_text}\n\nAssistant:"
                
                # Use DeepSeek-specific parameters if available
                if hasattr(self.model_manager, 'generate_response'):
                    # Add English language instruction to the prompt
                    english_prompt = f"Respond in English. {full_prompt}"
                    
                    if 'deepseek' in str(type(self.model_manager)).lower():
                        # DeepSeek-specific generation with reasoning
                        config = settings if CONFIG_AVAILABLE else None
                        use_reasoning = getattr(config, 'enable_reasoning_mode', True) if config else True
                        max_tokens = getattr(config, 'deepseek_max_tokens', 256) if config else 256
                        temperature = getattr(config, 'deepseek_temperature', 0.7) if config else 0.7
                        
                        response = self.model_manager.generate_response(
                            english_prompt, 
                            max_tokens=max_tokens,
                            temperature=temperature,
                            use_reasoning=use_reasoning
                        )
                    else:
                        # Standard generation for other models
                        response = self.model_manager.generate_response(english_prompt)
                else:
                    response = self._generate_fallback_response(user_text)
                
                # Validate and clean response
                if response and len(response.strip()) > 10:
                    return self._enhance_response_quality(response.strip())
                else:
                    # If using HF manager, it should have its own fallback
                    if hasattr(self.model_manager, '_generate_intelligent_fallback'):
                        return self.model_manager._generate_intelligent_fallback(user_text)
                    else:
                        return self._generate_fallback_response(user_text)
            else:
                return self._generate_fallback_response(user_text)
                
        except Exception as e:
            logger.error(f"Fel vid svarsgenerering för {self.agent_name}: {e}")
            return self._generate_fallback_response(user_text)

    def _enhance_response_quality(self, response: str) -> str:
        """
        Förbättra svarskvaliteten genom att lägga till diskussionselement och professionell ton.
        """
        # Remove any system artifacts
        response = response.replace("Assistant:", "").replace("User:", "").strip()
        
        # Ensure the response ends with a discussion element if it doesn't already have one
        discussion_indicators = ['?', 'What do you think', 'How do you', 'Let\'s discuss', 'I\'m curious']
        has_discussion = any(indicator in response for indicator in discussion_indicators)
        
        if not has_discussion and len(response) > 50:
            # Add a contextual discussion question
            user_context = self._extract_context_keywords(response)
            discussion_question = self._generate_contextual_question(user_context)
            response = f"{response} {discussion_question}"
        
        return response

    def _extract_context_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for contextual understanding"""
        business_keywords = [
            'strategy', 'market', 'competition', 'growth', 'revenue', 'profit',
            'risk', 'opportunity', 'investment', 'decision', 'planning', 'execution',
            'team', 'leadership', 'management', 'innovation', 'technology', 'digital'
        ]
        
        text_lower = text.lower()
        found_keywords = [keyword for keyword in business_keywords if keyword in text_lower]
        return found_keywords[:3]  # Return top 3 relevant keywords

    def _generate_contextual_question(self, keywords: List[str]) -> str:
        """Generate contextual discussion question based on keywords"""
        if not keywords:
            return "What is your perspective on this situation?"
        
        question_templates = {
            'strategy': "How does this fit into your strategic goals?",
            'market': "What market dynamics are you considering?",
            'risk': "What risk factors concern you most?",
            'team': "How is your team positioned to handle this?",
            'decision': "What factors are most important in your decision process?",
            'growth': "What growth opportunities do you see here?",
            'technology': "How might technology impact this situation?",
            'leadership': "What leadership approach would work best here?"
        }
        
        # Select question based on first relevant keyword
        primary_keyword = keywords[0]
        return question_templates.get(primary_keyword, "What aspects would you like to explore further?")

    def _generate_fallback_response(self, user_text: str) -> str:
        """
        Generera intelligent reservsvar när modeller inte är tillgängliga.
        Använder sofistikerade mallar baserade på textanalys.
        """
        user_lower = user_text.lower()
        
        # Advanced categorization for professional responses
        if any(word in user_lower for word in ['strategy', 'strategic', 'plan', 'planning', 'strategi', 'strategisk', 'planering']):
            responses = [
                "Strategic planning requires thorough analysis of market conditions, competitive landscape, and internal resources. I recommend starting with a SWOT analysis to identify strengths, weaknesses, opportunities, and threats. What strategic goals are you prioritizing highest right now?",
                "For successful strategic development, you should consider both short-term tactical actions and long-term strategic initiatives. Market positioning and value proposition are central elements. How does your current competitive situation look?",
                "Strategic success builds on clear vision, well-defined goals, and systematic execution. I suggest a phased approach with regular evaluation points. What resources do you have available for strategic implementation?"
            ]
        elif any(word in user_lower for word in ['risk', 'risks', 'threat', 'danger', 'risk', 'risker', 'hot', 'fara']):
            responses = [
                "Risk management requires systematic identification, evaluation, and mitigation of potential threats. I recommend developing a risk matrix that categorizes risks by probability and impact. What risks concern you most at the moment?",
                "Effective risk analysis includes both quantitative and qualitative assessments. Scenario planning and stress testing are valuable tools for understanding potential consequences. How do you work with risk management today?",
                "Risk mitigation is about balancing risk exposure against business opportunities. Diversification, insurance, and contingency plans are important strategies. What risk tolerance does your organization have?"
            ]
        elif any(word in user_lower for word in ['decision', 'decide', 'choice', 'choose', 'beslut', 'besluta', 'val', 'välja']):
            responses = [
                "Quality decisions build on structured analysis of alternatives, criteria, and consequences. I suggest a decision matrix that weighs different factors against your priorities. What criteria are most important for this decision?",
                "The decision process should include stakeholder analysis, risk assessment, and implementation planning. Transparency and documentation facilitate future evaluation. Who needs to be involved in this decision?",
                "Strategic decisions require balance between data-driven analysis and experience-based judgment. Time aspect and reversibility are important factors to consider. What timeframe are you working within?"
            ]
        else:
            responses = [
                "This is an interesting challenge that requires careful analysis of several factors. I recommend a structured approach that considers both short-term and long-term consequences. Can you tell me more about the context?",
                "Based on my experience, it's important to consider all stakeholders' perspectives and potential consequences. A systematic evaluation of alternatives usually gives the best results. What factors are most important to you?",
                "This requires balanced assessment of opportunities and risks. I suggest we break down the problem into smaller parts to get better overview. What do you see as the biggest challenge here?"
            ]
        
        return random.choice(responses)

    @abstractmethod
    def get_agent_perspective(self) -> str:
        """Returnera agentens unika perspektiv eller approach"""
        pass

    def get_model_info(self) -> Dict[str, Any]:
        """Få information om den aktuella modellen"""
        if self.model_manager:
            return self.model_manager.get_model_info()
        return {"model_type": "fallback", "requires_api_key": False}

    def clear_cache(self):
        """Rensa modellens cache om tillgängligt"""
        if self.model_manager and hasattr(self.model_manager, 'clear_cache'):
            self.model_manager.clear_cache()
            logger.info(f"Cache rensad för {self.agent_name}")

    def is_model_available(self) -> bool:
        """Kontrollera om modellen är tillgänglig"""
        return self.model_manager is not None and self.model_manager.is_available()

    def discuss_with_peers(self, user_text: str, other_agent_opinions: List[Dict[str, str]]) -> str:
        """
        Generera ett diskussionssvar baserat på andra agenters åsikter - optimerat för snabbhet.
        Args:
            user_text (str): Den ursprungliga användarfrågan.
            other_agent_opinions (List[Dict[str, str]]): Lista över andra agenters svar.
        Returns:
            str: Agentens diskussionssvar.
        """
        discussion_context = f"Ursprunglig fråga: {user_text}\n\n"
        discussion_context += "Andra agenters åsikter:\n"
        for opinion in other_agent_opinions:
            if opinion['agent_name'] != self.agent_name:
                discussion_context += f"- {opinion['agent_name']}: {opinion['text_response'][:100]}...\n"
        
        discussion_prompt = f"""
        Baserat på andra agenters åsikter, ge dina tankar om deras perspektiv.
        Håller du med eller inte med någon av dem? Vilka aspekter tror du de missade?
        Håll ditt svar fokuserat och konstruktivt (max 100 ord).
        """
        
        if self.model_manager and self.model_manager.is_available():
            # Använd gratis AI-modell med snabba parametrar
            prompt = f"{self.system_prompt}\n\n{discussion_prompt}\n\n{discussion_context}\n\nDitt diskussionssvar:"
            response = self.model_manager.generate_response(prompt, max_tokens=100, temperature=0.7)
            return response
        else:
            # Använd intelligent reserv för diskussion
            return self._generate_discussion_fallback(user_text, other_agent_opinions)

    def contribute_to_consensus(self, user_text: str, discussion_history: List[Dict[str, str]]) -> str:
        """
        Bidra till att bygga konsensus baserat på diskussionshistoriken - optimerat för snabbhet.
        Args:
            user_text (str): Den ursprungliga användarfrågan.
            discussion_history (List[Dict[str, str]]): Lista över diskussionsbidrag från agenter.
        Returns:
            str: Agentens konsensusbidrag.
        """
        consensus_prompt = f"""
        Baserat på alla diskussioner, hjälp till att formulera en enda, enhetlig rekommendation.
        Fokusera på att hitta gemensam grund och den mest praktiska lösningen.
        Ditt bidrag ska vara kortfattat och handlingsinriktat (max 80 ord).
        """
        
        discussion_summary = f"Ursprunglig fråga: {user_text}\n\nDiskussionspunkter:\n"
        for discussion in discussion_history:
            discussion_summary += f"- {discussion['agent_name']}: {discussion['discussion'][:80]}...\n"
        
        if self.model_manager and self.model_manager.is_available():
            prompt = f"{self.system_prompt}\n\n{consensus_prompt}\n\n{discussion_summary}\n\nDitt konsensusbidrag:"
            response = self.model_manager.generate_response(prompt, max_tokens=80, temperature=0.6)
            return response
        else:
            return self._generate_consensus_fallback(user_text, discussion_history)

    @abstractmethod
    def _generate_discussion_fallback(self, user_text: str, other_opinions: List[Dict[str, str]]) -> str:
        """
        Generera diskussionssvar med reservlogik.
        Args:
            user_text (str): Den ursprungliga användarfrågan.
            other_opinions (List[Dict[str, str]]): Lista över andra agenters svar.
        Returns:
            str: Agentens reservdiskussionssvar.
        """
        pass

    @abstractmethod
    def _generate_consensus_fallback(self, user_text: str, discussion_history: List[Dict[str, str]]) -> str:
        """
        Generera konsensusbidrag med reservlogik.
        Args:
            user_text (str): Den ursprungliga användarfrågan.
            discussion_history (List[Dict[str, str]]): Lista över diskussionsbidrag från agenter.
        Returns:
            str: Agentens reservkonsensusbidrag.
        """
        pass

    def _get_llm_response(self, user_text: str, specific_guidance: str) -> str:
        """
        Generera svar med gratis AI-modeller eller intelligent reserv - optimerat för snabbhet.
        Args:
            user_text (str): Användarens inmatade fråga eller påstående.
            specific_guidance (str): Ytterligare promptvägledning för LLM.
        Returns:
            str: Det genererade svaret.
        """
        if self.model_manager and self.model_manager.is_available():
            # Använd gratis AI-modell med optimerade parametrar för snabbhet
            prompt = f"{self.system_prompt}\n\n{specific_guidance}\n\nAnvändare: {user_text}\n\nAssistent:"
            response = self.model_manager.generate_response(
                prompt, 
                max_tokens=128,  # Reduced for speed
                temperature=0.7
            )
            return response
        else:
            # Använd intelligent reserv baserat på innehållsanalys
            return self._generate_intelligent_fallback(user_text, specific_guidance)

    def _generate_intelligent_fallback(self, user_text: str, specific_guidance: str) -> str:
        """
        Generera intelligenta svar baserat på nyckelord och kontextanalys.
        Args:
            user_text (str): Användarens inmatade fråga eller påstående.
            specific_guidance (str): Ytterligare promptvägledning för reserven.
        Returns:
            str: Det genererade reservsvaret.
        """
        user_text_lower = user_text.lower()
        
        # Determine question type and delegate to subclass methods
        if any(word in user_text_lower for word in ['invest', 'money', 'financial', 'crypto', 'stock', 'fund', 'budget', 'loan', 'debt', 'save', 'spend', 'buy', 'sell', 'price', 'investera', 'pengar', 'finansiell', 'krypto', 'aktie', 'fond', 'lån', 'skuld', 'spara', 'spendera', 'köpa', 'sälja', 'pris']):
            return self._generate_financial_fallback(user_text, specific_guidance)
        elif any(word in user_text_lower for word in ['job', 'career', 'work', 'promotion', 'interview', 'resume', 'salary', 'boss', 'colleague', 'quit', 'hire', 'jobb', 'karriär', 'arbete', 'befordran', 'intervju', 'cv', 'lön', 'chef', 'kollega', 'sluta', 'anställa']):
            return self._generate_career_fallback(user_text, specific_guidance)
        elif any(word in user_text_lower for word in ['relationship', 'dating', 'marriage', 'partner', 'love', 'friend', 'family', 'divorce', 'breakup', 'relation', 'dejta', 'äktenskap', 'kärlek', 'vän', 'familj', 'skilsmässa', 'uppbrott']):
            return self._generate_relationship_fallback(user_text, specific_guidance)
        elif any(word in user_text_lower for word in ['health', 'exercise', 'diet', 'medical', 'doctor', 'sick', 'wellness', 'hälsa', 'träning', 'medicinsk', 'doktor', 'sjuk', 'välmående']):
            return self._generate_health_fallback(user_text, specific_guidance)
        elif any(word in user_text_lower for word in ['education', 'school', 'college', 'university', 'study', 'learn', 'course', 'utbildning', 'skola', 'högskola', 'universitet', 'studera', 'lära', 'kurs']):
            return self._generate_education_fallback(user_text, specific_guidance)
        elif any(word in user_text_lower for word in ['travel', 'vacation', 'trip', 'flight', 'hotel', 'resa', 'semester', 'flyg', 'hotell']):
            return self._generate_travel_fallback(user_text, specific_guidance)
        elif any(word in user_text_lower for word in ['technology', 'computer', 'software', 'app', 'tech', 'digital', 'teknologi', 'dator', 'mjukvara', 'teknik']):
            return self._generate_technology_fallback(user_text, specific_guidance)
        else:
            return self._generate_general_fallback(user_text, specific_guidance)

    # Abstrakta metoder som subklasser måste implementera för reservsvar
    @abstractmethod
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för finansrelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för karriärrelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för relationsrelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_health_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för hälsorelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_education_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för utbildningsrelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_travel_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för reserelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_technology_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för teknikrelaterade frågor.
        """
        pass

    @abstractmethod
    def _generate_general_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generera ett reservsvar för allmänna frågor.
        """
        pass 