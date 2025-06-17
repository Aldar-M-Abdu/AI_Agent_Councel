"""
Executive Reporting System for Professional AI Agent Council
Generates international-standard executive reports and decision briefings
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import logging
from .decision_framework import ProfessionalDecision, DecisionFramework, ConfidenceLevel
from .consensus_manager import ConsensusResult, ConsensusMethod

logger = logging.getLogger(__name__)

@dataclass
class ExecutiveSummary:
    """Executive summary structure"""
    recommendation: str
    confidence_level: str
    key_rationale: List[str]
    financial_impact: Optional[str] = None
    timeline: Optional[str] = None
    risk_assessment: Optional[str] = None

@dataclass
class KeyFindings:
    """Key findings from the analysis"""
    primary_insights: List[str]
    supporting_evidence: List[str]
    dissenting_views: List[str]
    data_quality_notes: List[str]

@dataclass
class ActionPlan:
    """Detailed action plan"""
    immediate_actions: List[Dict[str, Any]]  # action, timeline, responsible_party
    short_term_actions: List[Dict[str, Any]]  # 1-3 months
    long_term_actions: List[Dict[str, Any]]   # 3+ months
    success_metrics: List[str]
    review_schedule: str

@dataclass
class RiskAnalysis:
    """Comprehensive risk analysis"""
    high_risks: List[Dict[str, str]]  # risk, probability, impact, mitigation
    medium_risks: List[Dict[str, str]]
    low_risks: List[Dict[str, str]]
    risk_monitoring_plan: List[str]
    contingency_plans: List[str]

@dataclass
class ExecutiveReport:
    """Complete executive report"""
    report_id: str
    title: str
    executive_summary: ExecutiveSummary
    key_findings: KeyFindings
    action_plan: ActionPlan
    risk_analysis: RiskAnalysis
    appendices: Dict[str, Any]
    generated_date: str = field(default_factory=lambda: datetime.now().isoformat())
    report_type: str = "Strategic Decision Analysis"
    classification: str = "Internal Use"

class ProfessionalExecutiveReporter:
    """Professional executive reporting system"""
    
    def __init__(self):
        self.report_templates = {
            "investment": "Investment Decision Analysis",
            "strategic": "Strategic Initiative Assessment", 
            "operational": "Operational Decision Brief",
            "risk": "Risk Assessment Report",
            "general": "Executive Decision Brief"
        }
        
    def generate_executive_report(self, 
                                decision: ProfessionalDecision,
                                consensus: ConsensusResult,
                                agent_responses: List[Dict[str, Any]],
                                discussion_history: List[Dict[str, Any]],
                                user_question: str) -> ExecutiveReport:
        """Generate comprehensive executive report"""
        
        # Determine report type
        report_type = self.determine_report_type(user_question)
        
        # Generate executive summary
        exec_summary = self.create_executive_summary(decision, consensus)
        
        # Extract key findings
        key_findings = self.extract_key_findings(agent_responses, discussion_history, consensus)
        
        # Create action plan
        action_plan = self.create_action_plan(decision, consensus)
        
        # Perform risk analysis
        risk_analysis = self.perform_risk_analysis(decision, consensus, agent_responses)
        
        # Create appendices
        appendices = self.create_appendices(decision, consensus, agent_responses, discussion_history)
        
        # Generate report
        report = ExecutiveReport(
            report_id=f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=self.generate_report_title(user_question, decision.recommended_alternative),
            executive_summary=exec_summary,
            key_findings=key_findings,
            action_plan=action_plan,
            risk_analysis=risk_analysis,
            appendices=appendices,
            report_type=report_type
        )
        
        return report
    
    def determine_report_type(self, question: str) -> str:
        """Determine the type of report based on question"""
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['invest', 'financial', 'money', 'budget', 'cost']):
            return self.report_templates["investment"]
        elif any(word in question_lower for word in ['strategy', 'strategic', 'long-term', 'vision']):
            return self.report_templates["strategic"]
        elif any(word in question_lower for word in ['risk', 'danger', 'safety', 'security']):
            return self.report_templates["risk"]
        elif any(word in question_lower for word in ['operations', 'process', 'workflow', 'efficiency']):
            return self.report_templates["operational"]
        else:
            return self.report_templates["general"]
    
    def generate_report_title(self, question: str, recommendation: str) -> str:
        """Generate professional report title"""
        # Extract key subject from question
        question_words = question.lower().split()
        key_subjects = []
        
        business_terms = ['investment', 'strategy', 'market', 'financial', 'business', 'operations', 
                         'technology', 'risk', 'growth', 'expansion', 'acquisition', 'merger']
        
        for word in question_words:
            if word in business_terms:
                key_subjects.append(word.title())
                
        if key_subjects:
            subject = " & ".join(key_subjects[:2])  # Take first two subjects
            return f"Executive Decision Brief: {subject} Analysis & Recommendation"
        else:
            return f"Executive Decision Brief: Strategic Analysis & Recommendation"
    
    def create_executive_summary(self, decision: ProfessionalDecision, 
                               consensus: ConsensusResult) -> ExecutiveSummary:
        """Create executive summary"""
        
        # Extract financial impact if mentioned
        financial_impact = None
        if any(word in decision.question.lower() for word in ['$', 'cost', 'budget', 'invest', 'price']):
            financial_impact = "Financial implications require careful consideration - see detailed analysis"
            
        # Determine timeline
        timeline = self.extract_timeline_from_decision(decision)
        
        # Risk assessment summary
        risk_level = "Medium"
        if decision.confidence_level in [ConfidenceLevel.HIGH, ConfidenceLevel.VERY_HIGH]:
            risk_level = "Low to Medium"
        elif decision.confidence_level in [ConfidenceLevel.LOW, ConfidenceLevel.VERY_LOW]:
            risk_level = "Medium to High"
            
        return ExecutiveSummary(
            recommendation=decision.recommended_alternative,
            confidence_level=decision.confidence_level.value.replace('_', ' ').title(),
            key_rationale=self.extract_key_rationale(decision, consensus),
            financial_impact=financial_impact,
            timeline=timeline,
            risk_assessment=f"{risk_level} risk profile identified"
        )
    
    def extract_key_rationale(self, decision: ProfessionalDecision, 
                            consensus: ConsensusResult) -> List[str]:
        """Extract key rationale points"""
        rationale = []
        
        # From decision framework
        if decision.alternatives:
            best_alt = decision.alternatives[0]
            rationale.append(f"Highest scoring alternative with {best_alt.overall_score:.2f} composite score")
            
        # From consensus
        rationale.append(f"Strong consensus achieved ({consensus.consensus_strength:.1%}) using {consensus.method_used.value.replace('_', ' ').title()} methodology")
        
        # Agent agreement
        if len(consensus.participating_agents) > 2:
            rationale.append(f"Recommendation supported by {len(consensus.participating_agents)} expert advisors")
            
        # Evidence base
        if decision.alternatives and decision.alternatives[0].evidence:
            rationale.append(f"Decision supported by {len(decision.alternatives[0].evidence)} pieces of evidence")
            
        return rationale[:4]  # Top 4 rationale points
    
    def extract_timeline_from_decision(self, decision: ProfessionalDecision) -> str:
        """Extract timeline information from decision"""
        if any(word in decision.question.lower() for word in ['urgent', 'immediate', 'asap']):
            return "Immediate action required (within 1-2 weeks)"
        elif any(word in decision.question.lower() for word in ['soon', 'quickly', 'fast']):
            return "Short-term implementation (1-3 months)"
        elif any(word in decision.question.lower() for word in ['long-term', 'future', 'eventually']):
            return "Long-term implementation (6+ months)"
        else:
            return "Medium-term implementation (3-6 months)"
    
    def extract_key_findings(self, agent_responses: List[Dict[str, Any]], 
                           discussion_history: List[Dict[str, Any]],
                           consensus: ConsensusResult) -> KeyFindings:
        """Extract key findings from analysis"""
        
        primary_insights = []
        supporting_evidence = []
        dissenting_views = []
        data_quality_notes = []
        
        # Extract insights from agent responses
        for response in agent_responses:
            text = response.get('text_response', '')
            agent_name = response.get('agent_name', '')
            
            # Look for key insights
            if len(text) > 100:  # Substantial response
                insight = f"{agent_name}: {text[:100]}..."
                primary_insights.append(insight)
                
            # Look for evidence references
            if any(keyword in text.lower() for keyword in ['research', 'study', 'data', 'evidence']):
                supporting_evidence.append(f"Evidence cited by {agent_name}")
                
        # Extract dissenting views from consensus
        for dissent in consensus.dissenting_opinions:
            dissenting_views.append(f"{dissent['agent_name']} recommends '{dissent['preferred_alternative']}' (Confidence: {dissent['confidence']:.1%})")
            
        # Data quality assessment
        if consensus.quality_assessment.get('overall_quality', 0) > 0.8:
            data_quality_notes.append("High-quality analysis with strong participation and evidence base")
        elif consensus.quality_assessment.get('overall_quality', 0) > 0.6:
            data_quality_notes.append("Good-quality analysis with adequate participation")
        else:
            data_quality_notes.append("Analysis quality limited by participation or evidence availability")
            
        return KeyFindings(
            primary_insights=primary_insights[:5],  # Top 5 insights
            supporting_evidence=supporting_evidence[:3],  # Top 3 evidence points
            dissenting_views=dissenting_views[:3],  # Top 3 dissenting views
            data_quality_notes=data_quality_notes
        )
    
    def create_action_plan(self, decision: ProfessionalDecision, 
                         consensus: ConsensusResult) -> ActionPlan:
        """Create detailed action plan"""
        
        immediate_actions = []
        short_term_actions = []
        long_term_actions = []
        
        # Immediate actions (next 2 weeks)
        immediate_actions.extend([
            {
                "action": "Communicate decision to key stakeholders",
                "timeline": "Within 3 days",
                "responsible_party": "Decision maker"
            },
            {
                "action": "Finalize implementation planning",
                "timeline": "Within 1 week", 
                "responsible_party": "Implementation team"
            }
        ])
        
        # Add specific immediate actions from decision
        if decision.implementation_steps:
            for step in decision.implementation_steps[:2]:
                immediate_actions.append({
                    "action": step,
                    "timeline": "Within 2 weeks",
                    "responsible_party": "Assigned team lead"
                })
        
        # Short-term actions (1-3 months)
        short_term_actions.extend([
            {
                "action": "Execute primary implementation phase",
                "timeline": "Month 1-2",
                "responsible_party": "Project team"
            },
            {
                "action": "Monitor initial results and adjust as needed",
                "timeline": "Month 2-3",
                "responsible_party": "Project manager"
            }
        ])
        
        # Long-term actions (3+ months)
        long_term_actions.extend([
            {
                "action": "Conduct comprehensive review of outcomes",
                "timeline": "Month 6",
                "responsible_party": "Senior management"
            },
            {
                "action": "Implement lessons learned and optimizations",
                "timeline": "Month 6+",
                "responsible_party": "Process improvement team"
            }
        ])
        
        return ActionPlan(
            immediate_actions=immediate_actions,
            short_term_actions=short_term_actions,
            long_term_actions=long_term_actions,
            success_metrics=decision.success_metrics,
            review_schedule=decision.review_timeline
        )
    
    def perform_risk_analysis(self, decision: ProfessionalDecision,
                            consensus: ConsensusResult,
                            agent_responses: List[Dict[str, Any]]) -> RiskAnalysis:
        """Perform comprehensive risk analysis"""
        
        high_risks = []
        medium_risks = []
        low_risks = []
        
        # Extract risks from decision
        for risk_item in decision.risks_and_mitigations:
            risk_dict = {
                "risk": risk_item["risk"],
                "probability": "Medium",  # Default - could be enhanced with NLP
                "impact": "Medium",      # Default - could be enhanced with NLP
                "mitigation": risk_item["mitigation"]
            }
            medium_risks.append(risk_dict)
            
        # Assess consensus-based risks
        if consensus.consensus_strength < 0.6:
            high_risks.append({
                "risk": "Low consensus may lead to implementation resistance",
                "probability": "High",
                "impact": "High", 
                "mitigation": "Conduct additional stakeholder engagement"
            })
        elif consensus.consensus_strength < 0.8:
            medium_risks.append({
                "risk": "Moderate consensus requires change management attention",
                "probability": "Medium",
                "impact": "Medium",
                "mitigation": "Implement structured change management process"
            })
            
        # Add standard business risks
        low_risks.extend([
            {
                "risk": "Market conditions may change during implementation",
                "probability": "Low",
                "impact": "Medium",
                "mitigation": "Regular market monitoring and adjustment mechanisms"
            },
            {
                "risk": "Resource availability may be constrained",
                "probability": "Low",
                "impact": "Low",
                "mitigation": "Maintain resource buffer and alternative sourcing"
            }
        ])
        
        return RiskAnalysis(
            high_risks=high_risks,
            medium_risks=medium_risks,
            low_risks=low_risks,
            risk_monitoring_plan=[
                "Weekly risk assessment during first month",
                "Monthly risk review thereafter",
                "Quarterly comprehensive risk analysis"
            ],
            contingency_plans=[
                "Alternative implementation approaches prepared",
                "Escalation procedures established",
                "Resource reallocation protocols defined"
            ]
        )
    
    def create_appendices(self, decision: ProfessionalDecision,
                        consensus: ConsensusResult, 
                        agent_responses: List[Dict[str, Any]],
                        discussion_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create report appendices"""
        
        appendices = {}
        
        # Appendix A: Detailed Analysis Framework
        appendices["A_Analysis_Framework"] = {
            "framework_used": decision.framework_used.value,
            "criteria_weights": [{"name": c.name, "weight": c.weight, "description": c.description} 
                               for c in decision.criteria],
            "alternatives_evaluated": len(decision.alternatives)
        }
        
        # Appendix B: Agent Consultation Details
        appendices["B_Expert_Consultation"] = {
            "participating_experts": consensus.participating_agents,
            "consensus_method": consensus.method_used.value,
            "rounds_conducted": len(consensus.rounds_conducted),
            "final_consensus_strength": consensus.consensus_strength
        }
        
        # Appendix C: Supporting Evidence
        evidence_summary = []
        for alt in decision.alternatives:
            for evidence in alt.evidence:
                evidence_summary.append({
                    "source": evidence.source,
                    "type": evidence.type,
                    "credibility": evidence.credibility,
                    "content_summary": evidence.content[:100] + "..." if len(evidence.content) > 100 else evidence.content
                })
                
        appendices["C_Supporting_Evidence"] = evidence_summary
        
        # Appendix D: Quality Metrics
        appendices["D_Quality_Metrics"] = {
            "decision_quality_score": decision.quality_score,
            "consensus_quality_assessment": consensus.quality_assessment,
            "confidence_interval": consensus.confidence_interval
        }
        
        return appendices
    
    def export_professional_report(self, report: ExecutiveReport) -> str:
        """Export as professional business report"""
        
        formatted_report = f"""


══════════════════════════════════════════════════════════════════════════════
                            {report.title.upper()}
══════════════════════════════════════════════════════════════════════════════

Report ID: {report.report_id}
Date: {datetime.fromisoformat(report.generated_date).strftime('%B %d, %Y')}
Classification: {report.classification}
Report Type: {report.report_type}


EXECUTIVE SUMMARY
═════════════════

RECOMMENDATION: {report.executive_summary.recommendation}

CONFIDENCE LEVEL: {report.executive_summary.confidence_level}

KEY RATIONALE:
"""
        
        for i, rationale in enumerate(report.executive_summary.key_rationale, 1):
            formatted_report += f"{i}. {rationale}\n"
            
        if report.executive_summary.financial_impact:
            formatted_report += f"\nFINANCIAL IMPACT: {report.executive_summary.financial_impact}\n"
            
        if report.executive_summary.timeline:
            formatted_report += f"IMPLEMENTATION TIMELINE: {report.executive_summary.timeline}\n"
            
        formatted_report += f"RISK ASSESSMENT: {report.executive_summary.risk_assessment}\n"
        
        formatted_report += f"""

KEY FINDINGS
════════════

PRIMARY INSIGHTS:
"""
        
        for i, insight in enumerate(report.key_findings.primary_insights, 1):
            formatted_report += f"{i}. {insight}\n"
            
        if report.key_findings.supporting_evidence:
            formatted_report += f"\nSUPPORTING EVIDENCE:\n"
            for evidence in report.key_findings.supporting_evidence:
                formatted_report += f"• {evidence}\n"
                
        if report.key_findings.dissenting_views:
            formatted_report += f"\nDISSENTING VIEWS:\n"
            for dissent in report.key_findings.dissenting_views:
                formatted_report += f"• {dissent}\n"
                
        formatted_report += f"""

ACTION PLAN
═══════════

IMMEDIATE ACTIONS (Next 2 Weeks):
"""
        
        for i, action in enumerate(report.action_plan.immediate_actions, 1):
            formatted_report += f"{i}. {action['action']}\n"
            formatted_report += f"   Timeline: {action['timeline']}\n"
            formatted_report += f"   Responsible: {action['responsible_party']}\n\n"
            
        formatted_report += f"SHORT-TERM ACTIONS (1-3 Months):\n"
        for i, action in enumerate(report.action_plan.short_term_actions, 1):
            formatted_report += f"{i}. {action['action']}\n"
            formatted_report += f"   Timeline: {action['timeline']}\n"
            formatted_report += f"   Responsible: {action['responsible_party']}\n\n"
            
        formatted_report += f"LONG-TERM ACTIONS (3+ Months):\n"
        for i, action in enumerate(report.action_plan.long_term_actions, 1):
            formatted_report += f"{i}. {action['action']}\n"
            formatted_report += f"   Timeline: {action['timeline']}\n"
            formatted_report += f"   Responsible: {action['responsible_party']}\n\n"
            
        formatted_report += f"""
SUCCESS METRICS:
"""
        
        for metric in report.action_plan.success_metrics:
            formatted_report += f"• {metric}\n"
            
        formatted_report += f"\nREVIEW SCHEDULE: {report.action_plan.review_schedule}\n"
        
        formatted_report += f"""

RISK ANALYSIS
═════════════
"""
        
        if report.risk_analysis.high_risks:
            formatted_report += f"HIGH RISKS:\n"
            for i, risk in enumerate(report.risk_analysis.high_risks, 1):
                formatted_report += f"{i}. Risk: {risk['risk']}\n"
                formatted_report += f"   Probability: {risk['probability']} | Impact: {risk['impact']}\n"
                formatted_report += f"   Mitigation: {risk['mitigation']}\n\n"
                
        if report.risk_analysis.medium_risks:
            formatted_report += f"MEDIUM RISKS:\n"
            for i, risk in enumerate(report.risk_analysis.medium_risks, 1):
                formatted_report += f"{i}. Risk: {risk['risk']}\n"
                formatted_report += f"   Probability: {risk['probability']} | Impact: {risk['impact']}\n"
                formatted_report += f"   Mitigation: {risk['mitigation']}\n\n"
                
        formatted_report += f"RISK MONITORING PLAN:\n"
        for plan in report.risk_analysis.risk_monitoring_plan:
            formatted_report += f"• {plan}\n"
            
        formatted_report += f"""

APPENDICES
══════════

A. Analysis Framework Details
B. Expert Consultation Process  
C. Supporting Evidence Summary
D. Quality Assurance Metrics

[Detailed appendices available in technical documentation]


══════════════════════════════════════════════════════════════════════════════
                                END OF REPORT
══════════════════════════════════════════════════════════════════════════════

This report was generated by the Professional AI Agent Council system using 
structured decision-making methodologies and expert consensus-building processes.

Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return formatted_report
    
    def export_executive_dashboard(self, report: ExecutiveReport) -> Dict[str, Any]:
        """Export as executive dashboard data"""
        
        dashboard = {
            "title": report.title,
            "recommendation": report.executive_summary.recommendation,
            "confidence": report.executive_summary.confidence_level,
            "risk_level": report.executive_summary.risk_assessment,
            "timeline": report.executive_summary.timeline,
            "key_actions": len(report.action_plan.immediate_actions),
            "high_risks": len(report.risk_analysis.high_risks),
            "quality_score": report.appendices.get("D_Quality_Metrics", {}).get("decision_quality_score", 0),
            "consensus_strength": report.appendices.get("D_Quality_Metrics", {}).get("consensus_quality_assessment", {}).get("consensus_strength", 0),
            "generated_date": report.generated_date
        }
        
        return dashboard 