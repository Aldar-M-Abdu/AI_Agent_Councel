"""
Professional Decision Framework for AI Agent Council
Implements structured decision-making methodologies used by international consulting firms
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DecisionFramework(Enum):
    """Standard decision-making frameworks used by professional consulting firms"""
    SWOT = "swot"  # Strengths, Weaknesses, Opportunities, Threats
    MECE = "mece"  # Mutually Exclusive, Collectively Exhaustive
    PROS_CONS = "pros_cons"  # Traditional Pros and Cons
    COST_BENEFIT = "cost_benefit"  # Cost-Benefit Analysis
    RISK_REWARD = "risk_reward"  # Risk-Reward Matrix
    DECISION_TREE = "decision_tree"  # Decision Tree Analysis
    STAKEHOLDER = "stakeholder"  # Stakeholder Analysis
    SCENARIO = "scenario"  # Scenario Planning
    PRIORITIZATION = "prioritization"  # Priority Matrix (Eisenhower Matrix)
    FEASIBILITY = "feasibility"  # Feasibility Analysis

class ConfidenceLevel(Enum):
    """Confidence levels for recommendations"""
    VERY_LOW = "very_low"
    LOW = "low"  
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class RecommendationPriority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"

@dataclass
class Evidence:
    """Structure for evidence supporting recommendations"""
    source: str
    type: str  # "research", "data", "expert_opinion", "case_study", "regulation"
    credibility: float  # 0.0 to 1.0
    relevance: float  # 0.0 to 1.0
    content: str
    url: Optional[str] = None
    date: Optional[str] = None

@dataclass
class Criterion:
    """Decision criteria with weights"""
    name: str
    weight: float  # 0.0 to 1.0
    description: str
    measurement: str  # How to measure this criterion

@dataclass
class Alternative:
    """Decision alternative with scoring"""
    name: str
    description: str
    scores: Dict[str, float] = field(default_factory=dict)  # criterion_name -> score
    overall_score: float = 0.0
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)

@dataclass
class ProfessionalDecision:
    """Professional decision structure with full documentation"""
    decision_id: str
    question: str
    framework_used: DecisionFramework
    criteria: List[Criterion]
    alternatives: List[Alternative]
    recommended_alternative: str
    confidence_level: ConfidenceLevel
    priority: RecommendationPriority
    reasoning: str
    evidence_summary: str
    implementation_steps: List[str]
    risks_and_mitigations: List[Dict[str, str]]
    success_metrics: List[str]
    review_timeline: str
    stakeholders: List[str]
    decision_date: str = field(default_factory=lambda: datetime.now().isoformat())
    quality_score: float = 0.0

class ProfessionalDecisionFramework:
    """Professional decision-making framework for AI agents"""
    
    def __init__(self):
        self.decision_history: List[ProfessionalDecision] = []
        
    def analyze_decision_context(self, question: str) -> Tuple[DecisionFramework, List[Criterion]]:
        """Analyze the question and determine the best decision framework to use"""
        question_lower = question.lower()
        
        # Determine framework based on question type
        if any(word in question_lower for word in ['invest', 'buy', 'financial', 'money', 'cost', 'budget']):
            framework = DecisionFramework.COST_BENEFIT
            criteria = [
                Criterion("Return on Investment", 0.3, "Expected financial return", "Percentage or absolute value"),
                Criterion("Risk Level", 0.3, "Level of financial risk", "Low/Medium/High"),
                Criterion("Liquidity", 0.2, "How easily convertible to cash", "Days to convert"),
                Criterion("Timeline", 0.2, "Investment timeline", "Short/Medium/Long term")
            ]
        elif any(word in question_lower for word in ['career', 'job', 'work', 'promotion', 'salary']):
            framework = DecisionFramework.PROS_CONS
            criteria = [
                Criterion("Career Growth", 0.3, "Advancement opportunities", "Growth potential rating"),
                Criterion("Compensation", 0.25, "Financial compensation", "Salary and benefits"),
                Criterion("Work-Life Balance", 0.25, "Quality of life impact", "Balance rating"),
                Criterion("Skill Development", 0.2, "Learning opportunities", "Skills gained")
            ]
        elif any(word in question_lower for word in ['risk', 'safety', 'security', 'danger']):
            framework = DecisionFramework.RISK_REWARD
            criteria = [
                Criterion("Risk Severity", 0.4, "Potential negative impact", "Severity scale 1-10"),
                Criterion("Risk Probability", 0.3, "Likelihood of occurrence", "Probability percentage"),
                Criterion("Reward Potential", 0.2, "Potential positive outcome", "Benefit scale 1-10"),
                Criterion("Mitigation Feasibility", 0.1, "Ability to reduce risk", "Feasibility rating")
            ]
        elif any(word in question_lower for word in ['choose', 'select', 'decide between', 'option']):
            framework = DecisionFramework.MECE
            criteria = [
                Criterion("Effectiveness", 0.3, "How well does it solve the problem", "Effectiveness rating"),
                Criterion("Feasibility", 0.25, "How realistic to implement", "Implementation difficulty"),
                Criterion("Cost", 0.25, "Financial and resource cost", "Total cost estimate"),
                Criterion("Time", 0.2, "Timeline to implement", "Implementation timeline")
            ]
        else:
            framework = DecisionFramework.SWOT
            criteria = [
                Criterion("Strengths", 0.25, "Internal positive factors", "Strength assessment"),
                Criterion("Weaknesses", 0.25, "Internal negative factors", "Weakness assessment"),
                Criterion("Opportunities", 0.25, "External positive factors", "Opportunity assessment"),
                Criterion("Threats", 0.25, "External negative factors", "Threat assessment")
            ]
            
        return framework, criteria
    
    def create_decision_alternatives(self, question: str, framework: DecisionFramework) -> List[Alternative]:
        """Generate standard decision alternatives based on the framework"""
        alternatives = []
        
        # Extract potential alternatives from the question
        if "should i" in question.lower():
            alternatives.extend([
                Alternative("Proceed", "Go ahead with the proposed action"),
                Alternative("Wait", "Delay the decision and gather more information"),
                Alternative("Modify", "Proceed with modifications to reduce risk"),
                Alternative("Decline", "Do not proceed with the proposed action")
            ])
        elif "which" in question.lower() or "choose" in question.lower():
            # For choice questions, we'll need agent input to identify specific options
            alternatives.extend([
                Alternative("Option A", "First identified option"),
                Alternative("Option B", "Second identified option"),
                Alternative("Hybrid Approach", "Combination of multiple options")
            ])
        else:
            # General alternatives
            alternatives.extend([
                Alternative("Conservative Approach", "Low-risk, cautious approach"),
                Alternative("Balanced Approach", "Moderate risk and reward balance"),
                Alternative("Aggressive Approach", "High-risk, high-reward approach")
            ])
            
        return alternatives
    
    def calculate_weighted_scores(self, alternatives: List[Alternative], criteria: List[Criterion]) -> List[Alternative]:
        """Calculate weighted scores for each alternative"""
        for alternative in alternatives:
            total_score = 0.0
            for criterion in criteria:
                if criterion.name in alternative.scores:
                    total_score += alternative.scores[criterion.name] * criterion.weight
            alternative.overall_score = total_score
            
        # Sort alternatives by score (descending)
        alternatives.sort(key=lambda x: x.overall_score, reverse=True)
        return alternatives
    
    def generate_professional_recommendation(self, 
                                           question: str, 
                                           agent_responses: List[Dict[str, Any]],
                                           discussion_history: List[Dict[str, Any]]) -> ProfessionalDecision:
        """Generate a professional decision recommendation"""
        
        # Analyze decision context
        framework, criteria = self.analyze_decision_context(question)
        
        # Create alternatives
        alternatives = self.create_decision_alternatives(question, framework)
        
        # Extract evidence from agent responses
        evidence = self.extract_evidence_from_responses(agent_responses)
        
        # Score alternatives based on agent input
        alternatives = self.score_alternatives_from_agent_input(alternatives, criteria, agent_responses, discussion_history)
        
        # Calculate weighted scores
        alternatives = self.calculate_weighted_scores(alternatives, criteria)
        
        # Select recommended alternative (highest score)
        recommended_alternative = alternatives[0] if alternatives else None
        
        # Determine confidence level
        confidence_level = self.determine_confidence_level(alternatives, agent_responses)
        
        # Generate professional decision
        decision = ProfessionalDecision(
            decision_id=f"DEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            question=question,
            framework_used=framework,
            criteria=criteria,
            alternatives=alternatives,
            recommended_alternative=recommended_alternative.name if recommended_alternative else "No recommendation",
            confidence_level=confidence_level,
            priority=RecommendationPriority.HIGH,
            reasoning=self.generate_reasoning(alternatives, agent_responses, discussion_history),
            evidence_summary=self.summarize_evidence(evidence),
            implementation_steps=self.generate_implementation_steps(recommended_alternative, question),
            risks_and_mitigations=self.identify_risks_and_mitigations(alternatives, agent_responses),
            success_metrics=self.define_success_metrics(question, recommended_alternative),
            review_timeline=self.determine_review_timeline(question),
            stakeholders=self.identify_stakeholders(question),
            quality_score=self.calculate_decision_quality_score(alternatives, evidence, agent_responses)
        )
        
        self.decision_history.append(decision)
        return decision
    
    def extract_evidence_from_responses(self, agent_responses: List[Dict[str, Any]]) -> List[Evidence]:
        """Extract evidence from agent responses"""
        evidence = []
        for response in agent_responses:
            # Look for references to frameworks, standards, or sources
            text = response.get('text_response', '')
            if any(keyword in text.lower() for keyword in ['cfa institute', 'sec', 'finra', 'iso', 'basel']):
                evidence.append(Evidence(
                    source=response['agent_name'],
                    type="expert_opinion",
                    credibility=0.8,
                    relevance=0.9,
                    content=text[:200] + "..." if len(text) > 200 else text
                ))
        return evidence
    
    def score_alternatives_from_agent_input(self, alternatives: List[Alternative], 
                                          criteria: List[Criterion],
                                          agent_responses: List[Dict[str, Any]], 
                                          discussion_history: List[Dict[str, Any]]) -> List[Alternative]:
        """Score alternatives based on agent input"""
        # This is a simplified scoring mechanism
        # In a real implementation, this would use NLP to extract specific scores
        
        for alternative in alternatives:
            for criterion in criteria:
                # Default scoring based on alternative type and criterion
                if alternative.name == "Conservative Approach":
                    if "risk" in criterion.name.lower():
                        alternative.scores[criterion.name] = 0.9  # Low risk
                    elif "return" in criterion.name.lower():
                        alternative.scores[criterion.name] = 0.4  # Low return
                    else:
                        alternative.scores[criterion.name] = 0.6
                elif alternative.name == "Aggressive Approach":
                    if "risk" in criterion.name.lower():
                        alternative.scores[criterion.name] = 0.3  # High risk
                    elif "return" in criterion.name.lower():
                        alternative.scores[criterion.name] = 0.9  # High return
                    else:
                        alternative.scores[criterion.name] = 0.7
                else:  # Balanced approach
                    alternative.scores[criterion.name] = 0.6
                    
        return alternatives
    
    def determine_confidence_level(self, alternatives: List[Alternative], agent_responses: List[Dict[str, Any]]) -> ConfidenceLevel:
        """Determine confidence level based on agent consensus and data quality"""
        if not alternatives:
            return ConfidenceLevel.VERY_LOW
            
        # Check score spread
        scores = [alt.overall_score for alt in alternatives]
        if len(scores) > 1:
            score_spread = max(scores) - min(scores)
            if score_spread > 0.7:
                return ConfidenceLevel.HIGH
            elif score_spread > 0.4:
                return ConfidenceLevel.MEDIUM
            else:
                return ConfidenceLevel.LOW
        
        return ConfidenceLevel.MEDIUM
    
    def generate_reasoning(self, alternatives: List[Alternative], 
                         agent_responses: List[Dict[str, Any]], 
                         discussion_history: List[Dict[str, Any]]) -> str:
        """Generate professional reasoning for the recommendation"""
        if not alternatives:
            return "Insufficient data to make a recommendation."
            
        best_alternative = alternatives[0]
        reasoning = f"Based on our structured analysis using professional decision-making frameworks, " \
                   f"we recommend '{best_alternative.name}' with a confidence score of {best_alternative.overall_score:.2f}.\n\n"
        
        reasoning += "Key factors in this recommendation:\n"
        for criterion_name, score in best_alternative.scores.items():
            reasoning += f"• {criterion_name}: {score:.2f}\n"
            
        reasoning += f"\nThis recommendation is supported by input from {len(agent_responses)} specialized advisors " \
                    f"with diverse perspectives including risk assessment, opportunity analysis, and practical implementation considerations."
        
        return reasoning
    
    def summarize_evidence(self, evidence: List[Evidence]) -> str:
        """Summarize evidence supporting the recommendation"""
        if not evidence:
            return "No external evidence available."
            
        summary = f"Evidence base includes {len(evidence)} sources:\n"
        for ev in evidence:
            summary += f"• {ev.type.title()} from {ev.source} (Credibility: {ev.credibility:.1f})\n"
            
        return summary
    
    def generate_implementation_steps(self, alternative: Optional[Alternative], question: str) -> List[str]:
        """Generate implementation steps for the recommended alternative"""
        if not alternative:
            return ["Gather additional information before proceeding"]
            
        # Generate generic implementation steps
        steps = [
            "Develop detailed implementation plan with timeline",
            "Identify required resources and budget",
            "Establish success metrics and monitoring system",
            "Communicate plan to relevant stakeholders",
            "Execute plan with regular progress reviews",
            "Monitor results and adjust as needed"
        ]
        
        # Customize based on question type
        if any(word in question.lower() for word in ['invest', 'financial', 'money']):
            steps.insert(1, "Consult with financial advisor if needed")
            steps.insert(2, "Ensure adequate emergency fund is maintained")
            
        return steps
    
    def identify_risks_and_mitigations(self, alternatives: List[Alternative], 
                                     agent_responses: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Identify risks and mitigation strategies"""
        risks = []
        
        # Extract risks from agent responses
        for response in agent_responses:
            if 'risk' in response.get('agent_type', '').lower():
                risks.append({
                    "risk": "Market volatility and uncertainty",
                    "mitigation": "Diversification and phased implementation"
                })
                
        # Add standard risks
        risks.extend([
            {"risk": "Insufficient information", "mitigation": "Conduct additional research before proceeding"},
            {"risk": "Changing market conditions", "mitigation": "Regular monitoring and adjustment mechanisms"},
            {"risk": "Implementation challenges", "mitigation": "Detailed planning and contingency measures"}
        ])
        
        return risks
    
    def define_success_metrics(self, question: str, alternative: Optional[Alternative]) -> List[str]:
        """Define success metrics for the recommendation"""
        metrics = ["Achievement of stated objectives", "Stakeholder satisfaction", "Risk mitigation effectiveness"]
        
        if any(word in question.lower() for word in ['invest', 'financial', 'money']):
            metrics.extend(["Return on investment", "Portfolio performance", "Risk-adjusted returns"])
        elif any(word in question.lower() for word in ['career', 'job']):
            metrics.extend(["Career advancement", "Salary growth", "Skill development"])
            
        return metrics
    
    def determine_review_timeline(self, question: str) -> str:
        """Determine appropriate review timeline"""
        if any(word in question.lower() for word in ['urgent', 'immediate', 'asap']):
            return "Weekly reviews for first month, then monthly"
        elif any(word in question.lower() for word in ['invest', 'long-term', 'career']):
            return "Quarterly reviews with annual comprehensive review"
        else:
            return "Monthly reviews for first quarter, then quarterly"
    
    def identify_stakeholders(self, question: str) -> List[str]:
        """Identify relevant stakeholders"""
        stakeholders = ["Decision maker", "Family/Personal network"]
        
        if any(word in question.lower() for word in ['invest', 'financial']):
            stakeholders.extend(["Financial advisor", "Tax advisor", "Investment manager"])
        elif any(word in question.lower() for word in ['career', 'job']):
            stakeholders.extend(["Current employer", "Potential employer", "Career mentor"])
        elif any(word in question.lower() for word in ['business', 'company']):
            stakeholders.extend(["Employees", "Customers", "Shareholders", "Partners"])
            
        return stakeholders
    
    def calculate_decision_quality_score(self, alternatives: List[Alternative], 
                                       evidence: List[Evidence], 
                                       agent_responses: List[Dict[str, Any]]) -> float:
        """Calculate overall decision quality score"""
        if not alternatives:
            return 0.0
            
        # Factors affecting quality score
        alternative_quality = len(alternatives) / 5.0  # More alternatives = better analysis
        evidence_quality = len(evidence) / 3.0  # More evidence = better support
        agent_consensus = len(agent_responses) / 4.0  # More agents = better coverage
        
        # Normalize and weight
        quality_score = min(1.0, (alternative_quality * 0.4 + evidence_quality * 0.3 + agent_consensus * 0.3))
        
        return quality_score
    
    def export_decision_report(self, decision: ProfessionalDecision) -> str:
        """Export decision as professional report"""
        report = f"""
PROFESSIONAL DECISION ANALYSIS REPORT
=====================================

Decision ID: {decision.decision_id}
Date: {decision.decision_date}
Framework: {decision.framework_used.value.upper()}
Quality Score: {decision.quality_score:.2f}/1.0
Confidence Level: {decision.confidence_level.value.upper()}
Priority: {decision.priority.value.upper()}

EXECUTIVE SUMMARY
================
Question: {decision.question}

Recommendation: {decision.recommended_alternative}

ANALYSIS FRAMEWORK
==================
{decision.reasoning}

EVIDENCE BASE
=============
{decision.evidence_summary}

IMPLEMENTATION PLAN
===================
"""
        
        for i, step in enumerate(decision.implementation_steps, 1):
            report += f"{i}. {step}\n"
            
        report += "\nRISK ANALYSIS\n============\n"
        for risk_item in decision.risks_and_mitigations:
            report += f"Risk: {risk_item['risk']}\nMitigation: {risk_item['mitigation']}\n\n"
            
        report += "SUCCESS METRICS\n===============\n"
        for metric in decision.success_metrics:
            report += f"• {metric}\n"
            
        report += f"\nREVIEW SCHEDULE\n===============\n{decision.review_timeline}\n"
        
        report += "\nSTAKEHOLDERS\n============\n"
        for stakeholder in decision.stakeholders:
            report += f"• {stakeholder}\n"
            
        return report 