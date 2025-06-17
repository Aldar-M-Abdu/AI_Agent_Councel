from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    app_name: str = "AI-Agent Råd API"
    debug: bool = False  # Inaktivera debug för produktion
    allowed_hosts: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*"  # Tillåt alla ursprung för utveckling
    ]
    log_level: str = "INFO"  # Standardloggning
    secret_key: str = "change_this_secret"
    rate_limit_per_minute: int = 60
    
    # Modellval - Välj vilken modell som ska användas 
    model_type: str = "direct_hf"  # Alternativ: "fast_cpu", "llama", "deepseek", "huggingface", "direct_hf"
    
    # Language Settings
    output_language: str = "english"  # Language for generated responses
    language_code: str = "en"  # ISO language code
    
    # Prestandainställningar - Prioritera Direct HF API med reservlösningar
    fast_mode: bool = True  # Aktivera snabbläge för tillförlitlig prestanda
    use_fast_cpu_model: bool = False  # Använd FastCPU-modell (bevisat fungerande)
    use_deepseek_model: bool = False  # Använd DeepSeek-R1-modell för avancerat resonemang
    use_huggingface_inference: bool = False  # Använd Hugging Face Inference API som primär
    use_direct_hf: bool = True  # Använd Direct HF API (användarens mönster)
    enable_model_caching: bool = True
    max_response_time: int = 10  # Ökat för DeepSeek-resonemang
    
    # Lokal modellkonfiguration (för LLAMA vid behov)
    use_local_models_only: bool = True
    llama_model_path: str = "models/llama-2-7b-chat.Q4_K_M.gguf"
    model_max_tokens: int = 256  # Ökat för DeepSeek-resonemang
    model_temperature: float = 0.7
    model_top_p: float = 0.9
    model_threads: int = 2  # Reducerat för att förhindra hängning
    model_gpu_layers: int = 0  # Endast CPU-läge
    model_timeout: int = 30  # Lägg till timeout för LLAMA-laddning
    
    # Hugging Face-modeller (lättviktsalternativ)
    hf_model_name: str = "microsoft/DialoGPT-small"  # Snabb CPU-modell
    
    # Hugging Face Inference API-konfiguration
    hf_inference_model: str = "facebook/blenderbot-400M-distill"  # Modell för Inference API (gratis nivå vänlig)
    hf_max_tokens: int = 256  # Max tokens för HF Inference API
    hf_temperature: float = 0.7  # Temperatur för HF Inference API
    hf_timeout: int = 30  # Timeout för HF API-förfrågningar
    
    # OpenRouter API-konfiguration
    openrouter_api_key: Optional[str] = None  # OpenRouter API-nyckel (read from environment variable OPENROUTER_API_KEY)
    openrouter_model: str = "mistralai/mixtral-8x7b-instruct"  # OpenRouter-modellnamn
    
    # DeepSeek-R1-konfiguration
    deepseek_model_size: str = "auto"  # Alternativ: "auto", "1.5b", "7b", "14b", "32b", "70b"
    deepseek_use_reasoning: bool = True  # Aktivera resonemangsförmågor
    deepseek_max_tokens: int = 256  # Max tokens för DeepSeek-svar
    deepseek_temperature: float = 0.7  # Temperatur för DeepSeek-generering
    deepseek_enable_gpu: bool = True  # Använd GPU om tillgänglig
    deepseek_trust_remote_code: bool = True  # Krävs för DeepSeek-modeller
    
    # Modellbeteendeinställningar
    enable_professional_mode: bool = True
    enable_discussion_mode: bool = True
    enable_reasoning_mode: bool = True  # Aktivera resonemang för DeepSeek
    quality_threshold: float = 0.7
    consensus_threshold: float = 0.8
    max_discussion_rounds: int = 3

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignorera extra fält från miljö

settings = Settings() 