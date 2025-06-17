import os
from typing import Dict, List, Optional, TypedDict, Annotated, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
# TAVILY removed - web search disabled
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import json
import asyncio
from datetime import datetime
import logging
from dataclasses import dataclass

# Import professional decision-making components
try:
    from agents.decision_framework import ProfessionalDecisionFramework, ProfessionalDecision
    from agents.consensus_manager import ProfessionalConsensusManager, ConsensusResult
    from agents.executive_reporter import ProfessionalExecutiveReporter, ExecutiveReport
    PROFESSIONAL_COMPONENTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Professional components not available: {e}")
    PROFESSIONAL_COMPONENTS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config
try:
    from config import settings
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    logger.warning("Config not available, using environment variables directly")

class AgentState(TypedDict):
    """State schema for the agent orchestration workflow"""
    user_query: str
    initial_responses: List[Dict[str, Any]]
    discussion_rounds: List[List[Dict[str, Any]]]
    consensus_attempts: List[Dict[str, Any]]
    final_recommendation: Optional[str]
    quality_scores: Dict[str, float]
    context_retrieved: List[str]
    external_data: List[Dict[str, Any]]
    workflow_metadata: Dict[str, Any]
    current_round: int
    max_rounds: int
    consensus_threshold: float
    agents_data: List[Dict[str, Any]]

@dataclass
class WorkflowConfig:
    """Configuration for the orchestration workflow"""
    max_discussion_rounds: int = 3
    consensus_threshold: float = 0.8
    quality_threshold: float = 0.7
    enable_web_search: bool = True
    enable_context_retrieval: bool = False
    enable_performance_monitoring: bool = True

