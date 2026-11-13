from typing import List, Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env only."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "AI Decision Council API"
    debug: bool = False
    allowed_hosts: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*",  # Allow all origins for local development
    ]
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    secret_key: str = Field(default="", validation_alias="SECRET_KEY")
    rate_limit_per_minute: int = 60

    # Model selection
    model_type: str = "direct_hf"  # Options: "fast_cpu", "llama", "deepseek", "huggingface", "direct_hf"

    # Language settings
    output_language: str = "english"
    language_code: str = "en"

    # Performance settings
    fast_mode: bool = True
    use_fast_cpu_model: bool = False
    use_deepseek_model: bool = False
    use_huggingface_inference: bool = False
    use_direct_hf: bool = True
    enable_model_caching: bool = True
    max_response_time: int = 10

    # Local model configuration (optional / unused in OpenRouter path)
    use_local_models_only: bool = True
    llama_model_path: str = "models/llama-2-7b-chat.Q4_K_M.gguf"
    model_max_tokens: int = 256
    model_temperature: float = 0.7
    model_top_p: float = 0.9
    model_threads: int = 2
    model_gpu_layers: int = 0
    model_timeout: int = 30

    # Hugging Face models (legacy options)
    hf_model_name: str = "microsoft/DialoGPT-small"
    hf_inference_model: str = "facebook/blenderbot-400M-distill"
    hf_max_tokens: int = 256
    hf_temperature: float = 0.7
    hf_timeout: int = 30

    # OpenRouter API configuration (key must come from env — never hardcode)
    openrouter_api_key: Optional[str] = Field(default=None, validation_alias="OPENROUTER_API_KEY")
    openrouter_model: str = "mistralai/mixtral-8x7b-instruct"

    # Accept .env.example names DEFAULT_MODEL / MAX_TOKENS without breaking existing fields
    default_model: Optional[str] = Field(default=None, validation_alias="DEFAULT_MODEL")
    max_tokens: Optional[int] = Field(default=None, validation_alias="MAX_TOKENS")

    # DeepSeek configuration (legacy options)
    deepseek_model_size: str = "auto"
    deepseek_use_reasoning: bool = True
    deepseek_max_tokens: int = 256
    deepseek_temperature: float = 0.7
    deepseek_enable_gpu: bool = True
    deepseek_trust_remote_code: bool = True

    # Behaviour settings
    enable_professional_mode: bool = True
    enable_discussion_mode: bool = True
    enable_reasoning_mode: bool = True
    quality_threshold: float = 0.7
    consensus_threshold: float = 0.8
    max_discussion_rounds: int = 3

    @model_validator(mode="after")
    def apply_env_aliases(self) -> "Settings":
        if self.default_model:
            self.openrouter_model = self.default_model
        if self.max_tokens is not None:
            self.hf_max_tokens = self.max_tokens
            self.model_max_tokens = self.max_tokens
        return self

settings = Settings()
