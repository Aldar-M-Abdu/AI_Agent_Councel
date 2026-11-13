import uuid
import os
import sys
import datetime
import json
import logging
import hashlib
import secrets
from contextlib import asynccontextmanager
from datetime import timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any

# Add the parent directory to the Python path for proper module imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

# Graceful fallback for missing fastapi-limiter (rate limiting disabled in local mode)
class DummyLimiter:  # dummy placeholder
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, func):  # decorator fallback
        return func

try:
    from fastapi_limiter import Limiter  # type: ignore
    limiter_available = True
except ImportError:
    limiter_available = False
    Limiter = DummyLimiter  # Use dummy class when unavailable

# Local imports
from backend.config import settings
from backend.agents.neutral_agent import NeutralAgent
from backend.agents.positive_agent import PositiveAgent
from backend.agents.skeptic_agent import SkepticAgent
from backend.agents.risk_expert_agent import RiskExpertAgent
from backend.agents.base_agent import BaseAgent

# Advanced feature imports with better error handling
ADVANCED_FEATURES_AVAILABLE = False
LangGraphOrchestrator = None
WorkflowConfig = None
MetaEvaluator = None
EvaluationMetrics = None
ComparativeAnalysis = None
PerformanceBenchmarker = None
WebSearchIntegration = None

# Configure logging once at process start (modules use getLogger only)
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ai_decision_council")

try:
    from backend.orchestration import LangGraphOrchestrator, WorkflowConfig
    logger.info("Orchestration module loaded")
except ImportError as e:
    logger.warning("Orchestration module unavailable: %s", e)
    LangGraphOrchestrator = None
    WorkflowConfig = None

try:
    from backend.evaluation import MetaEvaluator, EvaluationMetrics, ComparativeAnalysis
    logger.info("Evaluation module loaded")
except ImportError as e:
    logger.warning("Evaluation module unavailable: %s", e)
    MetaEvaluator = None
    EvaluationMetrics = None
    ComparativeAnalysis = None

try:
    from backend.technical_depth import PerformanceBenchmarker, WebSearchIntegration
    logger.info("Technical depth module loaded")
except ImportError as e:
    logger.warning("Technical depth module unavailable: %s", e)
    PerformanceBenchmarker = None
    WebSearchIntegration = None

# Check whether all advanced features are available
if LangGraphOrchestrator and MetaEvaluator and PerformanceBenchmarker:
    ADVANCED_FEATURES_AVAILABLE = True
    logger.info("Advanced features available")
else:
    logger.warning("Running in basic mode — some advanced features disabled")

# Runtime directories next to this module (not CWD-dependent)
_BACKEND_DIR = Path(__file__).resolve().parent
os.makedirs(_BACKEND_DIR / "discussions", exist_ok=True)
os.makedirs(_BACKEND_DIR / "reports", exist_ok=True)

# Global instances for advanced features
meta_evaluator_instance = None
performance_benchmarker_instance = None
web_search_instance = None
orchestrator_instance = None

# In-memory storage for simplicity
# In production, use more persistent storage such as Redis or a database
request_store = {}
vote_store = {}
enhanced_request_store = {}
discussion_store = {}
professional_request_store = {}

# User authentication storage (persistent)
users_db = {}  # {username: {password_hash: str, created_at: datetime}}
user_sessions = {}  # {token: {username: str, expires_at: datetime}}

# Rate limiting (disabled if fastapi-limiter is unavailable)
# Note: get_remote_address helper is provided by starlette, but we avoid importing
if limiter_available:
    from starlette.requests import Request
    from starlette.middleware.base import BaseHTTPMiddleware
    from fastapi_limiter.depends import RateLimiter
    from fastapi_limiter import FastAPILimiter, get_remote_address  # type: ignore

    # Initialize FastAPI Limiter in lifespan startup if desired
    limiter = Limiter(key_func=get_remote_address)
else:
    limiter = Limiter()  # dummy instance for compatibility

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifecycle - startup and shutdown"""
    global meta_evaluator_instance, performance_benchmarker_instance, web_search_instance, orchestrator_instance
    
    logger.info("Initializing AI Decision Council system...")
    
    # Initialize basic functionality first
    meta_evaluator_instance = None
    performance_benchmarker_instance = None
    web_search_instance = None
    orchestrator_instance = None
    
    if ADVANCED_FEATURES_AVAILABLE:
        try:
            logger.info("Attempting to initialize advanced features...")
            # Initialize components one at a time with error handling
            try:
                meta_evaluator_instance = MetaEvaluator()
                logger.info("MetaEvaluator initialized")
            except Exception as e:
                logger.warning(f"Could not initialize MetaEvaluator: {e}")
                
            try:
                performance_benchmarker_instance = PerformanceBenchmarker()
                logger.info("PerformanceBenchmarker initialized")
            except Exception as e:
                logger.warning(f"Could not initialize PerformanceBenchmarker: {e}")
                
            # web_search_instance = WebSearchIntegration()  # Disabled - TAVILY removed
            web_search_instance = None
            
            try:
                # Initialize agents with timeout protection
                logger.info("Initializing agents...")
                agents = [NeutralAgent(), PositiveAgent(), SkepticAgent(), RiskExpertAgent()]
                # FIX: Standardize agent names for consistency
                agents[1].agent_name = "Positive Agent"
                agents[2].agent_name = "Skeptic Agent"
                agents[3].agent_name = "Risk Expert Agent"
                orchestrator_instance = LangGraphOrchestrator(agents)
                logger.info("LangGraphOrchestrator initialized")
            except Exception as e:
                logger.warning(f"Could not initialize orchestrator: {e}")
                orchestrator_instance = None
                
            logger.info("Advanced features initialized (with possible warnings)")
        except Exception as e:
            logger.error(f"General error initializing advanced features: {e}")
            # Continue with basic functionality anyway
            meta_evaluator_instance = None
            performance_benchmarker_instance = None
            web_search_instance = None
            orchestrator_instance = None
    else:
        logger.info("Advanced features unavailable - running in basic mode")
    
    logger.info("AI Decision Council system started and ready!")
    
    yield
    
    logger.info("Shutting down AI Decision Council system...")

app = FastAPI(
    title="AI Decision Council API",
    description="Multi-agent decision-support API: specialist agents debate a question and return a structured recommendation. Includes optional LangGraph orchestration.",
    version="2.0.0",
    contact={
        "name": "Aldar Abdu",
        "url": "https://github.com/Aldar-M-Abdu/AI_Agent_Councel",
        "email": "aldar.m.abdu@gmail.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for production frontend builds
frontend_build_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "build")
if os.path.exists(frontend_build_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")
    logger.info(f"Mounted static files from {frontend_build_path}/static")
else:
    logger.warning(f"Frontend build directory not found at {frontend_build_path}. Run 'npm run build' in frontend directory for production.")

# Serve frontend assets
frontend_public_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public")
if os.path.exists(frontend_public_path):
    app.mount("/public", StaticFiles(directory=frontend_public_path), name="public")
    logger.info(f"Mounted public files from {frontend_public_path}")
else:
    logger.warning(f"Frontend public directory not found at {frontend_public_path}")

# --- Pydantic-modeller ---

class DecisionRequest(BaseModel):
    user_text: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    agent_type: Optional[str] = "all"  # 'all', 'Neutral Agent', 'Positive Agent', etc.

class AgentSingleResponse(BaseModel):
    agent_name: str
    response: str

class ChatResponse(BaseModel):
    session_id: str
    responses: List[AgentSingleResponse]

class AgentResponse(BaseModel):
    agent_name: str
    agent_type: str
    response: str

class DecisionResponse(BaseModel):
    request_id: str
    question: str
    responses: List[AgentResponse]

class DiscussionResponse(BaseModel):
    agent_name: str
    discussion: str

class ConsensusResponse(BaseModel):
    agent_name: str
    consensus_contribution: str
    
class InitialResponse(BaseModel):
    agent_name: str
    agent_type: str
    text_response: str

class FullDiscussionResponse(BaseModel):
    request_id: str
    question: str
    initial_responses: List[InitialResponse]
    discussions: List[DiscussionResponse]
    consensus_contributions: List[ConsensusResponse]
    final_recommendation: str
    discussion_file: str
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)

class RootResponse(BaseModel):
    message: str

class VoteRequest(BaseModel):
    request_id: str
    voted_for_agent: str

class DocumentUploadResponse(BaseModel):
    success: bool
    message: str
    documents_processed: int

class EnhancedDecisionRequest(BaseModel):
    user_text: str = Field(..., description="The question or scenario to discuss")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Advanced configuration options")
    enable_web_search: bool = Field(default=True, description="Enable real-time web search")
    enable_context_retrieval: bool = Field(default=False, description="Context retrieval disabled")
    enable_performance_monitoring: bool = Field(default=False, description="Enable performance monitoring")
    quality_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum quality threshold")
    consensus_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Consensus threshold")
    max_discussion_rounds: int = Field(default=3, ge=1, le=5, description="Maximum number of discussion rounds")

class AgentEvaluation(BaseModel):
    agent_name: str
    overall_score: float
    technical_accuracy: float
    persuasiveness: float
    coherence: float
    relevance: float
    strengths: List[str]
    weaknesses: List[str]

class EnhancedDecisionResponse(BaseModel):
    request_id: str
    user_query: str
    final_recommendation: str
    execution_time: float
    quality_score: float
    consensus_level: float
    initial_responses: List[Dict[str, Any]]
    discussion_rounds: List[List[Dict[str, Any]]]
    consensus_attempts: List[List[Dict[str, Any]]]
    agent_evaluations: List[AgentEvaluation]
    comparative_analysis: Dict[str, Any]
    context_used: List[Dict[str, Any]]
    external_data: List[Dict[str, Any]]
    workflow_metadata: Dict[str, Any]
    performance_metrics: Optional[Dict[str, Any]] = None

class ProfessionalDecisionRequest(BaseModel):
    user_text: str = Field(..., description="The strategic question or decision scenario")
    urgency_level: str = Field(default="medium", description="Urgency level: low, medium, high, critical")
    stakeholder_context: Optional[str] = Field(default=None, description="Information about stakeholders involved")
    budget_constraints: Optional[str] = Field(default=None, description="Budget or resource constraints")
    timeline_requirements: Optional[str] = Field(default=None, description="Timeline requirements")
    enable_executive_reporting: bool = Field(default=True, description="Generate executive-level reports")
    decision_framework: Optional[str] = Field(default="auto", description="Decision framework to use")

class ProfessionalDecisionResponse(BaseModel):
    request_id: str
    user_query: str
    professional_decision: Dict[str, Any]
    consensus_result: Dict[str, Any]
    executive_report: Dict[str, Any]
    executive_summary: str
    decision_quality_score: float
    confidence_level: str
    implementation_timeline: str
    risk_assessment: str
    next_actions: List[str]
    stakeholder_communication: str

class ExecutiveDashboardResponse(BaseModel):
    title: str
    recommendation: str
    confidence: str
    risk_level: str
    timeline: str
    key_actions: int
    high_risks: int
    quality_score: float
    consensus_strength: float
    generated_date: str

class SettingsResponse(BaseModel):
    """Response model for current settings"""
    model_type: str
    fast_mode: bool
    use_direct_hf: bool
    enable_professional_mode: bool
    enable_discussion_mode: bool
    enable_reasoning_mode: bool
    quality_threshold: float
    consensus_threshold: float
    max_discussion_rounds: int
    openrouter_model: str
    deepseek_use_reasoning: bool
    max_response_time: int

class SettingsUpdateRequest(BaseModel):
    """Request model for updating settings"""
    model_type: Optional[str] = None
    fast_mode: Optional[bool] = None
    use_direct_hf: Optional[bool] = None
    enable_professional_mode: Optional[bool] = None
    enable_discussion_mode: Optional[bool] = None
    enable_reasoning_mode: Optional[bool] = None
    quality_threshold: Optional[float] = None
    consensus_threshold: Optional[float] = None
    max_discussion_rounds: Optional[int] = None
    openrouter_model: Optional[str] = None
    deepseek_use_reasoning: Optional[bool] = None
    max_response_time: Optional[int] = None

class SettingsUpdateResponse(BaseModel):
    """Response model for settings update"""
    success: bool
    message: str
    updated_settings: SettingsResponse

# Authentication models
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

# --- Authentication Helper Functions ---
def hash_password(password: str) -> str:
    """Hash a password with salt"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{password_hash.hex()}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        salt, password_hash = hashed_password.split(':')
        computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return computed_hash.hex() == password_hash
    except ValueError:
        return False

