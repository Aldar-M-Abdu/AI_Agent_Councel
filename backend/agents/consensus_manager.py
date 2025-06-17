"""
Professional Consensus Management System
Implements formal consensus-building algorithms used in international decision-making bodies
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConsensusMethod(Enum):
    """Professional consensus building methods"""
    DELPHI = "delphi"  # Delphi Method - structured communication technique
    NOMINAL_GROUP = "nominal_group"  # Nominal Group Technique
    VOTING = "voting"  # Various voting methods
    WEIGHTED_SCORING = "weighted_scoring"  # Expert-weighted scoring
    MULTI_CRITERIA = "multi_criteria"  # Multi-criteria decision analysis
    STAKEHOLDER_ANALYSIS = "stakeholder_analysis"  # Stakeholder-based consensus

class VotingMethod(Enum):
    """Different voting methods for consensus"""
    SIMPLE_MAJORITY = "simple_majority"
    SUPERMAJORITY = "supermajority"  # 2/3 or 3/4 majority
    UNANIMOUS = "unanimous"
    WEIGHTED = "weighted"  # Expert-weighted voting
    RANKED_CHOICE = "ranked_choice"  # Ranked choice voting
    APPROVAL = "approval"  # Approval voting

@dataclass
class AgentVote:
    """Individual agent vote with confidence and reasoning"""
    agent_name: str
    agent_type: str
    vote: str  # The chosen alternative
    confidence: float  # 0.0 to 1.0
    reasoning: str
    weight: float = 1.0  # Agent's expertise weight
    vote_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ConsensusRound:
    """A single round of consensus building"""
    round_number: int
    method_used: ConsensusMethod
    votes: List[AgentVote]
    consensus_score: float  # 0.0 to 1.0
    convergence_metrics: Dict[str, float]
    round_summary: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class ConsensusResult:
    """Final consensus result with full documentation"""
    final_recommendation: str
    consensus_strength: float  # 0.0 to 1.0
    method_used: ConsensusMethod
    rounds_conducted: List[ConsensusRound]
    participating_agents: List[str]
    dissenting_opinions: List[Dict[str, Any]]
    confidence_interval: Tuple[float, float]
    quality_assessment: Dict[str, float]
    implementation_urgency: str
    follow_up_required: bool

class ProfessionalConsensusManager:
    """Professional consensus management system for AI agent councils"""
    
    def __init__(self, consensus_threshold: float = 0.75, max_rounds: int = 3):
        self.consensus_threshold = consensus_threshold
        self.max_rounds = max_rounds
        self.consensus_history: List[ConsensusResult] = []
        
    def determine_consensus_method(self, question: str, agent_count: int) -> ConsensusMethod:
        """Determine the best consensus method based on question type and agent count"""
        question_lower = question.lower()
        
        if agent_count <= 3:
            return ConsensusMethod.WEIGHTED_SCORING
        elif any(word in question_lower for word in ['complex', 'strategic', 'long-term']):
            return ConsensusMethod.DELPHI
        elif any(word in question_lower for word in ['urgent', 'quick', 'immediate']):
            return ConsensusMethod.VOTING
        elif any(word in question_lower for word in ['stakeholder', 'multiple parties', 'various interests']):
            return ConsensusMethod.STAKEHOLDER_ANALYSIS
        else:
            return ConsensusMethod.MULTI_CRITERIA
    
    def calculate_agent_weights(self, agents: List[Any], question: str) -> Dict[str, float]:
        """Calculate expertise weights for agents based on question domain"""
        weights = {}
        question_lower = question.lower()
        
        for agent in agents:
            agent_name = agent.agent_name
            agent_type = getattr(agent, 'agent_type', 'General Advisor')
            
            # Base weight
            base_weight = 1.0
            
            # Adjust based on question domain and agent expertise
            if any(word in question_lower for word in ['risk', 'danger', 'safety']) and 'risk' in agent_type.lower():
                base_weight = 1.5
            elif any(word in question_lower for word in ['financial', 'invest', 'money']) and 'financial' in agent_type.lower():
                base_weight = 1.3
            elif any(word in question_lower for word in ['neutral', 'balanced', 'objective']) and 'neutral' in agent_name.lower():
                base_weight = 1.2
            elif 'skeptic' in agent_name.lower():
                base_weight = 1.1  # Skeptics provide valuable contrarian views
                
            weights[agent_name] = base_weight
            
        # Normalize weights so they sum to the number of agents
        total_weight = sum(weights.values())
        agent_count = len(agents)
        for agent_name in weights:
            weights[agent_name] = (weights[agent_name] / total_weight) * agent_count
            
        return weights
    
    def extract_agent_votes(self, agent_responses: List[Dict[str, Any]], 
                          alternatives: List[str], 
                          agent_weights: Dict[str, float]) -> List[AgentVote]:
        """Extract votes from agent responses"""
        votes = []
        
        for response in agent_responses:
            agent_name = response['agent_name']
            agent_type = response.get('agent_type', 'Advisor')
            text_response = response['text_response']
            
            # Analyze response to determine preferred alternative
            vote = self.determine_agent_preference(text_response, alternatives)
            confidence = self.calculate_response_confidence(text_response)
            weight = agent_weights.get(agent_name, 1.0)
            
            votes.append(AgentVote(
                agent_name=agent_name,
                agent_type=agent_type,
                vote=vote,
                confidence=confidence,
                reasoning=text_response[:200] + "..." if len(text_response) > 200 else text_response,
                weight=weight
            ))
            
        return votes
    
    def determine_agent_preference(self, response_text: str, alternatives: List[str]) -> str:
        """Determine which alternative the agent prefers based on their response"""
        response_lower = response_text.lower()
        
        # Look for explicit preferences
        if any(word in response_lower for word in ['recommend', 'suggest', 'advise', 'should']):
            if any(word in response_lower for word in ['proceed', 'go ahead', 'move forward', 'yes']):
                return "Proceed"
            elif any(word in response_lower for word in ['wait', 'delay', 'postpone', 'more information']):
                return "Wait"
            elif any(word in response_lower for word in ['modify', 'adjust', 'change', 'adapt']):
                return "Modify"
            elif any(word in response_lower for word in ['avoid', 'decline', 'no', 'against']):
                return "Decline"
                
        # Default to balanced/conservative approach for neutral responses
        if any(word in response_lower for word in ['balanced', 'moderate', 'careful', 'cautious']):
            return "Balanced Approach"
        elif any(word in response_lower for word in ['conservative', 'safe', 'low-risk']):
            return "Conservative Approach"
        elif any(word in response_lower for word in ['aggressive', 'bold', 'high-risk']):
            return "Aggressive Approach"
            
        # If no clear preference, default to first alternative or "Balanced Approach"
        return alternatives[0] if alternatives else "Balanced Approach"
    
    def calculate_response_confidence(self, response_text: str) -> float:
        """Calculate confidence level based on response certainty indicators"""
        response_lower = response_text.lower()
        confidence = 0.5  # Base confidence
        
        # Increase confidence for certain phrases
        if any(phrase in response_lower for phrase in ['strongly recommend', 'definitely', 'certainly', 'absolutely']):
            confidence += 0.3
        elif any(phrase in response_lower for phrase in ['recommend', 'suggest', 'should']):
            confidence += 0.2
        elif any(phrase in response_lower for phrase in ['might', 'could', 'possibly', 'perhaps', 'maybe']):
            confidence -= 0.2
        elif any(phrase in response_lower for phrase in ['uncertain', 'unsure', 'unclear', 'difficult to say']):
            confidence -= 0.3
            
        # Adjust based on evidence provided
        if any(phrase in response_lower for phrase in ['research shows', 'studies indicate', 'data suggests']):
            confidence += 0.1
        if any(phrase in response_lower for phrase in ['in my experience', 'based on analysis']):
            confidence += 0.1
            
        return max(0.1, min(1.0, confidence))
    
    def conduct_consensus_round(self, votes: List[AgentVote], method: ConsensusMethod, 
                              round_number: int) -> ConsensusRound:
        """Conduct a single round of consensus building"""
        
        if method == ConsensusMethod.WEIGHTED_SCORING:
            consensus_score = self.calculate_weighted_consensus(votes)
        elif method == ConsensusMethod.VOTING:
            consensus_score = self.calculate_voting_consensus(votes)
        elif method == ConsensusMethod.DELPHI:
            consensus_score = self.calculate_delphi_consensus(votes, round_number)
        else:
            consensus_score = self.calculate_multi_criteria_consensus(votes)
            
        convergence_metrics = self.calculate_convergence_metrics(votes)
        round_summary = self.generate_round_summary(votes, consensus_score, method)
        
        return ConsensusRound(
            round_number=round_number,
            method_used=method,
            votes=votes,
            consensus_score=consensus_score,
            convergence_metrics=convergence_metrics,
            round_summary=round_summary
        )
    
    def calculate_weighted_consensus(self, votes: List[AgentVote]) -> float:
        """Calculate consensus using weighted voting"""
        if not votes:
            return 0.0
            
        # Group votes by preference
        vote_groups = {}
        total_weight = 0.0
        
        for vote in votes:
            preference = vote.vote
            weight = vote.weight * vote.confidence
            
            if preference not in vote_groups:
                vote_groups[preference] = 0.0
            vote_groups[preference] += weight
            total_weight += weight
            
        if total_weight == 0:
            return 0.0
            
        # Find the strongest preference
        max_support = max(vote_groups.values())
        consensus_strength = max_support / total_weight
        
        return consensus_strength
    
    def calculate_voting_consensus(self, votes: List[AgentVote]) -> float:
        """Calculate consensus using simple voting"""
        if not votes:
            return 0.0
            
        vote_counts = {}
        for vote in votes:
            preference = vote.vote
            if preference not in vote_counts:
                vote_counts[preference] = 0
            vote_counts[preference] += 1
            
        max_votes = max(vote_counts.values())
        consensus_strength = max_votes / len(votes)
        
        return consensus_strength
    
    def calculate_delphi_consensus(self, votes: List[AgentVote], round_number: int) -> float:
        """Calculate consensus using Delphi method principles"""
        # Delphi method emphasizes expert opinion convergence over rounds
        if not votes:
            return 0.0
            
        # Weight by both expertise and confidence
        weighted_consensus = self.calculate_weighted_consensus(votes)
        
        # Apply Delphi convergence factor (increases with rounds)
        convergence_factor = min(1.0, 0.5 + (round_number * 0.2))
        
        return weighted_consensus * convergence_factor
    
    def calculate_multi_criteria_consensus(self, votes: List[AgentVote]) -> float:
        """Calculate consensus using multi-criteria analysis"""
        if not votes:
            return 0.0
            
        # Consider both preference alignment and confidence levels
        preference_consensus = self.calculate_weighted_consensus(votes)
        
        # Calculate confidence alignment
        confidences = [vote.confidence for vote in votes]
        confidence_mean = np.mean(confidences)
        confidence_std = np.std(confidences)
        confidence_alignment = max(0.0, 1.0 - (confidence_std / confidence_mean)) if confidence_mean > 0 else 0.0
        
        # Combine preference and confidence consensus
        overall_consensus = (preference_consensus * 0.7) + (confidence_alignment * 0.3)
        
        return overall_consensus
    
    def calculate_convergence_metrics(self, votes: List[AgentVote]) -> Dict[str, float]:
        """Calculate various convergence metrics"""
        if not votes:
            return {}
            
        # Preference diversity (lower = more consensus)
        preferences = [vote.vote for vote in votes]
        unique_preferences = len(set(preferences))
        preference_diversity = unique_preferences / len(votes) if votes else 1.0
        
        # Confidence spread (lower = more consensus)
        confidences = [vote.confidence for vote in votes]
        confidence_spread = np.std(confidences) if len(confidences) > 1 else 0.0
        
        # Weight distribution (how evenly distributed are the expert weights)
        weights = [vote.weight for vote in votes]
        weight_entropy = self.calculate_entropy(weights)
        
        return {
            "preference_diversity": preference_diversity,
            "confidence_spread": confidence_spread,
            "weight_entropy": weight_entropy,
            "participation_rate": len(votes) / max(1, len(votes))  # Could be used with expected agent count
        }
    
    def calculate_entropy(self, values: List[float]) -> float:
        """Calculate entropy of a distribution"""
        if not values:
            return 0.0
            
        total = sum(values)
        if total == 0:
            return 0.0
            
        probabilities = [v / total for v in values]
        entropy = -sum(p * np.log2(p) for p in probabilities if p > 0)
        
        return entropy
    
    def generate_round_summary(self, votes: List[AgentVote], consensus_score: float, 
                             method: ConsensusMethod) -> str:
        """Generate a summary of the consensus round"""
        if not votes:
            return "No votes received."
            
        # Count preferences
        preference_counts = {}
        for vote in votes:
            pref = vote.vote
            if pref not in preference_counts:
                preference_counts[pref] = 0
            preference_counts[pref] += 1
            
        # Find most popular preference
        most_popular = max(preference_counts, key=preference_counts.get)
        support_count = preference_counts[most_popular]
        
        summary = f"Consensus Method: {method.value.title()}\n"
        summary += f"Consensus Strength: {consensus_score:.2f}\n"
        summary += f"Leading Preference: {most_popular} ({support_count}/{len(votes)} agents)\n"
        
        if len(preference_counts) > 1:
            summary += f"Alternative views: {len(preference_counts) - 1} different preferences\n"
            
        # Highlight high-confidence votes
        high_confidence_votes = [v for v in votes if v.confidence > 0.8]
        if high_confidence_votes:
            summary += f"High-confidence votes: {len(high_confidence_votes)}/{len(votes)}\n"
            
        return summary
    
    def build_professional_consensus(self, question: str, agents: List[Any], 
                                   agent_responses: List[Dict[str, Any]], 
                                   discussion_history: List[Dict[str, Any]],
                                   alternatives: List[str]) -> ConsensusResult:
        """Build professional consensus using structured methodology"""
        
        # Determine consensus method
        method = self.determine_consensus_method(question, len(agents))
        
        # Calculate agent weights
        agent_weights = self.calculate_agent_weights(agents, question)
        
        # Extract initial votes
        initial_votes = self.extract_agent_votes(agent_responses, alternatives, agent_weights)
        
        # Conduct consensus rounds
        rounds = []
        current_votes = initial_votes
        
        for round_num in range(1, self.max_rounds + 1):
            consensus_round = self.conduct_consensus_round(current_votes, method, round_num)
            rounds.append(consensus_round)
            
            # Check if consensus reached
            if consensus_round.consensus_score >= self.consensus_threshold:
                break
                
            # For multi-round methods, could update votes based on discussion
            # For now, we use the same votes across rounds
            
        # Determine final recommendation
        final_round = rounds[-1] if rounds else None
        final_recommendation = self.determine_final_recommendation(final_round, alternatives)
        
        # Calculate consensus strength
        consensus_strength = final_round.consensus_score if final_round else 0.0
        
        # Identify dissenting opinions
        dissenting_opinions = self.identify_dissenting_opinions(final_round, final_recommendation)
        
        # Quality assessment
        quality_assessment = self.assess_consensus_quality(rounds, len(agents))
        
        # Create consensus result
        result = ConsensusResult(
            final_recommendation=final_recommendation,
            consensus_strength=consensus_strength,
            method_used=method,
            rounds_conducted=rounds,
            participating_agents=[agent.agent_name for agent in agents],
            dissenting_opinions=dissenting_opinions,
            confidence_interval=self.calculate_confidence_interval(final_round),
            quality_assessment=quality_assessment,
            implementation_urgency=self.determine_implementation_urgency(consensus_strength, question),
            follow_up_required=consensus_strength < self.consensus_threshold
        )
        
        self.consensus_history.append(result)
        return result
    
    def determine_final_recommendation(self, final_round: Optional[ConsensusRound], 
                                     alternatives: List[str]) -> str:
        """Determine the final recommendation based on the consensus round"""
        if not final_round or not final_round.votes:
            return alternatives[0] if alternatives else "No recommendation possible"
            
        # Find the most supported alternative (weighted)
        preference_weights = {}
        for vote in final_round.votes:
            pref = vote.vote
            weight = vote.weight * vote.confidence
            
            if pref not in preference_weights:
                preference_weights[pref] = 0.0
            preference_weights[pref] += weight
            
        if preference_weights:
            return max(preference_weights, key=preference_weights.get)
        else:
            return alternatives[0] if alternatives else "No recommendation possible"
    
    def identify_dissenting_opinions(self, final_round: Optional[ConsensusRound], 
                                   final_recommendation: str) -> List[Dict[str, Any]]:
        """Identify agents with dissenting opinions"""
        if not final_round:
            return []
            
        dissenting = []
        for vote in final_round.votes:
            if vote.vote != final_recommendation:
                dissenting.append({
                    "agent_name": vote.agent_name,
                    "agent_type": vote.agent_type,
                    "preferred_alternative": vote.vote,
                    "confidence": vote.confidence,
                    "reasoning": vote.reasoning,
                    "weight": vote.weight
                })
                
        return dissenting
    
    def calculate_confidence_interval(self, final_round: Optional[ConsensusRound]) -> Tuple[float, float]:
        """Calculate confidence interval for the consensus"""
        if not final_round or not final_round.votes:
            return (0.0, 0.0)
            
        confidences = [vote.confidence for vote in final_round.votes]
        mean_confidence = np.mean(confidences)
        std_confidence = np.std(confidences)
        
        # 95% confidence interval
        margin = 1.96 * (std_confidence / np.sqrt(len(confidences)))
        
        lower_bound = max(0.0, mean_confidence - margin)
        upper_bound = min(1.0, mean_confidence + margin)
        
        return (lower_bound, upper_bound)
    
    def assess_consensus_quality(self, rounds: List[ConsensusRound], 
                               expected_agents: int) -> Dict[str, float]:
        """Assess the quality of the consensus process"""
        if not rounds:
            return {"overall_quality": 0.0}
            
        final_round = rounds[-1]
        
        # Participation quality
        participation_rate = len(final_round.votes) / max(1, expected_agents)
        
        # Convergence quality (did consensus improve over rounds?)
        if len(rounds) > 1:
            convergence_improvement = final_round.consensus_score - rounds[0].consensus_score
        else:
            convergence_improvement = 0.0
            
        # Confidence quality
        confidences = [vote.confidence for vote in final_round.votes]
        average_confidence = np.mean(confidences) if confidences else 0.0
        
        # Diversity quality (healthy debate vs groupthink)
        diversity_score = final_round.convergence_metrics.get("preference_diversity", 0.0)
        # Moderate diversity is good (not too high, not too low)
        optimal_diversity = 0.5
        diversity_quality = 1.0 - abs(diversity_score - optimal_diversity)
        
        # Overall quality score
        overall_quality = (
            participation_rate * 0.3 +
            final_round.consensus_score * 0.3 +
            average_confidence * 0.2 +
            diversity_quality * 0.1 +
            max(0, convergence_improvement) * 0.1
        )
        
        return {
            "overall_quality": overall_quality,
            "participation_rate": participation_rate,
            "consensus_strength": final_round.consensus_score,
            "average_confidence": average_confidence,
            "diversity_quality": diversity_quality,
            "convergence_improvement": convergence_improvement
        }
    
    def determine_implementation_urgency(self, consensus_strength: float, question: str) -> str:
        """Determine implementation urgency based on consensus and question type"""
        question_lower = question.lower()
        
        if consensus_strength >= 0.9:
            urgency = "High - Strong consensus achieved"
        elif consensus_strength >= 0.75:
            urgency = "Medium - Adequate consensus for proceeding"
        elif consensus_strength >= 0.6:
            urgency = "Low - Weak consensus, proceed with caution"
        else:
            urgency = "Very Low - Insufficient consensus, more analysis needed"
            
        # Adjust based on question urgency indicators
        if any(word in question_lower for word in ['urgent', 'immediate', 'asap', 'deadline']):
            if "Very Low" in urgency:
                urgency = "Medium - Despite weak consensus, urgency requires action"
            elif "Low" in urgency:
                urgency = "Medium - Urgency elevates implementation priority"
                
        return urgency
    
    def export_consensus_report(self, result: ConsensusResult) -> str:
        """Export consensus result as professional report"""
        report = f"""
