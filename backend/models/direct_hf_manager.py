import requests
import logging
import os
from typing import Dict, Optional, Any
import random

logger = logging.getLogger(__name__)

class DirectHFManager:
    """
    OpenRouter API Manager for Mixtral-8x7B-Instruct
    
    Uses OpenRouter API to access Mixtral models with proper authentication
    and error handling.
    """
    
    def __init__(self, config=None):
        """Initialize OpenRouter API manager"""
        self.config = config
        
        # Get API token from environment variable or config
        self.api_token = self._get_api_token()
        
        # OpenRouter API Configuration
        self.model_name = "mistralai/mixtral-8x7b-instruct"
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Set headers for OpenRouter
        if self.api_token:
            self.headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-username/ai-agent-council",
                "X-Title": "AI Agent Council"
            }
            logger.info(f"✅ Using OpenRouter API with Mixtral-8x7B-Instruct")
        else:
            self.headers = {"Content-Type": "application/json"}
            logger.warning("⚠️  No OpenRouter API key found - using fallback mode")
        
        # Generation parameters with improved defaults
        self.max_new_tokens = getattr(config, 'hf_max_tokens', 300) if config else 300
        self.temperature = getattr(config, 'hf_temperature', 0.7) if config else 0.7
        self.timeout = getattr(config, 'hf_timeout', 30) if config else 30
        
        logger.info(f"Initializing OpenRouter API Manager")
        logger.info(f"  Model: {self.model_name}")
        logger.info(f"  Provider: OpenRouter")
        logger.info(f"  Max tokens: {self.max_new_tokens}")
        logger.info(f"  Temperature: {self.temperature}")
        logger.info(f"  Authentication: {'Yes' if self.api_token else 'No (Fallback mode)'}")
        
        # Test API connectivity
        self._test_api_connection()
    
    def _get_api_token(self) -> Optional[str]:
        """Get API token from environment variable or config"""
        # Try OpenRouter environment variable first
        token = os.getenv('OPENROUTER_API_KEY')
        if token:
            logger.info("✅ Using OpenRouter API key from environment variable")
            return token.strip()
            
        # Try legacy HF_TOKEN for backward compatibility
        token = os.getenv('HF_TOKEN')
        if token:
            logger.info("✅ Using API key from HF_TOKEN environment variable")
            return token.strip()
            
        # Try config object
        if self.config:
            token = getattr(self.config, 'openrouter_api_key', None)
            if token:
                logger.info("✅ Using OpenRouter API key from config")
                return token.strip()
            # Fallback to hf_token
            token = getattr(self.config, 'hf_token', None)
            if token:
                logger.info("✅ Using API key from hf_token config")
                return token.strip()
        
        # No token found
        logger.warning("❌ No OpenRouter API key found in environment or config")
        return None
    
    def _test_api_connection(self):
        """Test if the API is accessible"""
        try:
            test_response = self.query({
                "inputs": "Hello",
                "parameters": {
                    "max_new_tokens": 10,
                    "temperature": 0.1
                }
            })
            
            if isinstance(test_response, list) and len(test_response) > 0:
                logger.info("✅ OpenRouter API connection successful!")
                self._api_available = True
            elif isinstance(test_response, dict):
                if test_response.get('error') == 'credits_exceeded':
                    logger.warning("⚠️  API credits exceeded - using fallback responses")
                    self._api_available = False
                elif test_response.get('error') == 'invalid_token':
                    logger.error("❌ Invalid OpenRouter API key - check your OPENROUTER_API_KEY")
                    self._api_available = False
                elif 'loading' in str(test_response).lower():
                    logger.info("🔄 Model is loading - will be available soon")
                    self._api_available = True
                else:
                    logger.warning(f"⚠️  API test returned: {test_response}")
                    self._api_available = False
            else:
                logger.warning(f"⚠️  API test returned unexpected format: {test_response}")
                self._api_available = False
                
        except Exception as e:
            logger.error(f"❌ API connection test failed: {e}")
            self._api_available = False
    
    def query(self, payload):
        """OpenRouter API query method with proper format conversion"""
        try:
            # Convert HuggingFace format to OpenRouter format
            openrouter_payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": payload.get("inputs", "")}],
                "max_tokens": payload.get("parameters", {}).get("max_new_tokens", self.max_new_tokens),
                "temperature": payload.get("parameters", {}).get("temperature", self.temperature),
                "top_p": payload.get("parameters", {}).get("top_p", 0.9),
                "frequency_penalty": payload.get("parameters", {}).get("repetition_penalty", 1.1) - 1.0
            }
            
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=openrouter_payload, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                # Convert OpenRouter response back to HuggingFace format
                if "choices" in data and len(data["choices"]) > 0:
                    generated_text = payload.get("inputs", "") + data["choices"][0]["message"]["content"]
                    return [{"generated_text": generated_text}]
                else:
                    return {"error": "invalid_response", "message": "No choices in response"}
            elif response.status_code == 401:
                logger.error("❌ Unauthorized: Invalid or missing OpenRouter API key")
                return {"error": "invalid_token", "message": "Invalid or missing OpenRouter API key"}
            elif response.status_code == 402:
                logger.warning("⚠️  OpenRouter API credits exceeded")
                return {"error": "credits_exceeded", "message": "API credits exceeded"}
            elif response.status_code == 403:
                logger.error("❌ Forbidden: Access denied to this model")
                return {"error": "access_denied", "message": "Access denied to model"}
            elif response.status_code == 429:
                logger.warning("⚠️  Rate limit exceeded - too many requests")
                return {"error": "rate_limit", "message": "Rate limit exceeded"}
            elif response.status_code == 503:
                logger.info("🔄 Model is loading - please try again in a moment")
                return {"error": "model_loading", "message": "Model is loading"}
            else:
                logger.error(f"❌ API request failed with status {response.status_code}: {response.text}")
                return {"error": f"HTTP {response.status_code}", "message": response.text}
                
        except requests.exceptions.Timeout:
            logger.error("❌ API request timed out")
            return {"error": "timeout", "message": "Request timeout"}
        except requests.exceptions.ConnectionError:
            logger.error("❌ Connection error - check internet connection")
            return {"error": "connection_error", "message": "Connection failed"}
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request failed: {e}")
            return {"error": "request_failed", "message": str(e)}
        except Exception as e:
            logger.error(f"❌ Unexpected error in API query: {e}")
            return {"error": "unexpected_error", "message": str(e)}
    
    def is_available(self) -> bool:
        """Check if the API is available"""
        return getattr(self, '_api_available', False)
    
    def generate_response(self, prompt: str, **kwargs) -> Optional[str]:
        """
        Generate response using OpenRouter API with enhanced error handling
        
        Args:
            prompt: Input text prompt
            **kwargs: Additional parameters (max_tokens, temperature, etc.)
        
        Returns:
            Generated response text
        """
        try:
            # Extract parameters
            max_tokens = kwargs.get('max_tokens', self.max_new_tokens)
            temperature = kwargs.get('temperature', self.temperature)
            
            # Ensure reasonable limits
            max_tokens = min(max_tokens, 1000)  # Cap at 1000 tokens
            temperature = max(0.1, min(temperature, 1.0))  # Keep between 0.1 and 1.0
            
            logger.debug(f"Generating response for: {prompt[:50]}...")
            
            output = self.query({
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "do_sample": True,
                    "top_p": 0.9,
                    "repetition_penalty": 1.1
                }
            })
            
            # Process response
            if isinstance(output, list) and len(output) > 0:
                if 'generated_text' in output[0]:
                    generated_text = output[0]['generated_text']
                    
                    # Extract only the new generated part (after the original prompt)
                    if generated_text.startswith(prompt):
                        response = generated_text[len(prompt):].strip()
                    else:
                        response = generated_text.strip()
                    
                    if response and len(response.strip()) > 0:
                        logger.debug(f"✅ Generated response: {len(response)} characters")
                        return response
                    else:
                        logger.warning("⚠️  Empty response generated")
                        return self._generate_intelligent_fallback(prompt)
                else:
                    logger.warning(f"⚠️  No 'generated_text' in response: {output[0]}")
                    return self._generate_intelligent_fallback(prompt)
            
            elif isinstance(output, dict) and 'error' in output:
                error_type = output['error']
                if error_type == 'credits_exceeded':
                    logger.info("💡 Using intelligent fallback due to API credits limit")
                elif error_type == 'invalid_token':
                    logger.error("❌ Invalid token - please check your OpenRouter API key")
                elif error_type == 'model_loading':
                    logger.info("🔄 Model loading - using fallback response")
                else:
                    logger.error(f"❌ API returned error: {output['error']}")
                return self._generate_intelligent_fallback(prompt)
            
            else:
                logger.warning(f"⚠️  Unexpected response format: {output}")
                return self._generate_intelligent_fallback(prompt)
                
        except Exception as e:
            logger.error(f"❌ Error in generate_response: {e}")
            return self._generate_intelligent_fallback(prompt)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "model_type": "openrouter",
            "model_name": self.model_name,
            "api_url": self.api_url,
            "available": self.is_available(),
            "authenticated": bool(self.api_token),
            "max_tokens": self.max_new_tokens,
            "temperature": self.temperature,
            "timeout": self.timeout,
            "parameters": "8x7B (Mixture of Experts)",
            "provider": "OpenRouter",
            "method": "OpenAI-compatible API",
            "token_status": "Valid" if self.api_token else "Not provided (fallback mode)"
        }
    
    def _generate_intelligent_fallback(self, prompt: str) -> str:
        """Generate intelligent fallback when API is not available"""
        prompt_lower = prompt.lower()
        
        # Arabic language support
        if any(word in prompt_lower for word in ['code', 'program', 'function', 'python', 'javascript', 'programming', 'kod', 'programmering', 'funktion']):
            responses = [
                "För att lösa denna programmeringsutmaning rekommenderar jag att dela upp den i mindre komponenter. Börja med att identifiera grundkraven och implementera sedan varje del systematiskt. Vilket specifikt programmeringsspråk eller ramverk arbetar du med?",
                "Kodutveckling kräver noggrann planering och testning. Överväg att skriva enhetstester, använda tydliga variabelnamn och följa bästa praxis för ditt valda språk. Vilken särskild aspekt av implementeringen behöver uppmärksamhet?",
                "Programmeringslösningar drar ofta nytta av iterativ utveckling. Börja med en grundläggande fungerande version, optimera sedan och lägg till funktioner. Vad är huvudfunktionaliteten du försöker uppnå?"
            ]
        
        elif any(word in prompt_lower for word in ['explain', 'what is', 'how does', 'why', 'förklara', 'vad är', 'hur fungerar', 'varför']):
            responses = [
                "Detta är en utmärkt fråga som förtjänar en omfattande förklaring. Ämnet involverar flera sammankopplade koncept som bygger på varandra. Låt mig dela upp detta i nyckelkomponenter för att hjälpa till att klargöra relationerna mellan olika aspekter.",
                "För att ge en grundlig förklaring skulle jag behöva överväga flera perspektiv och faktorer. Detta ämne har både teoretiska grunder och praktiska tillämpningar som är värda att utforska. Vilken specifik aspekt skulle du vilja att jag fokuserar på först?",
                "Att förstå detta koncept kräver att man undersöker det från olika vinklar. Det finns grundläggande principer i arbete här, tillsammans med olika verkliga tillämpningar och konsekvenser. Skulle du vilja att jag börjar med grundprinciperna eller hoppar in på specifika exempel?"
            ]
        
        elif any(word in prompt_lower for word in ['help', 'problem', 'issue', 'stuck', 'error', 'hjälp', 'problem', 'fel', 'fastnat']):
            responses = [
                "Jag förstår att du står inför en utmaning, och jag är här för att hjälpa dig att arbeta igenom den. Ofta kan det att dela upp komplexa problem i mindre, hanterbara delar göra dem mycket lättare att lösa. Vad är det specifika området där du upplever svårigheter?",
                "Problemlösning är ofta mest effektivt när vi närmar oss det systematiskt. Låt oss identifiera kärnproblemet och sedan utforska potentiella lösningar steg för steg. Kan du beskriva vad du redan har provat och var du fastnade?",
                "Varje utmaning är en möjlighet att lära sig och växa. Jag skulle gärna hjälpa dig att arbeta igenom detta metodiskt. Vad skulle vara mest hjälpsamt - ska vi börja med att klargöra kraven, eller skulle du föredra att dyka in i potentiella lösningar?"
            ]
        
        else:
            responses = [
                "Tack för din fråga. Detta är definitivt värt att utforska i detalj. Det finns flera viktiga aspekter att överväga, och jag skulle vilja försäkra mig om att jag tar upp det som är mest relevant för din specifika situation. Kan du ge lite mer sammanhang om vad du letar efter?",
                "Det är en genomtänkt förfrågan som berör några viktiga koncept. För att ge dig det mest hjälpsamma svaret skulle jag ha nytta av att förstå din bakgrund och vad du hoppas att uppnå. Vad är det bredare sammanhanget för denna fråga?",
                "Jag uppskattar att du tar upp detta. Det finns flera sätt att närma sig detta ämne, var och en med sina egna fördelar. För att skräddarsy mitt svar så att det blir mest användbart för dig, kan du berätta mer om dina specifika intressen eller mål relaterade till detta ämne?"
            ]
        
        return random.choice(responses)
    
    # Test methods for development and debugging
        
    def test_api_directly(self):
        """Test direct API call"""
        return self.query({
            "inputs": "What is the capital of France?",
            "parameters": {
                "max_new_tokens": 50,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            }
        })
    
    def set_token(self, token: str):
        """Set API token manually"""
        self.api_token = token.strip() if token else None
        
        # Update headers
        if self.api_token:
            self.headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-username/ai-agent-council",
                "X-Title": "AI Agent Council"
            }
            logger.info("✅ API token updated successfully")
        else:
            self.headers = {"Content-Type": "application/json"}
            logger.warning("⚠️  API token removed - using fallback mode")
        
        # Re-test connection
        self._test_api_connection() 