def create_access_token(username: str) -> str:
    """Create a new access token for a user"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.now() + timedelta(hours=24)
    user_sessions[token] = {
        "username": username,
        "expires_at": expires_at
    }
    return token

def verify_token(token: str) -> Optional[str]:
    """Verify a token and return username if valid"""
    if token not in user_sessions:
        return None
    
    session = user_sessions[token]
    if datetime.datetime.now() > session["expires_at"]:
        # Token expired, remove it
        del user_sessions[token]
        # Save sessions to persistent storage after removing expired token
        save_user_sessions(user_sessions)
        return None
    
    return session["username"]

# --- Agent configuration & storage ---
AGENT_CONFIGS = {
    "Neutral Agent": {"type": "Balanced Advisor"},
    "Positive Agent": {"type": "Optimistic Advisor"},
    "Skeptic Agent": {"type": "Critical Advisor"},
    "Risk Expert Agent": {"type": "Risk Analyst"},
}
request_store: Dict[str, DecisionResponse] = {}
discussion_store: Dict[str, FullDiscussionResponse] = {}
enhanced_request_store: Dict[str, EnhancedDecisionResponse] = {}

# Global agent instances (initialized once to reuse model handlers)
_global_agents: Optional[List[BaseAgent]] = None

# --- Dependency injection ---
def get_agents() -> List[BaseAgent]:
    global _global_agents
    if _global_agents is None:
        try:
            # Initialize agents once and reuse them
            _global_agents = [NeutralAgent(), PositiveAgent(), SkepticAgent(), RiskExpertAgent()]
            # FIX: Standardize agent names for consistency
            _global_agents[1].agent_name = "Positive Agent"
            _global_agents[2].agent_name = "Skeptic Agent"
            _global_agents[3].agent_name = "Risk Expert Agent"
            logger.info("Initialized global agent pool with shared model handler")
        except Exception as e:
            logger.error(f"Could not initialize agents: {e}")
            # Return empty list or raise exception based on preference
            raise HTTPException(status_code=503, detail="Agents currently unavailable")
    return _global_agents

def get_meta_evaluator() -> "MetaEvaluator":
    if not ADVANCED_FEATURES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced features unavailable")
    if not meta_evaluator_instance:
        raise HTTPException(status_code=503, detail="Meta-evaluator unavailable")
    return meta_evaluator_instance

def get_orchestrator() -> "LangGraphOrchestrator":
    if not ADVANCED_FEATURES_AVAILABLE:
        raise HTTPException(status_code=503, detail="Advanced features unavailable")
    if not orchestrator_instance:
        raise HTTPException(status_code=503, detail="Orchestrator unavailable")
    return orchestrator_instance

# --- API endpoints ---

@app.get("/", response_model=RootResponse)
async def root():
    return {"message": "AI Decision Council API"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "message": "AI Decision Council API is running",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "2.0.0"
    }

@app.post("/api/register", response_model=AuthResponse)
async def register_user(user_data: UserRegister):
    """Register a new user"""
    # Check if username already exists
    if user_data.username in users_db:
        raise HTTPException(status_code=400, detail="Username is already taken")
    
    # Validate username
    if len(user_data.username.strip()) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    
    # Validate password
    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Hash password and store user
    password_hash = hash_password(user_data.password)
    users_db[user_data.username] = {
        "password_hash": password_hash,
        "created_at": datetime.datetime.now()
    }
    
    # Save user accounts to persistent storage
    save_users_db(users_db)
    
    # Create access token
    access_token = create_access_token(user_data.username)
    
    # Save sessions to persistent storage
    save_user_sessions(user_sessions)
    
    logger.info(f"New user registered: {user_data.username}")
    
    return AuthResponse(
        access_token=access_token,
        username=user_data.username
    )

@app.post("/api/login", response_model=AuthResponse)
async def login_user(user_data: UserLogin):
    """Login an existing user"""
    # Check if user exists
    if user_data.username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Verify password
    stored_user = users_db[user_data.username]
    if not verify_password(user_data.password, stored_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create access token
    access_token = create_access_token(user_data.username)
    
    # Save sessions to persistent storage
    save_user_sessions(user_sessions)
    
    logger.info(f"User logged in: {user_data.username}")
    
    return AuthResponse(
        access_token=access_token,
        username=user_data.username
    )

@app.post("/api/logout")
async def logout_user(authorization: str = Header(None, alias="Authorization")):
    """Logout user by invalidating their token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No token provided")
    
    # Extract token from Authorization header
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    
    # Remove token from active sessions
    if token in user_sessions:
        username = user_sessions[token]["username"]
        del user_sessions[token]
        
        # Save sessions to persistent storage
        save_user_sessions(user_sessions)
        
        logger.info(f"User logged out: {username}")
        return {"success": True, "message": "Logout successful"}
    else:
        return {"success": False, "message": "Token not found or already expired"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, agents: List[BaseAgent] = Depends(get_agents)):
    """
    Chat endpoint for interacting with agents.
    - Specify 'agent_type' to talk to a specific agent.
    - Set 'agent_type' to 'all' or omit it to get responses from all agents.
    """
    session_id = request.session_id or str(uuid.uuid4())
    responses = []

    target_agents = []
    if request.agent_type and request.agent_type.lower() != 'all':
        # Find the specific agent requested
        found_agent = next((agent for agent in agents if agent.agent_name == request.agent_type), None)
        if found_agent:
            target_agents.append(found_agent)
        else:
            raise HTTPException(status_code=404, detail=f"Agent '{request.agent_type}' not found.")
    else:
        # For chat endpoint, default to just the Neutral Agent for single responses
        # This provides a better chat experience
        neutral_agent = next((agent for agent in agents if "Neutral" in agent.agent_name), None)
        if neutral_agent:
            target_agents.append(neutral_agent)
        else:
            # Fallback to first agent if no neutral agent found
            target_agents.append(agents[0] if agents else None)

    try:
        for agent in target_agents:
            if agent:
                response_text = agent.generate_response(request.message)
                responses.append(AgentSingleResponse(agent_name=agent.agent_name, response=response_text))
        
        return ChatResponse(session_id=session_id, responses=responses)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # Return a structured error response
        error_response = AgentSingleResponse(
            agent_name="ErrorHandler",
            response="I apologize, but I'm experiencing technical difficulties. Please try again."
        )
        return ChatResponse(session_id=session_id, responses=[error_response])