PROFESSIONAL CONSENSUS ANALYSIS REPORT
======================================

Consensus Method: {result.method_used.value.upper()}
Final Recommendation: {result.final_recommendation}
Consensus Strength: {result.consensus_strength:.2f}/1.0
Confidence Interval: {result.confidence_interval[0]:.2f} - {result.confidence_interval[1]:.2f}

PARTICIPATING AGENTS
===================
"""
        for agent in result.participating_agents:
            report += f"• {agent}\n"
            
        report += f"\nCONSENSUS BUILDING PROCESS\n"
        report += f"=========================\n"
        report += f"Rounds Conducted: {len(result.rounds_conducted)}\n"
        
        for i, round_data in enumerate(result.rounds_conducted, 1):
            report += f"\nRound {i}:\n{round_data.round_summary}\n"
            
        if result.dissenting_opinions:
            report += f"\nDISSENTING OPINIONS\n"
            report += f"==================\n"
            for dissent in result.dissenting_opinions:
                report += f"Agent: {dissent['agent_name']}\n"
                report += f"Preferred: {dissent['preferred_alternative']}\n"
                report += f"Confidence: {dissent['confidence']:.2f}\n"
                report += f"Reasoning: {dissent['reasoning']}\n\n"
                
        report += f"QUALITY ASSESSMENT\n"
        report += f"==================\n"
        for metric, value in result.quality_assessment.items():
            report += f"{metric.replace('_', ' ').title()}: {value:.2f}\n"
            
        report += f"\nIMPLEMENTATION\n"
        report += f"=============\n"
        report += f"Urgency: {result.implementation_urgency}\n"
        report += f"Follow-up Required: {'Yes' if result.follow_up_required else 'No'}\n"
        
        return report 