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
    
    def __init__(self, config: Optional[Any] = None) -> None:
        """Initialize OpenRouter API manager"""
        self.config = config
        
        # Get API token from environment variable or config
        self.api_token = self._get_api_token()
        
        # OpenRouter API Configuration (model from settings/env when provided)
        self.model_name = getattr(config, "openrouter_model", None) or "mistralai/mixtral-8x7b-instruct"
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Set headers for OpenRouter
        if self.api_token:
            self.headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/Aldar-M-Abdu/AI_Agent_Councel",
                "X-Title": "AI Decision Council"
            }
            logger.info("Using OpenRouter API with model %s", self.model_name)
        else:
            self.headers = {"Content-Type": "application/json"}
            logger.warning("No OpenRouter API key found - using fallback mode")
        
        # Generation parameters with improved defaults
        self.max_new_tokens = getattr(config, 'hf_max_tokens', 300) if config else 300
        self.temperature = getattr(config, 'hf_temperature', 0.7) if config else 0.7
        self.timeout = getattr(config, 'hf_timeout', 30) if config else 30
        
        logger.info(
            "Initializing OpenRouter API Manager (model=%s, max_tokens=%s, temperature=%s)",
            self.model_name,
            self.max_new_tokens,
            self.temperature,
        )
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
        
        # Swedish keywords kept as aliases so Swedish user input still categorizes
        if any(word in prompt_lower for word in ['code', 'program', 'function', 'python', 'javascript', 'programming', 'kod', 'programmering', 'funktion']):
            responses = [
                "To solve this programming challenge, I recommend breaking it into smaller components. Start by identifying the core requirements, then implement each part systematically. Which specific programming language or framework are you working with?",
                "Code development requires careful planning and testing. Consider writing unit tests, using clear variable names, and following best practices for your chosen language. Which particular aspect of the implementation needs attention?",
                "Programming solutions often benefit from iterative development. Start with a basic working version, then optimize and add features. What is the main functionality you are trying to achieve?"
            ]
        
        elif any(word in prompt_lower for word in ['explain', 'what is', 'how does', 'why', 'förklara', 'vad är', 'hur fungerar', 'varför']):
            responses = [
                "This is an excellent question that deserves a comprehensive explanation. The topic involves several interconnected concepts that build on each other. Let me break this down into key components to help clarify the relationships between different aspects.",
                "To provide a thorough explanation, I would need to consider several perspectives and factors. This topic has both theoretical foundations and practical applications worth exploring. Which specific aspect would you like me to focus on first?",
                "Understanding this concept requires examining it from different angles. There are fundamental principles at work here, along with various real-world applications and implications. Would you like me to start with the core principles or jump into specific examples?"
            ]
        
        elif any(word in prompt_lower for word in ['help', 'problem', 'issue', 'stuck', 'error', 'hjälp', 'fel', 'fastnat']):
            responses = [
                "I understand you are facing a challenge, and I am here to help you work through it. Often, breaking complex problems into smaller, manageable parts makes them much easier to solve. What is the specific area where you are experiencing difficulties?",
                "Problem-solving is often most effective when we approach it systematically. Let us identify the core problem and then explore potential solutions step by step. Can you describe what you have already tried and where you got stuck?",
                "Every challenge is an opportunity to learn and grow. I would be glad to help you work through this methodically. What would be most helpful — should we start by clarifying the requirements, or would you prefer to dive into potential solutions?"
            ]
        
        else:
            responses = [
                "Thank you for your question. This is definitely worth exploring in detail. There are several important aspects to consider, and I want to make sure I address what is most relevant to your specific situation. Can you give a bit more context about what you are looking for?",
                "That is a thoughtful request that touches on some important concepts. To give you the most helpful answer, I would benefit from understanding your background and what you hope to achieve. What is the broader context for this question?",
                "I appreciate you raising this. There are several ways to approach this topic, each with its own advantages. To tailor my response so it is most useful for you, can you tell me more about your specific interests or goals related to this topic?"
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
                "HTTP-Referer": "https://github.com/Aldar-M-Abdu/AI_Agent_Councel",
                "X-Title": "AI Decision Council"
            }
            logger.info("✅ API token updated successfully")
        else:
            self.headers = {"Content-Type": "application/json"}
            logger.warning("⚠️  API token removed - using fallback mode")
        
        # Re-test connection
        self._test_api_connection() 