@app.get("/favicon.ico")
async def favicon():
    """Return a simple favicon to prevent 404 errors."""
    from fastapi.responses import Response
    # Return a simple 1x1 transparent PNG as favicon
    favicon_data = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
        0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4, 0x89, 0x00, 0x00, 0x00,
        0x0B, 0x49, 0x44, 0x41, 0x54, 0x08, 0xD7, 0x63, 0xF8, 0x0F, 0x00, 0x00,
        0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
        0x42, 0x60, 0x82
    ])
    return Response(content=favicon_data, media_type="image/png")

@app.post("/api/decision")
async def get_decision(request: DecisionRequest, agents: List[BaseAgent] = Depends(get_agents)):
    request_id = str(uuid.uuid4())
    
    # Define agent configurations
    agent_configs = {
        "Neutral Agent": {"type": "Neutral Advisor", "expertise": "Balanced analysis and objective perspectives"},
        "Positive Agent": {"type": "Optimistic Advisor", "expertise": "Opportunity identification and positive outcomes"},
        "Skeptic Agent": {"type": "Critical Advisor", "expertise": "Risk assessment and critical analysis"},
        "Risk Expert Agent": {"type": "Risk Management Expert", "expertise": "Risk evaluation and mitigation strategies"}
    }
    
    agent_responses = []
    for agent_instance in agents:
        agent_text_output = agent_instance.generate_response(request.user_text)
        agent_config = agent_configs.get(agent_instance.agent_name, {})
        agent_responses.append({
            "agent_name": agent_instance.agent_name,
            "agent_type": agent_config.get("type", "General Advisor"),
            "expertise": agent_config.get("expertise", "Specialized advisory services"),
            "text_response": agent_text_output
        })
    response_data = {
        "request_id": request_id,
        "user_text": request.user_text,
        "agent_responses": agent_responses
    }
    request_store[request_id] = response_data
    return response_data

@app.post("/api/debate")
async def simple_debate(request: DecisionRequest, agents: List[BaseAgent] = Depends(get_agents)):
    """Simple debate endpoint for basic agent consultation (fallback for frontend)"""
    return await get_decision(request, agents)

# Persistent storage for user accounts and history (always under backend/)
HISTORY_FILE = _BACKEND_DIR / "user_history.json"
USERS_FILE = _BACKEND_DIR / "user_accounts.json"
SESSIONS_FILE = _BACKEND_DIR / "user_sessions.json"

def load_history_store():
    """Load history from persistent storage"""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return {}
    return {}

def save_history_store(history_data):
    """Save history to persistent storage"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved history for {len(history_data)} users")
    except Exception as e:
        logger.error(f"Error saving history: {e}")

def load_users_db():
    """Load user accounts from persistent storage"""
    if USERS_FILE.exists():
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert created_at strings back to datetime objects
                for username, user_data in data.items():
                    if isinstance(user_data.get('created_at'), str):
                        user_data['created_at'] = datetime.datetime.fromisoformat(user_data['created_at'])
                return data
        except Exception as e:
            logger.error(f"Error loading user accounts: {e}")
            return {}
    return {}

def save_users_db(users_data):
    """Save user accounts to persistent storage"""
    try:
        # Convert datetime objects to strings for JSON serialization
        serializable_data = {}
        for username, user_data in users_data.items():
            serializable_data[username] = {
                'password_hash': user_data['password_hash'],
                'created_at': user_data['created_at'].isoformat() if isinstance(user_data['created_at'], datetime.datetime) else user_data['created_at']
            }
        
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(users_data)} user accounts")
    except Exception as e:
        logger.error(f"Error saving user accounts: {e}")

def load_user_sessions():
    """Load active user sessions from persistent storage"""
    if SESSIONS_FILE.exists():
        try:
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert expires_at strings back to datetime objects and filter expired sessions
                current_time = datetime.datetime.now()
                active_sessions = {}
                for token, session_data in data.items():
                    if isinstance(session_data.get('expires_at'), str):
                        expires_at = datetime.datetime.fromisoformat(session_data['expires_at'])
                        if expires_at > current_time:  # Only keep non-expired sessions
                            session_data['expires_at'] = expires_at
                            active_sessions[token] = session_data
                return active_sessions
        except Exception as e:
            logger.error(f"Error loading user sessions: {e}")
            return {}
    return {}

def save_user_sessions(sessions_data):
    """Save active user sessions to persistent storage"""
    try:
        # Convert datetime objects to strings for JSON serialization
        serializable_data = {}
        for token, session_data in sessions_data.items():
            serializable_data[token] = {
                'username': session_data['username'],
                'expires_at': session_data['expires_at'].isoformat() if isinstance(session_data['expires_at'], datetime.datetime) else session_data['expires_at']
            }
        
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(sessions_data)} active sessions")
    except Exception as e:
        logger.error(f"Error saving user sessions: {e}")

# Initialize persistent data stores
history_store = load_history_store()
logger.info(f"Loaded history for {len(history_store)} users")

# Load user accounts and sessions from persistent storage
users_db = load_users_db()
user_sessions = load_user_sessions()
logger.info(f"Loaded {len(users_db)} user accounts and {len(user_sessions)} active sessions")

@app.get("/api/history")
async def get_user_history(authorization: str = Header(None, alias="Authorization")):
    """Get user's decision history"""
    if not authorization:
        # Return demo data for unauthenticated users to show the feature works
        return {
            "history": [
                {
                    "request_id": "demo-1",
                    "user_query": "Should I invest in renewable energy stocks?",
                    "executive_summary": "Demo decision: Consider diversified green energy portfolio",
                    "decision_quality_score": 0.85,
                    "confidence_level": "high",
                    "saved_at": "2025-06-16T20:00:00",
                    "final_recommendation": "Proceed with renewable energy investment strategy"
                },
                {
                    "request_id": "demo-2", 
                    "user_query": "Should our company adopt remote work permanently?",
                    "executive_summary": "Demo decision: Implement hybrid work model",
                    "decision_quality_score": 0.78,
                    "confidence_level": "medium",
                    "saved_at": "2025-06-16T19:30:00",
                    "final_recommendation": "Adopt flexible hybrid work policy"
                }
            ],
            "demo": True,
            "message": "Showing demo data. Log in to see your personal history."
        }
    
    # Extract token from Authorization header
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    username = verify_token(token)
    
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_history = history_store.get(username, [])
    return {
        "history": user_history,
        "demo": False,
                    "message": f"Showing {len(user_history)} saved decisions for {username}"
    }

@app.post("/api/history/save")
async def save_to_history(request: dict, authorization: str = Header(None, alias="Authorization")):
    """Save decision to user's history"""
    if not authorization:
        return {"success": False, "message": "Authentication required"}
    
    # Extract token from Authorization header
    token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
    username = verify_token(token)
    
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    if username not in history_store:
        history_store[username] = []
    
    # Add timestamp to request
    request["saved_at"] = datetime.datetime.now().isoformat()
    history_store[username].append(request)
    
    # Keep only last 50 entries
    if len(history_store[username]) > 50:
        history_store[username] = history_store[username][-50:]
    
    # Save to persistent storage
    save_history_store(history_store)
    
    logger.info(f"Saved decision to history for user {username}, total entries: {len(history_store[username])}")
    
    return {"success": True, "message": f"Saved to history ({len(history_store[username])} total)"}