class LangGraphOrchestrator:
    """Advanced orchestration system using LangGraph for managing agent workflows"""
    
    def __init__(self, agents: List[Any], config: WorkflowConfig = None):
        self.agents = agents
        self.config = config or WorkflowConfig()
        self.memory = MemorySaver()
        self.search_tool = None
        self.workflow = None
        
        # Initialize professional decision-making components
        if PROFESSIONAL_COMPONENTS_AVAILABLE:
            self.decision_framework = ProfessionalDecisionFramework()
            self.consensus_manager = ProfessionalConsensusManager()
            self.executive_reporter = ProfessionalExecutiveReporter()
            logger.info("Professional decision-making components initialized")
        else:
            self.decision_framework = None
            self.consensus_manager = None
            self.executive_reporter = None
            
        self.setup_tools()
        self.setup_workflow()
        
        self.max_quality_retries = 2
        
    def setup_tools(self):
        """Initialize external tools for enhanced agent capabilities"""
        # Web search disabled - TAVILY removed
        self.config.enable_web_search = False
        self.search_tool = None
        logger.info("Web search functionality disabled (TAVILY removed)")
                
    def setup_workflow(self):
        """Create the LangGraph workflow with conditional routing"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each stage of the debate
        workflow.add_node("initialize", self.initialize_debate)
        workflow.add_node("gather_initial_responses", self.gather_initial_responses)
        workflow.add_node("evaluate_quality", self.evaluate_response_quality)
        workflow.add_node("retrieve_context", self.retrieve_external_context)
        workflow.add_node("facilitate_discussion", self.facilitate_discussion_round)
        workflow.add_node("assess_convergence", self.assess_convergence)
        workflow.add_node("build_consensus", self.build_consensus)
        workflow.add_node("generate_final_recommendation", self.generate_final_recommendation)
        workflow.add_node("emergency_fallback", self.emergency_fallback)
        
        # Define the workflow edges with conditional routing
        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "gather_initial_responses")
        workflow.add_edge("gather_initial_responses", "evaluate_quality")
        
        # Conditional routing based on quality assessment
        workflow.add_conditional_edges(
            "evaluate_quality",
            self.quality_routing_decision,
            {
                "proceed": "retrieve_context",
                "improve": "gather_initial_responses",
                "fallback": "emergency_fallback"
            }
        )
        
        workflow.add_edge("retrieve_context", "facilitate_discussion")
        
        # Conditional routing for discussion continuation
        workflow.add_conditional_edges(
            "facilitate_discussion",
            self.discussion_routing_decision,
            {
                "continue": "assess_convergence",
                "consensus": "build_consensus",
                "max_rounds": "build_consensus"
            }
        )
        
        workflow.add_conditional_edges(
            "assess_convergence",
            self.convergence_routing_decision,
            {
                "converged": "build_consensus",
                "continue": "facilitate_discussion",
                "diverged": "emergency_fallback"
            }
        )
        
        workflow.add_edge("build_consensus", "generate_final_recommendation")
        workflow.add_edge("generate_final_recommendation", END)
        workflow.add_edge("emergency_fallback", END)
        
        self.workflow = workflow.compile(checkpointer=self.memory)
        
    async def orchestrate_debate(self, user_query: str, thread_id: str = None) -> Dict[str, Any]:
        """Main orchestration method that runs the complete debate workflow"""
        if not thread_id:
            thread_id = f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        # Initialize state
        initial_state = AgentState(
            user_query=user_query,
            initial_responses=[],
            discussion_rounds=[],
            consensus_attempts=[],
            final_recommendation=None,
            quality_scores={},
            context_retrieved=[],
            external_data=[],
            workflow_metadata={
                "start_time": datetime.now().isoformat(),
                "thread_id": thread_id,
                "config": self.config.__dict__,
                "quality_retries": 0,
            },
            current_round=0,
            max_rounds=self.config.max_discussion_rounds,
            consensus_threshold=self.config.consensus_threshold,
            agents_data=[{"name": agent.agent_name, "role": getattr(agent, 'role', 'advisor')} for agent in self.agents]
        )
        
        try:
            # Run the workflow
            config = {"configurable": {"thread_id": thread_id}}
            final_state = await self.workflow.ainvoke(initial_state, config)
            
            # Add performance metrics
            final_state["workflow_metadata"]["end_time"] = datetime.now().isoformat()
            final_state["workflow_metadata"]["total_rounds"] = final_state["current_round"]
            
            return final_state
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return self.create_error_response(user_query, str(e))
            
    async def initialize_debate(self, state: AgentState) -> AgentState:
        """Initialize the debate with context analysis"""
        logger.info(f"Initializing debate for query: {state['user_query'][:100]}...")
        
        # Analyze query complexity and domain
        query_analysis = self.analyze_query_complexity(state['user_query'])
        state['workflow_metadata']['query_analysis'] = query_analysis
        
        # Adjust workflow parameters based on complexity
        if query_analysis['complexity'] == 'high':
            state['max_rounds'] = min(self.config.max_discussion_rounds + 1, 5)
            state['consensus_threshold'] = 0.75
        elif query_analysis['complexity'] == 'low':
            state['max_rounds'] = max(self.config.max_discussion_rounds - 1, 1)
            state['consensus_threshold'] = 0.85
            
        return state
        
    async def gather_initial_responses(self, state: AgentState) -> AgentState:
        """Gather initial responses from all agents"""
        logger.info("Gathering initial responses from agents...")
        
        responses = []
        for agent in self.agents:
            try:
                response = agent.generate_response(state['user_query'])
                responses.append({
                    'agent_name': agent.agent_name,
                    'text_response': response,
                    'timestamp': datetime.now().isoformat(),
                    'word_count': len(response.split()),
                    'sentiment': self.analyze_sentiment(response)
                })
            except Exception as e:
                logger.error(f"Failed to get response from {agent.agent_name}: {e}")
                responses.append({
                    'agent_name': agent.agent_name,
                    'text_response': f"Error generating response: {str(e)}",
                    'timestamp': datetime.now().isoformat(),
                    'word_count': 0,
                    'sentiment': 'neutral'
                })
                
        state['initial_responses'] = responses
        logger.info(f"Gathered {len(responses)} initial responses.")
        return state
        
    async def evaluate_response_quality(self, state: AgentState) -> AgentState:
        """Evaluate the quality of initial responses"""
        logger.info("Evaluating response quality...")
        
        quality_scores = {}
        for response in state['initial_responses']:
            score = self.calculate_response_quality(response['text_response'], state['user_query'])
            quality_scores[response['agent_name']] = score
            
        state['quality_scores'] = quality_scores
        
        # Calculate overall quality
        avg_quality = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0
        state['workflow_metadata']['average_quality'] = avg_quality
        
        return state
        
    async def retrieve_external_context(self, state: AgentState) -> AgentState:
        """Retrieve external context using web search and other sources"""
        # External context retrieval disabled - TAVILY removed
        logger.info("External context retrieval disabled (TAVILY removed)")
        return state
        
    async def facilitate_discussion_round(self, state: AgentState) -> AgentState:
        """Facilitate a round of discussion between agents"""
        state['current_round'] += 1
        logger.info(f"Facilitating discussion round {state['current_round']}")
        
        # Prepare discussion context
        if state['current_round'] == 1:
            discussion_context = state['initial_responses']
        else:
            discussion_context = state['discussion_rounds'][-1] if state['discussion_rounds'] else state['initial_responses']
            
        round_discussions = []
        for agent in self.agents:
            try:
                # Get other agents' opinions for this agent to discuss
                other_opinions = [resp for resp in discussion_context if resp['agent_name'] != agent.agent_name]
                
                discussion = agent.discuss_with_peers(state['user_query'], other_opinions)
                round_discussions.append({
                    'agent_name': agent.agent_name,
                    'discussion': discussion,
                    'round': state['current_round'],
                    'timestamp': datetime.now().isoformat(),
                    'references': self.extract_references(discussion, other_opinions)
                })
            except Exception as e:
                logger.error(f"Failed to get discussion from {agent.agent_name}: {e}")
                
        state['discussion_rounds'].append(round_discussions)
        return state
        
    async def assess_convergence(self, state: AgentState) -> AgentState:
        """Assess whether agents are converging toward consensus"""
        logger.info("Assessing convergence...")
        
        if len(state['discussion_rounds']) < 2:
            state['workflow_metadata']['convergence_score'] = 0.0
            return state
            
        # Calculate convergence based on similarity of recent discussions
        current_round = state['discussion_rounds'][-1]
        previous_round = state['discussion_rounds'][-2]
        
        convergence_score = self.calculate_convergence_score(current_round, previous_round)
        state['workflow_metadata']['convergence_score'] = convergence_score
        
        return state
        
    async def build_consensus(self, state: AgentState) -> AgentState:
        """Build consensus from agent discussions"""
        logger.info("Building consensus...")
        
        consensus_contributions = []
        for agent in self.agents:
            try:
                contribution = agent.contribute_to_consensus(
                    state['user_query'], 
                    [item for round_data in state['discussion_rounds'] for item in round_data]
                )
                consensus_contributions.append({
                    'agent_name': agent.agent_name,
                    'contribution': contribution,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                logger.error(f"Failed to get consensus from {agent.agent_name}: {e}")
                
        state['consensus_attempts'].append(consensus_contributions)
        return state
        
    async def generate_final_recommendation(self, state: AgentState) -> AgentState:
        """Generate the final professional recommendation using advanced frameworks"""
        logger.info("Generating final professional recommendation...")
        
        if self.decision_framework and self.consensus_manager and self.executive_reporter:
            # Use professional decision-making framework
            try:
                # Generate professional decision
                professional_decision = self.decision_framework.generate_professional_recommendation(
                    state["user_query"],
                    state["initial_responses"],
                    [round_data for round_data in state["discussion_rounds"]]
                )
                
                # Build professional consensus
                consensus_result = self.consensus_manager.build_professional_consensus(
                    state["user_query"],
                    self.agents,
                    state["initial_responses"],
                    [round_data for round_data in state["discussion_rounds"]],
                    [alt.name for alt in professional_decision.alternatives]
                )
                
                # Generate executive report
                executive_report = self.executive_reporter.generate_executive_report(
                    professional_decision,
                    consensus_result,
                    state["initial_responses"],
                    [round_data for round_data in state["discussion_rounds"]],
                    state["user_query"]
                )
                
                # Create comprehensive recommendation
                recommendation = self.create_professional_recommendation(
                    professional_decision, 
                    consensus_result, 
                    executive_report
                )
                
                # Store professional analysis results
                state["professional_decision"] = professional_decision
                state["consensus_result"] = consensus_result
                state["executive_report"] = executive_report
                
                logger.info("Professional recommendation generated successfully")
                
            except Exception as e:
                logger.error(f"Error in professional recommendation generation: {e}")
                # Fallback to standard recommendation
                recommendation = self.synthesize_final_recommendation(state)
        else:
            # Standard recommendation synthesis
            recommendation = self.synthesize_final_recommendation(state)
        
        state['final_recommendation'] = recommendation
        
        # Add workflow completion metadata
        state['workflow_metadata']['completion_status'] = 'success'
        state['workflow_metadata']['final_quality_score'] = self.calculate_final_quality_score(state)
        
        return state
        
    async def emergency_fallback(self, state: AgentState) -> AgentState:
        """Emergency fallback when normal workflow fails"""
        logger.warning("Executing emergency fallback...")
        
        # Generate a basic recommendation using available data
        fallback_recommendation = self.generate_fallback_recommendation(state)
        state['final_recommendation'] = fallback_recommendation
        state['workflow_metadata']['completion_status'] = 'fallback'
        
        return state
        
    # Routing decision methods
    def quality_routing_decision(self, state: AgentState) -> str:
        """Determines routing based on response quality."""
        
        avg_quality = state.get('avg_quality_score', 0)
        retries = state['workflow_metadata'].get('quality_retries', 0)
        
        logger.info(f"Quality routing: Avg score={avg_quality:.2f}, Retries={retries}")
        
        if avg_quality >= self.config.quality_threshold:
            return "proceed"
            
        if retries < self.max_quality_retries:
            state['workflow_metadata']['quality_retries'] = retries + 1
            logger.warning(f"Response quality low. Retrying ({retries + 1}/{self.max_quality_retries})...")
            return "improve"
            
        logger.error("Max quality retries reached. Proceeding with low-quality responses.")
        return "proceed" # Changed from 'fallback' to allow process to continue
            
    def discussion_routing_decision(self, state: AgentState) -> str:
        """Determines whether to continue discussion or move to consensus."""
        if state['current_round'] >= state['max_rounds']:
            return "max_rounds"
            
        convergence_score = state['workflow_metadata'].get('convergence_score', 0)
        if convergence_score >= state['consensus_threshold']:
            return "consensus"
            
        return "continue"
        
    def convergence_routing_decision(self, state: AgentState) -> str:
        """Decide based on convergence assessment"""
        convergence_score = state['workflow_metadata'].get('convergence_score', 0)
        
        if convergence_score >= state['consensus_threshold']:
            return "converged"
        elif convergence_score < 0.2:  # Highly divergent
            return "diverged"
        else:
            return "continue"
            
    # Helper methods
    def analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """Analyze query complexity and domain"""
        word_count = len(query.split())
        question_marks = query.count('?')
        
        # Simple complexity analysis
        if word_count > 50 or question_marks > 2:
            complexity = 'high'
        elif word_count > 20 or question_marks > 1:
            complexity = 'medium'
        else:
            complexity = 'low'
            
        return {
            'complexity': complexity,
            'word_count': word_count,
            'question_count': question_marks,
            'estimated_domain': self.estimate_domain(query)
        }
        
    def estimate_domain(self, query: str) -> str:
        """Estimate the domain of the query"""
        query_lower = query.lower()
        
        domains = {
            'financial': ['money', 'invest', 'finance', 'budget', 'cost', 'price', 'profit', 'loan'],
            'technical': ['software', 'code', 'tech', 'algorithm', 'system', 'database', 'api'],
            'career': ['job', 'work', 'career', 'salary', 'interview', 'resume', 'promotion'],
            'health': ['health', 'medical', 'doctor', 'treatment', 'exercise', 'diet'],
            'relationship': ['relationship', 'dating', 'marriage', 'family', 'friend']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
                
        return 'general'
        
    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ['good', 'great', 'excellent', 'positive', 'beneficial', 'advantage']
        negative_words = ['bad', 'poor', 'negative', 'risk', 'problem', 'issue', 'concern']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
            
    def calculate_response_quality(self, response: str, query: str) -> float:
        """Calculate quality score for a response"""
        if not response or len(response.strip()) < 10:
            return 0.0
            
        # Basic quality metrics
        word_count = len(response.split())
        
        # Quality factors
        length_score = min(word_count / 100, 1.0)  # Normalize to 0-1
        relevance_score = self.calculate_relevance(response, query)
        structure_score = self.calculate_structure_score(response)
        
        return (length_score * 0.3 + relevance_score * 0.5 + structure_score * 0.2)
        
    def calculate_relevance(self, response: str, query: str) -> float:
        """Calculate relevance between response and query"""
        response_words = set(response.lower().split())
        query_words = set(query.lower().split())
        
        if not query_words:
            return 0.0
            
        overlap = len(response_words.intersection(query_words))
        return min(overlap / len(query_words), 1.0)
        
    def calculate_structure_score(self, response: str) -> float:
        """Calculate structural quality of response"""
        sentences = response.split('.')
        has_structure = len(sentences) > 2
        has_punctuation = any(p in response for p in ['.', '!', '?', ','])
        
        score = 0.5  # Base score
        if has_structure:
            score += 0.3
        if has_punctuation:
            score += 0.2
            
        return min(score, 1.0)
        
    def calculate_convergence_score(self, current_round: List[Dict], previous_round: List[Dict]) -> float:
        """Calculate convergence score between discussion rounds"""
        if not current_round or not previous_round:
            return 0.0
            
        # Simple convergence based on similarity of discussion topics
        current_topics = self.extract_topics([d['discussion'] for d in current_round])
        previous_topics = self.extract_topics([d['discussion'] for d in previous_round])
        
        overlap = len(current_topics.intersection(previous_topics))
        total = len(current_topics.union(previous_topics))
        
        return overlap / total if total > 0 else 0.0
        
    def extract_topics(self, discussions: List[str]) -> set:
        """Extract key topics from discussions"""
        all_words = []
        for discussion in discussions:
            words = discussion.lower().split()
            # Filter out common words
            filtered_words = [w for w in words if len(w) > 4 and w not in ['should', 'would', 'could', 'might', 'think', 'consider']]
            all_words.extend(filtered_words)
            
        # Return most common words as topics
        from collections import Counter
        common_words = Counter(all_words).most_common(10)
        return set(word for word, count in common_words if count > 1)
        
    def extract_references(self, discussion: str, other_opinions: List[Dict]) -> List[str]:
        """Extract references to other agents in discussion"""
        references = []
        for opinion in other_opinions:
            agent_name = opinion['agent_name'].lower()
            if agent_name in discussion.lower():
                references.append(opinion['agent_name'])
        return references
        
    def synthesize_final_recommendation(self, state: AgentState) -> str:
        """Synthesize final recommendation from all state information"""
        if not state['consensus_attempts']:
            return "Unable to generate recommendation due to insufficient consensus data."
            
        # Combine all consensus contributions
        all_contributions = []
        for attempt in state['consensus_attempts']:
            for contribution in attempt:
                all_contributions.append(contribution['contribution'])
                
        # Create unified recommendation
        recommendation = f"""Based on comprehensive analysis and discussion among specialized agents, here is the unified recommendation:

EXECUTIVE SUMMARY:
{self.create_executive_summary(state)}

DETAILED RECOMMENDATION:
{self.combine_contributions(all_contributions)}

CONFIDENCE LEVEL: {self.calculate_confidence_level(state):.1%}

SUPPORTING EVIDENCE:
{self.format_supporting_evidence(state)}

NEXT STEPS:
{self.generate_next_steps(state)}
"""
        return recommendation
    
    def create_professional_recommendation(self, decision: 'ProfessionalDecision', 
                                         consensus: 'ConsensusResult', 
                                         executive_report: 'ExecutiveReport') -> str:
        """Create professional recommendation from all components"""
        try:
            # Use the executive reporter to format the recommendation
            return self.executive_reporter.export_professional_report(executive_report)
        except Exception as e:
            logger.error(f"Error formatting professional report: {e}")
            # Fallback to basic professional format
            return f"""PROFESSIONAL DECISION ANALYSIS

RECOMMENDATION: {decision.recommended_alternative}
CONFIDENCE: {decision.confidence_level.value.replace('_', ' ').title()}
CONSENSUS STRENGTH: {consensus.consensus_strength:.1%}

FRAMEWORK USED: {decision.framework_used.value.upper()}
METHOD: {consensus.method_used.value.replace('_', ' ').title()}

