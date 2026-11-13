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

# Global model manager instance (shared across agents for efficiency)
_global_model_manager = None

class BaseAgent(ABC):
    """
    Abstract base class for AI Decision Council agents. Handles model loading, response
    generation, discussion, and consensus helpers. Subclasses implement fallbacks and domain prompts.
    """
    def __init__(self, agent_name: str, system_prompt: str) -> None:
        """
        Initialize the agent with a name and system prompt. Uses free models without API keys.
        """
        global _global_model_manager
        
        self.agent_name: str = agent_name
        self.system_prompt: str = system_prompt
        
        # Initialize global model manager if not already done
        if _global_model_manager is None and MODEL_MANAGER_AVAILABLE:
            config = settings if CONFIG_AVAILABLE else None
            
            # Only DirectHFManager (OpenRouter/Mixtral) is available after cleanup
            _global_model_manager = DirectHFManager(config)
            logger.info("Using DirectHFManager with mistralai/mixtral-8x7b-instruct via OpenRouter API")
            
        self.model_manager = _global_model_manager
        
        if self.model_manager and self.model_manager.is_available():
            model_info = self.model_manager.get_model_info()
            logger.info(f"{self.agent_name} initialized with {model_info.get('model_type', 'unknown')} model (no API key required)")
        else:
            logger.info(f"{self.agent_name} using intelligent fallback response system.")

    def generate_response(self, user_text: str) -> str:
        """
        Generate a response based on user text. Uses the model manager if available,
        otherwise falls back to the intelligent fallback response system.
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
            logger.error(f"Error generating response for {self.agent_name}: {e}")
            return self._generate_fallback_response(user_text)

    def _enhance_response_quality(self, response: str) -> str:
        """
        Improve response quality by adding discussion elements and a professional tone.
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
        Generate an intelligent fallback response when models are unavailable.
        Uses sophisticated templates based on text analysis.
        """
        user_lower = user_text.lower()
        
        # Advanced categorization for professional responses
        # Swedish keywords kept as aliases so Swedish user input still categorizes
        if any(word in user_lower for word in ['strategy', 'strategic', 'plan', 'planning', 'strategi', 'strategisk', 'planering']):
            responses = [
                "Strategic planning requires thorough analysis of market conditions, competitive landscape, and internal resources. I recommend starting with a SWOT analysis to identify strengths, weaknesses, opportunities, and threats. What strategic goals are you prioritizing highest right now?",
                "For successful strategic development, you should consider both short-term tactical actions and long-term strategic initiatives. Market positioning and value proposition are central elements. How does your current competitive situation look?",
                "Strategic success builds on clear vision, well-defined goals, and systematic execution. I suggest a phased approach with regular evaluation points. What resources do you have available for strategic implementation?"
            ]
        elif any(word in user_lower for word in ['risk', 'risks', 'threat', 'danger', 'risker', 'hot', 'fara']):
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
        """Return the agent's unique perspective or approach"""
        pass

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        if self.model_manager:
            return self.model_manager.get_model_info()
        return {"model_type": "fallback", "requires_api_key": False}

    def clear_cache(self):
        """Clear the model's cache if available"""
        if self.model_manager and hasattr(self.model_manager, 'clear_cache'):
            self.model_manager.clear_cache()
            logger.info(f"Cache cleared for {self.agent_name}")

    def is_model_available(self) -> bool:
        """Check if the model is available"""
        return self.model_manager is not None and self.model_manager.is_available()

    def discuss_with_peers(self, user_text: str, other_agent_opinions: List[Dict[str, str]]) -> str:
        """
        Generate a discussion response based on other agents' opinions - optimized for speed.
        Args:
            user_text (str): The original user question.
            other_agent_opinions (List[Dict[str, str]]): List of other agents' responses.
        Returns:
            str: The agent's discussion response.
        """
        discussion_context = f"Original question: {user_text}\n\n"
        discussion_context += "Other agents' opinions:\n"
        for opinion in other_agent_opinions:
            if opinion['agent_name'] != self.agent_name:
                discussion_context += f"- {opinion['agent_name']}: {opinion['text_response'][:100]}...\n"
        
        discussion_prompt = f"""
        Based on the other agents' opinions, share your thoughts on their perspectives.
        Do you agree or disagree with any of them? What aspects do you think they missed?
        Keep your response focused and constructive (max 100 words).
        """
        
        if self.model_manager and self.model_manager.is_available():
            # Use free AI model with fast parameters
            prompt = f"{self.system_prompt}\n\n{discussion_prompt}\n\n{discussion_context}\n\nYour discussion response:"
            response = self.model_manager.generate_response(prompt, max_tokens=100, temperature=0.7)
            return response
        else:
            # Use intelligent fallback for discussion
            return self._generate_discussion_fallback(user_text, other_agent_opinions)

    def contribute_to_consensus(self, user_text: str, discussion_history: List[Dict[str, str]]) -> str:
        """
        Contribute to building consensus based on discussion history - optimized for speed.
        Args:
            user_text (str): The original user question.
            discussion_history (List[Dict[str, str]]): List of discussion contributions from agents.
        Returns:
            str: The agent's consensus contribution.
        """
        consensus_prompt = f"""
        Based on all discussions, help formulate a single, unified recommendation.
        Focus on finding common ground and the most practical solution.
        Your contribution should be concise and action-oriented (max 80 words).
        """
        
        discussion_summary = f"Original question: {user_text}\n\nDiscussion points:\n"
        for discussion in discussion_history:
            discussion_summary += f"- {discussion['agent_name']}: {discussion['discussion'][:80]}...\n"
        
        if self.model_manager and self.model_manager.is_available():
            prompt = f"{self.system_prompt}\n\n{consensus_prompt}\n\n{discussion_summary}\n\nYour consensus contribution:"
            response = self.model_manager.generate_response(prompt, max_tokens=80, temperature=0.6)
            return response
        else:
            return self._generate_consensus_fallback(user_text, discussion_history)

    @abstractmethod
    def _generate_discussion_fallback(self, user_text: str, other_opinions: List[Dict[str, str]]) -> str:
        """
        Generate a discussion response with fallback logic.
        Args:
            user_text (str): The original user question.
            other_opinions (List[Dict[str, str]]): List of other agents' responses.
        Returns:
            str: The agent's fallback discussion response.
        """
        pass

    @abstractmethod
    def _generate_consensus_fallback(self, user_text: str, discussion_history: List[Dict[str, str]]) -> str:
        """
        Generate a consensus contribution with fallback logic.
        Args:
            user_text (str): The original user question.
            discussion_history (List[Dict[str, str]]): List of discussion contributions from agents.
        Returns:
            str: The agent's fallback consensus contribution.
        """
        pass

    def _get_llm_response(self, user_text: str, specific_guidance: str) -> str:
        """
        Generate a response with free AI models or intelligent fallback - optimized for speed.
        Args:
            user_text (str): The user's input question or statement.
            specific_guidance (str): Additional prompt guidance for the LLM.
        Returns:
            str: The generated response.
        """
        if self.model_manager and self.model_manager.is_available():
            # Use free AI model with optimized parameters for speed
            prompt = f"{self.system_prompt}\n\n{specific_guidance}\n\nUser: {user_text}\n\nAssistant:"
            response = self.model_manager.generate_response(
                prompt, 
                max_tokens=128,  # Reduced for speed
                temperature=0.7
            )
            return response
        else:
            # Use intelligent fallback based on content analysis
            return self._generate_intelligent_fallback(user_text, specific_guidance)

    def _generate_intelligent_fallback(self, user_text: str, specific_guidance: str) -> str:
        """
        Generate intelligent responses based on keyword and context analysis.
        Args:
            user_text (str): The user's input question or statement.
            specific_guidance (str): Additional prompt guidance for the fallback.
        Returns:
            str: The generated fallback response.
        """
        user_text_lower = user_text.lower()
        
        # Determine question type and delegate to subclass methods
        # Swedish keywords kept as aliases so Swedish user input still categorizes
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

    # Abstract methods that subclasses must implement for fallback responses
    @abstractmethod
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for finance-related questions.
        """
        pass

    @abstractmethod
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for career-related questions.
        """
        pass

    @abstractmethod
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for relationship-related questions.
        """
        pass

    @abstractmethod
    def _generate_health_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for health-related questions.
        """
        pass

    @abstractmethod
    def _generate_education_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for education-related questions.
        """
        pass

    @abstractmethod
    def _generate_travel_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for travel-related questions.
        """
        pass

    @abstractmethod
    def _generate_technology_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for technology-related questions.
        """
        pass

    @abstractmethod
    def _generate_general_fallback(self, user_text: str, guidance: str) -> str:
        """
        Generate a fallback response for general questions.
        """
        pass