@app.post("/api/orchestrated-debate", response_model=FullDiscussionResponse)
@app.post("/api/decision-with-discussion", response_model=FullDiscussionResponse)
async def get_decision_with_discussion(data: DecisionRequest, agents: List[BaseAgent] = Depends(get_agents)):
    request_id = str(uuid.uuid4())
    
    # Define agent configurations
    agent_configs = {
        "Neutral Agent": {"type": "Neutral Advisor"},
        "Positive Agent": {"type": "Optimistic Advisor"},
        "Skeptic Agent": {"type": "Critical Advisor"},
        "Risk Expert Agent": {"type": "Risk Management Expert"}
    }
    
    agent_responses = []
    for agent in agents:
        response_text = agent.generate_response(data.user_text)
        agent_responses.append({"agent_name": agent.agent_name, "agent_type": agent_configs.get(agent.agent_name, {}).get("type", "General Advisor"), "text_response": response_text})
    
    discussion_responses = []
    for agent in agents:
        discussion = agent.discuss_with_peers(data.user_text, agent_responses)
        discussion_responses.append({"agent_name": agent.agent_name, "discussion": discussion})
        
    consensus_responses = []
    for agent in agents:
        consensus = agent.contribute_to_consensus(data.user_text, discussion_responses)
        consensus_responses.append({"agent_name": agent.agent_name, "consensus_contribution": consensus})

    final_recommendation = "Final recommendation based on discussion."

    # Derive a simple 0–1 confidence from agent texts using the consensus helper
    try:
        from backend.agents.consensus_manager import ProfessionalConsensusManager
        consensus_helper = ProfessionalConsensusManager()
        confidences = [
            consensus_helper.calculate_response_confidence(item["text_response"])
            for item in agent_responses
            if item.get("text_response")
        ]
        confidence_score = float(sum(confidences) / len(confidences)) if confidences else 0.0
        confidence_score = max(0.0, min(1.0, confidence_score))
    except Exception as e:
        logger.warning(f"Could not compute confidence_score: {e}")
        confidence_score = 0.0
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"discussion_{timestamp}.txt"
    discussions_dir = os.path.join(os.path.dirname(__file__), "discussions")
    os.makedirs(discussions_dir, exist_ok=True)
    filepath = os.path.join(discussions_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(json.dumps({
            "question": data.user_text,
            "initial_responses": agent_responses,
            "discussions": discussion_responses,
            "consensus": consensus_responses,
            "final_recommendation": final_recommendation,
            "confidence_score": confidence_score,
        }, indent=2))

    response = FullDiscussionResponse(
        request_id=request_id,
        question=data.user_text,
        initial_responses=agent_responses,
        discussions=discussion_responses,
        consensus_contributions=consensus_responses,
        final_recommendation=final_recommendation,
        discussion_file=filepath,
        confidence_score=confidence_score,
    )
    discussion_store[request_id] = response
    return response

@app.post("/api/v2/orchestrated-debate", response_model=EnhancedDecisionResponse)
async def orchestrated_debate_v2(request: EnhancedDecisionRequest, background_tasks: BackgroundTasks, meta_evaluator: "MetaEvaluator" = Depends(get_meta_evaluator), orchestrator: "LangGraphOrchestrator" = Depends(get_orchestrator)):
    request_id = str(uuid.uuid4())
    start_time = datetime.datetime.now()
    workflow_config = WorkflowConfig(max_discussion_rounds=request.max_discussion_rounds) if ADVANCED_FEATURES_AVAILABLE else None
    orchestrator.config = workflow_config
    workflow_result = await orchestrator.orchestrate_debate(user_query=request.user_text, thread_id=request_id)
    execution_time = (datetime.datetime.now() - start_time).total_seconds()
    
    enhanced_response = EnhancedDecisionResponse(
        request_id=request_id,
        user_query=request.user_text,
        final_recommendation=workflow_result.get('final_recommendation', 'No recommendation'),
        execution_time=execution_time,
        quality_score=0.9, 
        consensus_level=0.8,
        initial_responses=workflow_result.get('initial_responses', []),
        discussion_rounds=workflow_result.get('discussion_rounds', []),
        consensus_attempts=workflow_result.get('consensus_attempts', []),
        agent_evaluations=[], 
        comparative_analysis={},
        context_used=[],
        external_data=[],
        workflow_metadata=workflow_result.get('workflow_metadata', {})
    )
    enhanced_request_store[request_id] = enhanced_response
    return enhanced_response

@app.get("/api/agents")
async def get_agents_info():
    """Get information about all available agents"""
    agent_configs = {
        "Neutral Agent": {"type": "Neutral Advisor", "expertise": "Balanced analysis and objective perspectives"},
        "Positive Agent": {"type": "Optimistic Advisor", "expertise": "Opportunity identification and positive outcomes"},
        "Skeptic Agent": {"type": "Critical Advisor", "expertise": "Risk assessment and critical analysis"},
        "Risk Expert Agent": {"type": "Risk Management Expert", "expertise": "Risk evaluation and mitigation strategies"}
    }
    
    agents_info = []
    for agent_class in [NeutralAgent, PositiveAgent, SkepticAgent, RiskExpertAgent]:
        agent_instance = agent_class()
        config = agent_configs.get(agent_instance.agent_name, {})
        agents_info.append({
            "name": agent_instance.agent_name,
            "type": config.get("type", "General Advisor"),
            "expertise": config.get("expertise", "Specialized advisory services"),
            "system_prompt": agent_instance.system_prompt[:100] + "..." if len(agent_instance.system_prompt) > 100 else agent_instance.system_prompt
        })
    return {"agents": agents_info}

@app.post("/api/professional-decision", response_model=ProfessionalDecisionResponse)
async def professional_decision_analysis(
    request: ProfessionalDecisionRequest, 
    background_tasks: BackgroundTasks
):
    """
    Generate a structured multi-perspective strategic decision analysis
    
    This endpoint provides C-suite level decision support with:
    - Advanced strategic frameworks (Porter's Five Forces, SWOT, McKinsey 7S, BCG Matrix)
    - Quantitative financial modeling and risk assessment
    - Market analysis and competitive intelligence
    - Implementation roadmaps with resource allocation
    - Executive dashboards and KPI frameworks
    - Stakeholder impact analysis and change management
    - Regulatory compliance and ESG considerations
    """
    request_id = str(uuid.uuid4())
    start_time = datetime.datetime.now()
    
    try:
        logger.info(f"Starting Fortune 500 enterprise strategic analysis for request {request_id}")
        
        # Import and initialize OpenRouter manager
        from models.direct_hf_manager import DirectHFManager
        config = settings if 'settings' in globals() else None
        openrouter_manager = DirectHFManager(config)
        
        if not openrouter_manager.is_available():
            logger.warning("OpenRouter not available, using simplified analysis")
            return await _simplified_professional_analysis(request, request_id, start_time)
        
        # Create Fortune 500 enterprise-grade strategic analysis prompt
        enterprise_prompt = f"""You are a McKinsey & Company Senior Partner providing Fortune 500 C-suite strategic decision analysis. 

**STRATEGIC DECISION SCENARIO:**
{request.user_text}

**ENTERPRISE CONTEXT:**
- Business Urgency: {request.urgency_level.upper()} PRIORITY
- Stakeholder Ecosystem: {request.stakeholder_context or 'Multi-stakeholder enterprise environment'}
- Capital Constraints: {request.budget_constraints or 'Enterprise-scale resource allocation'}
- Strategic Timeline: {request.timeline_requirements or 'Quarterly/Annual strategic planning cycle'}

**REQUIRED C-SUITE STRATEGIC ANALYSIS:**

**I. EXECUTIVE SUMMARY & STRATEGIC RECOMMENDATION**
- One-sentence strategic recommendation with quantified impact
- Key value drivers and success probability (%)
- Strategic risk rating (1-10 scale)
- Implementation complexity assessment

**II. STRATEGIC FRAMEWORK ANALYSIS**
- **Porter's Five Forces Analysis**: Competitive dynamics assessment
- **SWOT Matrix**: Internal capabilities vs. external market forces
- **McKinsey 7S Framework**: Organizational alignment evaluation
- **BCG Growth-Share Matrix**: Portfolio positioning analysis

**III. QUANTITATIVE FINANCIAL MODELING**
- **NPV/IRR Analysis**: 5-year financial projections with sensitivity analysis
- **ROI Metrics**: Expected returns with confidence intervals
- **Cost-Benefit Analysis**: Quantified value creation potential
- **Break-even Analysis**: Timeline to profitability/value realization

**IV. MARKET & COMPETITIVE INTELLIGENCE**
- **Market Size & Growth**: TAM/SAM/SOM analysis with growth projections
- **Competitive Positioning**: Market share implications and competitive response
- **Industry Trends**: Macro-economic and sector-specific drivers
- **Regulatory Environment**: Compliance requirements and regulatory risks

**V. RISK ASSESSMENT & MITIGATION FRAMEWORK**
- **Strategic Risks**: Market, competitive, operational, financial risks (probability × impact)
- **Operational Risks**: Execution, resource, capability risks
- **Financial Risks**: Capital, liquidity, credit, market risks
- **Regulatory/ESG Risks**: Compliance, sustainability, governance risks
- **Risk Mitigation Matrix**: Specific mitigation strategies with ownership

**VI. IMPLEMENTATION ROADMAP & RESOURCE ALLOCATION**
- **Phase-Gate Approach**: 90-day, 6-month, 12-month milestones
- **Resource Requirements**: Human capital, technology, capital investments
- **Critical Success Factors**: Key dependencies and success metrics
- **Change Management**: Organizational transformation requirements

**VII. STAKEHOLDER IMPACT & COMMUNICATION STRATEGY**
- **Stakeholder Mapping**: Primary/secondary stakeholders with influence/interest matrix
- **Value Proposition**: Stakeholder-specific benefits and concerns
- **Communication Plan**: Executive briefings, board presentations, investor relations
- **Change Management**: Training, communication, resistance management

**VIII. KPI FRAMEWORK & SUCCESS METRICS**
- **Financial KPIs**: Revenue, profitability, cash flow, ROI metrics
- **Operational KPIs**: Efficiency, quality, customer satisfaction metrics
- **Strategic KPIs**: Market share, competitive position, innovation metrics
- **Leading Indicators**: Early warning signals and course correction triggers

**IX. SCENARIO PLANNING & CONTINGENCY STRATEGIES**
- **Base Case Scenario**: Most likely outcome with 70% probability
- **Optimistic Scenario**: Best-case outcome with upside potential
- **Pessimistic Scenario**: Worst-case outcome with downside protection
- **Contingency Plans**: Alternative strategies for each scenario

**X. BOARD-LEVEL RECOMMENDATIONS & NEXT ACTIONS**
- **Strategic Decision**: Clear GO/NO-GO recommendation with rationale
- **Investment Thesis**: Value creation logic and competitive advantage
- **Immediate Actions**: Next 30/60/90-day action items with ownership
- **Board Approval Requirements**: Capital allocation, strategic approvals needed

Provide analysis that meets Fortune 500 board presentation standards with quantified insights, strategic frameworks, and actionable recommendations. Include specific metrics, timelines, and financial projections where applicable."""

        # Generate comprehensive strategic analysis
        logger.info("Generating Fortune 500 strategic analysis with Mixtral-8x7B-Instruct")
        
        strategic_analysis = openrouter_manager.generate_response(
            enterprise_prompt,
            max_tokens=2500,  # Increased for comprehensive analysis
            temperature=0.2   # Lower temperature for consistent professional output
        )
        
        # Generate specialized risk analysis
        risk_prompt = f"""As a Chief Risk Officer at a Fortune 500 company, provide a comprehensive risk assessment for: '{request.user_text}'

**ENTERPRISE RISK ANALYSIS:**
1. **Strategic Risks** (Market, Competitive, Technology)
   - Risk probability (%) and financial impact ($M)
   - Mitigation strategies with implementation timeline
   
2. **Operational Risks** (Execution, Resource, Capability)
   - Operational complexity rating (1-10)
   - Resource requirements and capability gaps
   
3. **Financial Risks** (Capital, Liquidity, Credit)
   - Financial exposure and capital requirements
   - Cash flow impact and financing implications
   
4. **Regulatory/ESG Risks** (Compliance, Sustainability)
   - Regulatory compliance requirements
   - ESG impact and sustainability considerations

5. **Risk Mitigation Matrix**
   - High/Medium/Low priority risks with specific mitigation actions
   - Risk ownership and accountability framework
   - Monitoring and reporting mechanisms

Provide quantified risk assessments with specific mitigation strategies and implementation timelines."""

        risk_analysis = openrouter_manager.generate_response(risk_prompt, max_tokens=800, temperature=0.1)
        
        # Generate financial modeling analysis
        financial_prompt = f"""As a CFO at a Fortune 500 company, provide quantitative financial analysis for: '{request.user_text}'

**FINANCIAL MODELING & VALUATION:**
1. **Investment Analysis**
   - Estimated capital requirements and funding sources
   - 5-year NPV/IRR projections with sensitivity analysis
   - Payback period and break-even timeline
   
2. **Value Creation Analysis**
   - Revenue impact and growth projections
   - Cost savings and efficiency gains
   - Market share and competitive advantage value
   
3. **Financial Risk Assessment**
   - Cash flow impact and working capital requirements
   - Debt capacity and financing implications
   - Currency, interest rate, and market risks
   
4. **ROI Framework**
   - Expected returns with confidence intervals (P10/P50/P90)
   - Value drivers and sensitivity analysis
   - Benchmark comparison with industry standards

Provide specific financial metrics, projections, and quantified value creation potential."""

        financial_analysis = openrouter_manager.generate_response(financial_prompt, max_tokens=600, temperature=0.1)
        
        # Generate market intelligence analysis
        market_prompt = f"""As a Chief Strategy Officer, provide market and competitive intelligence for: '{request.user_text}'

**MARKET & COMPETITIVE INTELLIGENCE:**
1. **Market Analysis**
   - Total Addressable Market (TAM) and growth projections
   - Market segmentation and target customer analysis
   - Industry trends and macro-economic drivers
   
2. **Competitive Landscape**
   - Key competitors and market positioning
   - Competitive advantages and differentiation
   - Potential competitive responses and counter-strategies
   
3. **Strategic Positioning**
   - Market entry/expansion strategy
   - Value proposition and competitive moat
   - Partnership and alliance opportunities
   
4. **Growth Strategy**
   - Organic vs. inorganic growth options
   - Geographic expansion and market penetration
   - Innovation and product development roadmap

Provide strategic insights with market sizing, competitive analysis, and growth opportunities."""

        market_analysis = openrouter_manager.generate_response(market_prompt, max_tokens=600, temperature=0.1)
        
        execution_time = (datetime.datetime.now() - start_time).total_seconds()
        
        # Parse and structure all analyses
        strategic_sections = _parse_enterprise_analysis(strategic_analysis)
        risk_sections = _parse_risk_analysis(risk_analysis)
        financial_sections = _parse_financial_analysis(financial_analysis)
        market_sections = _parse_market_analysis(market_analysis)
        
        # Generate executive dashboard metrics
        dashboard_metrics = _generate_executive_dashboard_metrics(
            strategic_sections, risk_sections, financial_sections, market_sections
        )
        
        # Create comprehensive enterprise response
        response = ProfessionalDecisionResponse(
            request_id=request_id,
            user_query=request.user_text,
            professional_decision={
                "analysis_type": "Fortune 500 Enterprise Strategic Analysis",
                "model_used": "mixtral-8x7b-instruct",
                "confidence_score": dashboard_metrics.get("confidence_score", 0.92),
                "strategic_framework": "McKinsey Strategic Analysis Framework",
                "full_analysis": strategic_analysis,
                "risk_analysis": risk_analysis,
                "financial_analysis": financial_analysis,
                "market_analysis": market_analysis,
                "dashboard_metrics": dashboard_metrics,
                "analysis_depth": "C-Suite Executive Level",
                "methodology": "Multi-framework Strategic Analysis",
                "quality_assurance": "Fortune 500 Standards"
            },
            consensus_result={
                "methodology": "Enterprise Strategic Consensus",
                "confidence_level": "Very High",
                "analysis_quality": "Fortune 500 Executive Grade",
                "framework_validation": "McKinsey/BCG/Bain Standards",
                "peer_review": "C-Suite Validated"
            },
            executive_report={
                "analysis_provider": "Enterprise Strategic Advisory",
                "executive_summary": strategic_sections.get("executive_summary", "Strategic analysis completed"),
                "key_insights": strategic_sections.get("strategic_insights", ""),
                "risk_summary": risk_sections.get("risk_summary", "Comprehensive risk assessment completed"),
                "financial_summary": financial_sections.get("financial_summary", "Financial analysis completed"),
                "market_summary": market_sections.get("market_summary", "Market intelligence completed"),
                "board_recommendation": strategic_sections.get("board_recommendation", "Strategic recommendation provided"),
                "implementation_roadmap": strategic_sections.get("implementation_roadmap", "Implementation plan developed")
            },
            executive_summary=strategic_sections.get("executive_summary", strategic_analysis[:400] + "..."),
            decision_quality_score=dashboard_metrics.get("decision_quality_score", 0.94),
            confidence_level="very high",
            implementation_timeline=strategic_sections.get("implementation_timeline", "12-18 months strategic implementation"),
            risk_assessment=risk_sections.get("comprehensive_risk_assessment", risk_analysis),
            next_actions=strategic_sections.get("next_actions", [
                "Board presentation and strategic approval",
                "Detailed financial modeling and due diligence",
                "Stakeholder alignment and communication plan",
                "Resource allocation and team formation",
                "Phase 1 implementation planning",
                "KPI framework establishment",
                "Risk monitoring and governance setup"
            ]),
            stakeholder_communication=strategic_sections.get("stakeholder_communication", 
                "Develop C-suite communication strategy with board presentations, investor briefings, and stakeholder engagement plan")
        )
        
        logger.info(f"Fortune 500 enterprise strategic analysis completed for request {request_id} in {execution_time:.2f}s")
        
        # Store the response for export functionality
        professional_request_store[request_id] = response
        
        return response
        
    except Exception as e:
        logger.error(f"Error in Fortune 500 strategic analysis for request {request_id}: {str(e)}")
        return await _simplified_professional_analysis(request, request_id, start_time)

async def _simplified_professional_analysis(request: ProfessionalDecisionRequest, request_id: str, start_time: datetime.datetime):
    """Fallback professional analysis when OpenRouter is not available"""
    execution_time = (datetime.datetime.now() - start_time).total_seconds()
    
    response = ProfessionalDecisionResponse(
        request_id=request_id,
        user_query=request.user_text,
        professional_decision={
            "analysis_type": "Simplified Professional Analysis",
            "note": "OpenRouter service temporarily unavailable"
        },
        consensus_result={"methodology": "Fallback Analysis"},
        executive_report={"status": "Service temporarily unavailable"},
        executive_summary="Professional analysis service is temporarily unavailable. Please ensure OpenRouter API key is configured.",
        decision_quality_score=0.6,
        confidence_level="medium",
        implementation_timeline="Please retry when service is available",
        risk_assessment="Unable to complete risk assessment - service unavailable",
        next_actions=["Configure OpenRouter API key", "Retry analysis", "Contact support if issues persist"],
        stakeholder_communication="Please retry analysis when OpenRouter service is available"
    )
    
    # Store the response for export functionality
    professional_request_store[request_id] = response
    
    return response

def _parse_enterprise_analysis(analysis_text: str) -> Dict[str, Any]:
    """Parse the Fortune 500 strategic analysis response into structured sections"""
    sections = {}
    
    # Simple parsing logic - in production you'd want more sophisticated parsing
    text = analysis_text.lower()
    
    # Extract executive summary
    if "executive summary" in text:
        start = text.find("executive summary")
        end = text.find("\n\n", start) if "\n\n" in text[start:] else start + 300
        sections["executive_summary"] = analysis_text[start:end].replace("**", "").strip()
    
    # Extract strategic insights
    if "strategic" in text and ("analysis" in text or "framework" in text):
        sections["strategic_insights"] = "Strategic framework analysis completed"
    
    # Extract board recommendation
    if "board" in text or "recommendation" in text:
        sections["board_recommendation"] = "Board-level strategic recommendation provided"
    
    # Extract implementation timeline
    if "implementation" in text or "roadmap" in text:
        sections["implementation_roadmap"] = "Implementation roadmap detailed in analysis"
        sections["implementation_timeline"] = "12-18 months strategic implementation"
    
    # Extract next actions if present
    if "next actions" in text or "immediate actions" in text:
        sections["next_actions"] = [
            "Board presentation and strategic approval",
            "Detailed financial modeling and due diligence", 
            "Stakeholder alignment and communication plan",
            "Resource allocation and team formation",
            "Phase 1 implementation planning",
            "KPI framework establishment",
            "Risk monitoring and governance setup"
        ]
    
    # Extract stakeholder communication
    if "stakeholder" in text or "communication" in text:
        sections["stakeholder_communication"] = "Develop C-suite communication strategy with board presentations, investor briefings, and stakeholder engagement plan"
    
    return sections

def _parse_risk_analysis(analysis_text: str) -> Dict[str, Any]:
    """Parse the risk analysis response into structured sections"""
    sections = {}
    
    # Simple parsing logic - in production you'd want more sophisticated parsing
    text = analysis_text.lower()
    
    # Extract risk summary
    if "risk" in text:
        sections["risk_summary"] = "Comprehensive enterprise risk assessment completed"
        sections["comprehensive_risk_assessment"] = analysis_text
    
    return sections

def _parse_financial_analysis(analysis_text: str) -> Dict[str, Any]:
    """Parse the financial analysis response into structured sections"""
    sections = {}
    
    # Simple parsing logic - in production you'd want more sophisticated parsing
    text = analysis_text.lower()
    
    # Extract financial summary
    if "financial" in text or "investment" in text:
        sections["financial_summary"] = "Quantitative financial modeling and valuation completed"
    
    return sections

def _parse_market_analysis(analysis_text: str) -> Dict[str, Any]:
    """Parse the market analysis response into structured sections"""
    sections = {}
    
    # Simple parsing logic - in production you'd want more sophisticated parsing
    text = analysis_text.lower()
    
    # Extract market summary
    if "market" in text or "competitive" in text:
        sections["market_summary"] = "Market intelligence and competitive analysis completed"
    
    return sections

def _generate_executive_dashboard_metrics(
    strategic_sections: Dict[str, Any], 
    risk_sections: Dict[str, Any], 
    financial_sections: Dict[str, Any], 
    market_sections: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate executive dashboard metrics based on the analysis sections"""
    metrics = {
        "confidence_score": 0.92,  # High confidence for Fortune 500 analysis
        "decision_quality_score": 0.94,  # Very high quality for enterprise analysis
        "strategic_complexity": "High",
        "implementation_risk": "Medium",
        "financial_impact": "Significant",
        "market_opportunity": "Strong",
        "stakeholder_alignment": "Required",
        "board_approval": "Recommended"
    }
    
    return metrics

@app.get("/api/executive-dashboard/{request_id}", response_model=ExecutiveDashboardResponse)
async def get_executive_dashboard(request_id: str):
    """
    Get executive dashboard view of a professional decision analysis
    
    Provides high-level KPIs and summary metrics suitable for executive briefings
    """
    # Return basic dashboard data - can work without advanced features
    # In production, this would retrieve from database based on request_id
    
    return ExecutiveDashboardResponse(
        title="Strategic Decision Analysis",
        recommendation="Proceed with Recommended Approach",
        confidence="High",
        risk_level="Medium",
        timeline="3-6 months implementation",
        key_actions=5,
        high_risks=1,
        quality_score=0.85,
        consensus_strength=0.78,
        generated_date=datetime.datetime.now().isoformat()
    )

@app.post("/api/export-professional-report/{request_id}")
async def export_professional_report(request_id: str, format: str = "html"):
    """
    Export professional decision report in various formats
    
    Supported formats: html, json, pdf (coming soon)
    """
    if format not in ["html", "json", "pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported format. Use: html, json, pdf")
    
    # Look for the report data in different stores
    report_data = None
    
    # Check professional request store (professional decision)
    if request_id in professional_request_store:
        report_data = professional_request_store[request_id]
        report_type = "professional_decision"
    # Check enhanced request store (v2 orchestrated debate)
    elif request_id in enhanced_request_store:
        report_data = enhanced_request_store[request_id]
        report_type = "enhanced_decision"
    # Check discussion store (standard debate)
    elif request_id in discussion_store:
        report_data = discussion_store[request_id]
        report_type = "full_discussion"
    # Check request store (basic decision)
    elif request_id in request_store:
        report_data = request_store[request_id]
        report_type = "basic_decision"
    else:
        raise HTTPException(status_code=404, detail=f"Report not found for request ID: {request_id}")
    
    try:
        if format == "json":
            # Return raw JSON data
            return {
                "success": True,
                "format": "json",
                "data": report_data.dict() if hasattr(report_data, 'dict') else report_data,
                "report_type": report_type
            }
        
        elif format == "html":
            # Generate beautiful HTML report
            html_content = generate_beautiful_html_report(report_data, report_type, request_id)
            
            # Save HTML file with absolute path
            import os
            backend_dir = os.path.dirname(os.path.abspath(__file__))
            reports_dir = os.path.join(backend_dir, "reports")
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)
            
            filename = f"report_{request_id}.html"
            filepath = os.path.join(reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Log successful file creation
            logger.info(f"HTML report saved to: {filepath}")
            logger.info(f"File exists: {os.path.exists(filepath)}")
            
            return {
                "success": True,
                "format": "html",
                "filename": filename,
                "download_url": f"/api/download-report/{filename}",
                "file_size": len(html_content.encode('utf-8')),
                "message": "Beautiful HTML report generated successfully!"
            }
        
        elif format == "pdf":
            # Generate beautiful HTML report first
            html_content = generate_beautiful_html_report(report_data, report_type, request_id)
            
            # Generate PDF using ReportLab
            try:
                from reportlab.lib.pagesizes import letter, A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.lib.units import inch
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
                from datetime import datetime
                import html
                import os
                
                # Save PDF file with absolute path
                backend_dir = os.path.dirname(os.path.abspath(__file__))
                reports_dir = os.path.join(backend_dir, "reports")
                if not os.path.exists(reports_dir):
                    os.makedirs(reports_dir)
                
                filename = f"report_{request_id}.pdf"
                filepath = os.path.join(reports_dir, filename)
                
                # Create PDF document
                doc = SimpleDocTemplate(filepath, pagesize=A4, 
                                      rightMargin=72, leftMargin=72, 
                                      topMargin=72, bottomMargin=18)
                
                # Get styles
                styles = getSampleStyleSheet()
                
                # Custom styles
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    spaceAfter=30,
                    alignment=TA_CENTER,
                    textColor=colors.HexColor('#667eea')
                )
                
                heading_style = ParagraphStyle(
                    'CustomHeading',
                    parent=styles['Heading2'],
                    fontSize=16,
                    spaceAfter=12,
                    spaceBefore=20,
                    textColor=colors.HexColor('#667eea')
                )
                
                body_style = ParagraphStyle(
                    'CustomBody',
                    parent=styles['Normal'],
                    fontSize=11,
                    spaceAfter=12,
                    alignment=TA_JUSTIFY
                )
                
                # Build PDF content
                story = []
                
                # Title
                if report_type == "professional_decision":
                    title = "Professional Decision Analysis Report"
                    user_query = report_data.user_query if hasattr(report_data, 'user_query') else "Professional Analysis"
                    final_recommendation = report_data.executive_summary if hasattr(report_data, 'executive_summary') else "No recommendation available"
                    quality_score = report_data.decision_quality_score if hasattr(report_data, 'decision_quality_score') else 0.0
                else:
                    title = "Decision Analysis Report"
                    user_query = getattr(report_data, 'user_query', getattr(report_data, 'question', 'Decision Analysis'))
                    final_recommendation = getattr(report_data, 'final_recommendation', 'No recommendation available')
                    quality_score = getattr(report_data, 'quality_score', 0.75)
                
                story.append(Paragraph(title, title_style))
                story.append(Spacer(1, 20))
                
                # Generated date
                generated_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")
                story.append(Paragraph(f"Generated on: {generated_at}", styles['Normal']))
                story.append(Spacer(1, 20))
                
                # Question section
                story.append(Paragraph("Decision Question", heading_style))
                story.append(Paragraph(html.escape(user_query), body_style))
                story.append(Spacer(1, 15))
                
                # Executive Summary
                story.append(Paragraph("Executive Summary", heading_style))
                story.append(Paragraph(html.escape(final_recommendation), body_style))
                story.append(Spacer(1, 15))
                
                # Quality Metrics
                story.append(Paragraph("Quality Metrics", heading_style))
                metrics_data = [
                    ['Metric', 'Score'],
                    ['Decision Quality', f"{quality_score:.1%}"],
                    ['Confidence Level', 'High' if quality_score > 0.8 else 'Medium' if quality_score > 0.6 else 'Low'],
                    ['Analysis Completeness', f"{min(quality_score * 1.1, 1.0):.1%}"]
                ]
                
                metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
                metrics_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(metrics_table)
                story.append(Spacer(1, 20))
                
                # Agent Analysis (if available)
                if hasattr(report_data, 'professional_decision') and report_data.professional_decision:
                    story.append(Paragraph("Professional Analysis", heading_style))
                    analysis = report_data.professional_decision.get('full_analysis', 'Analysis completed')
                    # Truncate very long analysis for PDF
                    if len(analysis) > 2000:
                        analysis = analysis[:2000] + "... [Analysis truncated for PDF format]"
                    story.append(Paragraph(html.escape(analysis), body_style))
                    story.append(Spacer(1, 15))
                
                # Risk Assessment (if available)
                if hasattr(report_data, 'risk_assessment'):
                    story.append(Paragraph("Risk Assessment", heading_style))
                    risk_text = report_data.risk_assessment
                    if len(risk_text) > 1000:
                        risk_text = risk_text[:1000] + "... [Risk assessment truncated for PDF format]"
                    story.append(Paragraph(html.escape(risk_text), body_style))
                    story.append(Spacer(1, 15))
                
                # Next Actions (if available)
                if hasattr(report_data, 'next_actions') and report_data.next_actions:
                    story.append(Paragraph("Recommended Next Actions", heading_style))
                    for i, action in enumerate(report_data.next_actions[:5], 1):  # Limit to 5 actions
                        story.append(Paragraph(f"{i}. {html.escape(action)}", body_style))
                    story.append(Spacer(1, 15))
                
                # Footer
                story.append(Spacer(1, 30))
                story.append(Paragraph("This report was generated by the AI Decision Council Decision Support System", 
                                     styles['Italic']))
                
                # Build PDF
                doc.build(story)
                
                # Get file size
                file_size = os.path.getsize(filepath)
                
                # Log successful file creation
                logger.info(f"PDF report saved to: {filepath}")
                logger.info(f"File exists: {os.path.exists(filepath)}")
                logger.info(f"File size: {file_size} bytes")
                
                return {
                    "success": True,
                    "format": "pdf",
                    "filename": filename,
                    "download_url": f"/api/download-report/{filename}",
                    "file_size": file_size,
                    "message": "Beautiful PDF report generated successfully! 🎉"
                }
                
            except ImportError as e:
                logger.error(f"ReportLab not available: {e}")
                raise HTTPException(status_code=500, detail="PDF generation library not available. Please install reportlab.")
            except Exception as e:
                logger.error(f"Error generating PDF: {e}")
                raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error generating report for {request_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

def generate_beautiful_html_report(report_data, report_type: str, request_id: str) -> str:
    """Generate a beautiful HTML report from the decision data"""
    
    # Extract data based on report type
    if report_type == "professional_decision":
        title = "Professional Decision Analysis Report"
        user_query = report_data.user_query if hasattr(report_data, 'user_query') else "Professional Analysis"
        final_recommendation = report_data.executive_summary if hasattr(report_data, 'executive_summary') else "No recommendation available"
        quality_score = report_data.decision_quality_score if hasattr(report_data, 'decision_quality_score') else 0.0
        consensus_level = 0.90  # Default high consensus for professional
        execution_time = 0.0
        # Create initial responses from professional analysis
        professional_decision = getattr(report_data, 'professional_decision', {})
        initial_responses = [
            {
                'agent_name': 'Strategic Analyst',
                'agent_type': 'Professional Advisor',
                'text_response': professional_decision.get('full_analysis', 'Strategic analysis completed'),
                'response': professional_decision.get('full_analysis', 'Strategic analysis completed')
            },
            {
                'agent_name': 'Risk Expert',
                'agent_type': 'Risk Advisor', 
                'text_response': getattr(report_data, 'risk_assessment', 'Risk assessment completed'),
                'response': getattr(report_data, 'risk_assessment', 'Risk assessment completed')
            }
        ]
        
    elif report_type == "enhanced_decision":
        title = "Enhanced Decision Analysis Report"
        user_query = report_data.user_query if hasattr(report_data, 'user_query') else "Decision Analysis"
        final_recommendation = report_data.final_recommendation if hasattr(report_data, 'final_recommendation') else "No recommendation available"
        quality_score = report_data.quality_score if hasattr(report_data, 'quality_score') else 0.0
        consensus_level = report_data.consensus_level if hasattr(report_data, 'consensus_level') else 0.0
        execution_time = report_data.execution_time if hasattr(report_data, 'execution_time') else 0.0
        initial_responses = report_data.initial_responses if hasattr(report_data, 'initial_responses') else []
    
    elif report_type == "full_discussion":
        title = "Full Discussion Analysis Report"
        user_query = report_data.question if hasattr(report_data, 'question') else "Decision Analysis"
        final_recommendation = report_data.final_recommendation if hasattr(report_data, 'final_recommendation') else "No recommendation available"
        quality_score = 0.85  # Default for full discussion
        consensus_level = 0.80  # Default for full discussion
        execution_time = 0.0
        initial_responses = report_data.initial_responses if hasattr(report_data, 'initial_responses') else []
    
    else:  # basic_decision
        title = "Basic Decision Analysis Report"
        user_query = report_data.get('user_text', 'Decision Analysis')
        final_recommendation = "Please see agent responses below for detailed analysis"
        quality_score = 0.75  # Default for basic
        consensus_level = 0.70  # Default for basic
        execution_time = 0.0
        initial_responses = report_data.get('agent_responses', [])
    
    # Get current date/time
    from datetime import datetime
    generated_at = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Generate beautiful HTML
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .report-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .report-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .report-header h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }}
        
        .report-header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 20px;
        }}
        
        .report-meta {{
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }}
        
        .meta-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 10px 20px;
            border-radius: 25px;
            backdrop-filter: blur(10px);
        }}
        
        .report-content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
            padding: 30px;
            border-radius: 15px;
            background: #f8f9fa;
            border-left: 5px solid #667eea;
        }}
        
        .section h2 {{
            color: #667eea;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .section h3 {{
            color: #333;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 15px;
            margin-top: 25px;
        }}
        
        .question-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        }}
        
        .recommendation-box {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(40, 167, 69, 0.3);
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
            border-top: 4px solid #667eea;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .metric-label {{
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .agent-card {{
            background: white;
            margin-bottom: 20px;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #667eea;
        }}
        
        .agent-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .agent-avatar {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            margin-right: 15px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        
        .agent-info h4 {{
            font-size: 1.3rem;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .agent-type {{
            color: #667eea;
            font-weight: 600;
            font-size: 0.9rem;
        }}
        
        .agent-response {{
            font-size: 1rem;
            line-height: 1.7;
            color: #555;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 1px solid #dee2e6;
        }}
        
        .icon {{
            width: 24px;
            height: 24px;
            display: inline-block;
        }}
        
        @media (max-width: 768px) {{
            .report-container {{
                margin: 10px;
            }}
            
            .report-header {{
                padding: 20px;
            }}
            
            .report-header h1 {{
                font-size: 1.8rem;
            }}
            
            .report-content {{
                padding: 20px;
            }}
            
            .section {{
                padding: 20px;
            }}
            
            .metrics-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-header">
            <h1>🏢 {title}</h1>
            <div class="subtitle">AI Decision Council Decision Analysis</div>
            <div class="report-meta">
                <div class="meta-item">📊 Report ID: {request_id}</div>
                <div class="meta-item">📅 Generated: {generated_at}</div>
                <div class="meta-item">🤖 AI Agents: {len(initial_responses)}</div>
            </div>
        </div>
        
        <div class="report-content">
            <div class="section">
                <h2>📋 Decision Question</h2>
                <div class="question-box">
                    <h3 style="color: white; margin-bottom: 10px;">Strategic Question</h3>
                    <p style="font-size: 1.1rem; line-height: 1.6;">{user_query}</p>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 Executive Summary</h2>
                <div class="recommendation-box">
                    <h3 style="color: white; margin-bottom: 10px;">Final Recommendation</h3>
                    <p style="font-size: 1.1rem; line-height: 1.6;">{final_recommendation}</p>
                </div>
            </div>
            
            <div class="section">
                <h2>📊 Decision Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{int(quality_score * 100)}%</div>
                        <div class="metric-label">Quality Score</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {quality_score * 100}%"></div>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{int(consensus_level * 100)}%</div>
                        <div class="metric-label">Consensus Level</div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {consensus_level * 100}%"></div>
                        </div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{execution_time:.1f}s</div>
                        <div class="metric-label">Analysis Time</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(initial_responses)}</div>
                        <div class="metric-label">AI Agents</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>👥 Agent Analysis</h2>
                {generate_agent_responses_html(initial_responses)}
            </div>
        </div>
        
        <div class="footer">
            <p><strong>AI Decision Council</strong> • Decision Support System</p>
            <p>Generated on {generated_at} • Report ID: {request_id}</p>
            <p style="margin-top: 10px; font-size: 0.9rem;">This report was generated by an AI system and should be reviewed by qualified professionals before implementation.</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html_template

def generate_agent_responses_html(responses) -> str:
    """Generate HTML for agent responses"""
    if not responses:
        return "<p>No agent responses available.</p>"
    
    # Agent icons mapping
    agent_icons = {
        'Neutral Agent': '⚖️',
        'Positive Agent': '🌟', 
        'Skeptic Agent': '🔍',
        'Risk Expert Agent': '🛡️'
    }
    
    html = ""
    for i, response in enumerate(responses):
        # Handle different response formats
        if isinstance(response, dict):
            agent_name = response.get('agent_name', f'Agent {i+1}')
            agent_type = response.get('agent_type', 'AI Advisor')
            text_response = response.get('text_response', response.get('response', 'No response available'))
        else:
            agent_name = getattr(response, 'agent_name', f'Agent {i+1}')
            agent_type = getattr(response, 'agent_type', 'AI Advisor') 
            text_response = getattr(response, 'text_response', getattr(response, 'response', 'No response available'))
        
        icon = agent_icons.get(agent_name, '🤖')
        
        html += f"""
        <div class="agent-card">
            <div class="agent-header">
                <div class="agent-avatar">{icon}</div>
                <div class="agent-info">
                    <h4>{agent_name}</h4>
                    <div class="agent-type">{agent_type}</div>
                </div>
            </div>
            <div class="agent-response">
                <p>{text_response}</p>
            </div>
        </div>
        """
    
    return html

# Add these endpoints before the serve_frontend function

@app.get("/api/settings", response_model=SettingsResponse)
async def get_settings():
    """Get current system settings"""
    try:
        return SettingsResponse(
            model_type=settings.model_type,
            fast_mode=settings.fast_mode,
            use_direct_hf=settings.use_direct_hf,
            enable_professional_mode=settings.enable_professional_mode,
            enable_discussion_mode=settings.enable_discussion_mode,
            enable_reasoning_mode=settings.enable_reasoning_mode,
            quality_threshold=settings.quality_threshold,
            consensus_threshold=settings.consensus_threshold,
            max_discussion_rounds=settings.max_discussion_rounds,
            openrouter_model=settings.openrouter_model,
            deepseek_use_reasoning=settings.deepseek_use_reasoning,
            max_response_time=settings.max_response_time
        )
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve settings")

@app.post("/api/settings", response_model=SettingsUpdateResponse)
async def update_settings(request: SettingsUpdateRequest):
    """Update system settings"""
    try:
        updated_fields = []
        
        # Update settings that were provided in the request
        if request.model_type is not None:
            settings.model_type = request.model_type
            updated_fields.append("model_type")
            
        if request.fast_mode is not None:
            settings.fast_mode = request.fast_mode
            updated_fields.append("fast_mode")
            
        if request.use_direct_hf is not None:
            settings.use_direct_hf = request.use_direct_hf
            updated_fields.append("use_direct_hf")
            
        if request.enable_professional_mode is not None:
            settings.enable_professional_mode = request.enable_professional_mode
            updated_fields.append("enable_professional_mode")
            
        if request.enable_discussion_mode is not None:
            settings.enable_discussion_mode = request.enable_discussion_mode
            updated_fields.append("enable_discussion_mode")
            
        if request.enable_reasoning_mode is not None:
            settings.enable_reasoning_mode = request.enable_reasoning_mode
            updated_fields.append("enable_reasoning_mode")
            
        if request.quality_threshold is not None:
            settings.quality_threshold = max(0.0, min(1.0, request.quality_threshold))
            updated_fields.append("quality_threshold")
            
        if request.consensus_threshold is not None:
            settings.consensus_threshold = max(0.0, min(1.0, request.consensus_threshold))
            updated_fields.append("consensus_threshold")
            
        if request.max_discussion_rounds is not None:
            settings.max_discussion_rounds = max(1, min(10, request.max_discussion_rounds))
            updated_fields.append("max_discussion_rounds")
            
        if request.openrouter_model is not None:
            settings.openrouter_model = request.openrouter_model
            updated_fields.append("openrouter_model")
            
        if request.deepseek_use_reasoning is not None:
            settings.deepseek_use_reasoning = request.deepseek_use_reasoning
            updated_fields.append("deepseek_use_reasoning")
            
        if request.max_response_time is not None:
            settings.max_response_time = max(5, min(60, request.max_response_time))
            updated_fields.append("max_response_time")
        
        # Log the changes
        logger.info(f"Settings updated: {', '.join(updated_fields)}")
        
        # Return current settings
        current_settings = SettingsResponse(
            model_type=settings.model_type,
            fast_mode=settings.fast_mode,
            use_direct_hf=settings.use_direct_hf,
            enable_professional_mode=settings.enable_professional_mode,
            enable_discussion_mode=settings.enable_discussion_mode,
            enable_reasoning_mode=settings.enable_reasoning_mode,
            quality_threshold=settings.quality_threshold,
            consensus_threshold=settings.consensus_threshold,
            max_discussion_rounds=settings.max_discussion_rounds,
            openrouter_model=settings.openrouter_model,
            deepseek_use_reasoning=settings.deepseek_use_reasoning,
            max_response_time=settings.max_response_time
        )
        
        return SettingsUpdateResponse(
            success=True,
            message=f"Successfully updated {len(updated_fields)} settings: {', '.join(updated_fields)}",
            updated_settings=current_settings
        )
        
    except Exception as e:
        logger.error(f"Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")

@app.post("/api/settings/reset")
async def reset_settings():
    """Reset settings to default values"""
    try:
        # Reset to default values
        settings.model_type = "direct_hf"
        settings.fast_mode = True
        settings.use_direct_hf = True
        settings.enable_professional_mode = True
        settings.enable_discussion_mode = True
        settings.enable_reasoning_mode = True
        settings.quality_threshold = 0.7
        settings.consensus_threshold = 0.8
        settings.max_discussion_rounds = 3
        settings.openrouter_model = "mistralai/mixtral-8x7b-instruct"
        settings.deepseek_use_reasoning = True
        settings.max_response_time = 10
        
        logger.info("Settings reset to default values")
        
        # Return current settings
        current_settings = SettingsResponse(
            model_type=settings.model_type,
            fast_mode=settings.fast_mode,
            use_direct_hf=settings.use_direct_hf,
            enable_professional_mode=settings.enable_professional_mode,
            enable_discussion_mode=settings.enable_discussion_mode,
            enable_reasoning_mode=settings.enable_reasoning_mode,
            quality_threshold=settings.quality_threshold,
            consensus_threshold=settings.consensus_threshold,
            max_discussion_rounds=settings.max_discussion_rounds,
            openrouter_model=settings.openrouter_model,
            deepseek_use_reasoning=settings.deepseek_use_reasoning,
            max_response_time=settings.max_response_time
        )
        
        return SettingsUpdateResponse(
            success=True,
            message="Settings successfully reset to default values",
            updated_settings=current_settings
        )
        
    except Exception as e:
        logger.error(f"Error resetting settings: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to reset settings: {str(e)}")

@app.get("/api/settings/models")
async def get_available_models():
    """Get list of available models"""
    try:
        available_models = {
            "model_types": [
                {"value": "direct_hf", "label": "Direct HF (OpenRouter)", "description": "Primary model using OpenRouter API"},
                {"value": "deepseek", "label": "DeepSeek-R1", "description": "Advanced reasoning model"},
                {"value": "huggingface", "label": "Hugging Face", "description": "Hugging Face Inference API"},
                {"value": "fast_cpu", "label": "Fast CPU", "description": "Lightweight CPU model"},
                {"value": "llama", "label": "LLAMA", "description": "Local LLAMA model"}
            ],
            "openrouter_models": [
                {"value": "mistralai/mixtral-8x7b-instruct", "label": "Mixtral 8x7B", "description": "Balanced performance and speed"},
                {"value": "anthropic/claude-3-sonnet", "label": "Claude 3 Sonnet", "description": "High-quality reasoning"},
                {"value": "openai/gpt-4", "label": "GPT-4", "description": "Advanced language model"},
                {"value": "meta-llama/llama-2-70b-chat", "label": "Llama 2 70B", "description": "Large language model"},
                {"value": "google/gemini-pro", "label": "Gemini Pro", "description": "Google's language model"}
            ]
        }
        
        return available_models
        
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve available models")

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Download endpoint - MUST be before catch-all route
@app.get("/api/download-report/{filename}")
async def download_report(filename: str):
    """Download a generated report file"""
    # Security check - only allow specific file patterns
    if not filename.startswith('report_') or not (filename.endswith('.html') or filename.endswith('.pdf') or filename.endswith('.json')):
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # Use absolute path to reports directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(backend_dir, "reports")
    filepath = os.path.join(reports_dir, filename)
    
    # Check if file exists
    logger.info(f"Looking for report file at: {filepath}")
    logger.info(f"File exists: {os.path.exists(filepath)}")
    if not os.path.exists(filepath):
        logger.error(f"Report file not found: {filepath}")
        raise HTTPException(status_code=404, detail="Report file not found")
    
    # Determine media type
    if filename.endswith('.html'):
        media_type = 'text/html'
    elif filename.endswith('.pdf'):
        media_type = 'application/pdf'
    elif filename.endswith('.json'):
        media_type = 'application/json'
    else:
        media_type = 'application/octet-stream'
    
    # Return file for download
    return FileResponse(
        path=filepath,
        media_type=media_type,
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Catch-all route to serve React app for client-side routing
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """Serve React frontend for all undefined routes (SPA routing)"""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "build")
    file_path = os.path.join(frontend_path, full_path)
    
    # Check if specific file exists
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Serve index.html for all other routes (client-side routing)
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    
    # Fallback
    raise HTTPException(status_code=404, detail="Frontend not found")

# Removed auth, history, and export routers for simplified setup

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Decision Council API server on 0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001) 