REASONING:
{decision.reasoning}

IMPLEMENTATION STEPS:
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(decision.implementation_steps))}

RISK ANALYSIS:
{chr(10).join(f'• {risk["risk"]}: {risk["mitigation"]}' for risk in decision.risks_and_mitigations)}

QUALITY SCORE: {decision.quality_score:.2f}/1.0
"""
        
    def create_executive_summary(self, state: AgentState) -> str:
        """Create executive summary from state"""
        return f"After {state['current_round']} rounds of discussion among {len(state['agents_data'])} specialized agents, the council has reached a consensus with {state['workflow_metadata'].get('convergence_score', 0):.1%} agreement level."
        
    def combine_contributions(self, contributions: List[str]) -> str:
        """Combine consensus contributions into coherent recommendation"""
        if not contributions:
            return "No specific recommendations available."
            
        # Simple combination - in practice, this could be more sophisticated
        return "\n\n".join(f"• {contrib}" for contrib in contributions[:3])
        
    def calculate_confidence_level(self, state: AgentState) -> float:
        """Calculate overall confidence in the recommendation"""
        quality_score = state['workflow_metadata'].get('average_quality', 0)
        convergence_score = state['workflow_metadata'].get('convergence_score', 0)
        
        return (quality_score * 0.6 + convergence_score * 0.4)
        
    def format_supporting_evidence(self, state: AgentState) -> str:
        """Format supporting evidence from external sources"""
        evidence = []
        if state['external_data']:
            evidence.append(f"External research: {len(state['external_data'])} sources consulted")
        if state['context_retrieved']:
            evidence.append(f"Context analysis: {len(state['context_retrieved'])} data points")
            
        return "\n".join(evidence) if evidence else "Internal agent knowledge base"
        
    def generate_next_steps(self, state: AgentState) -> str:
        """Generate actionable next steps"""
        domain = state['workflow_metadata'].get('query_analysis', {}).get('estimated_domain', 'general')
        
        next_steps = {
            'financial': "1. Consult with a financial advisor\n2. Review current financial situation\n3. Create implementation timeline",
            'technical': "1. Prototype the solution\n2. Test with small dataset\n3. Scale gradually",
            'career': "1. Update resume/portfolio\n2. Network with industry contacts\n3. Set measurable goals",
            'general': "1. Create action plan\n2. Set timeline\n3. Monitor progress"
        }
        
        return next_steps.get(domain, next_steps['general'])
        
    def calculate_final_quality_score(self, state: AgentState) -> float:
        """Calculate final quality score for the entire workflow"""
        factors = [
            state['workflow_metadata'].get('average_quality', 0),
            state['workflow_metadata'].get('convergence_score', 0),
            min(state['current_round'] / state['max_rounds'], 1.0),  # Efficiency score
            1.0 if state['final_recommendation'] else 0.0  # Completion score
        ]
        
        return sum(factors) / len(factors)
        
    def generate_fallback_recommendation(self, state: AgentState) -> str:
        """Generate fallback recommendation when workflow fails"""
        return f"""Due to technical difficulties in the discussion process, here's a basic recommendation:

QUERY: {state['user_query']}

BASIC ANALYSIS:
Based on available initial responses from {len(state['initial_responses'])} agents, here are the key considerations:

{self.format_initial_responses(state['initial_responses'])}

RECOMMENDATION:
Given the complexity of your question, we recommend:
1. Gather more specific information about your situation
2. Consult with domain experts
3. Consider multiple perspectives before making a decision

Note: This is a simplified recommendation due to technical limitations in the full analysis process.
"""

    def format_initial_responses(self, responses: List[Dict]) -> str:
        """Format initial responses for fallback"""
        formatted = []
        for resp in responses[:3]:  # Limit to first 3
            formatted.append(f"• {resp['agent_name']}: {resp['text_response'][:100]}...")
        return "\n".join(formatted)
        
    def create_error_response(self, query: str, error: str) -> Dict[str, Any]:
        """Create error response when workflow completely fails"""
        return {
            'user_query': query,
            'final_recommendation': f"Error in processing: {error}",
            'workflow_metadata': {
                'completion_status': 'error',
                'error_message': error,
                'timestamp': datetime.now().isoformat()
            },
            'initial_responses': [],
            'discussion_rounds': [],
            'consensus_attempts': []
        } 