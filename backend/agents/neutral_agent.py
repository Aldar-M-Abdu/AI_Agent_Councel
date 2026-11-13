from .base_agent import BaseAgent

class NeutralAgent(BaseAgent):
    """
    Professional Strategic Analyst providing objective, evidence-based recommendations with comprehensive business analysis.
    Specializes in balanced decision frameworks, risk-benefit analysis, and multi-stakeholder perspectives.
    """
    def __init__(self):
        super().__init__(
            agent_name="Neutral Agent", 
            system_prompt="""You are a Senior Strategic Business Analyst with 15+ years of consulting experience advising large organizations.

IMPORTANT: Always respond in English. Use professional English terminology in strategic business analysis and consulting.

Your expertise spans across:

CORE COMPETENCIES:
• Strategic Planning & Business Analysis
• Multi-Criteria Decision Analysis (MCDA)
• Stakeholder Management & Alignment
• Risk-Benefit Assessment Frameworks
• Market Research & Competitive Analysis
• Financial Modeling & ROI Analysis
• Change Management & Implementation Planning

ANALYTICAL METHODOLOGY:
1. STRUCTURED ASSESSMENT: Use proven frameworks (SWOT, Porter's Five Forces, PESTEL, McKinsey 7S)
2. DATA-DRIVEN INSIGHTS: Reference industry benchmarks, market data, and evidence-based practices
3. STAKEHOLDER ANALYSIS: Consider all affected parties and their interests/concerns
4. SCENARIO PLANNING: Evaluate multiple outcomes with probability assessments
5. IMPLEMENTATION ROADMAP: Provide actionable steps with timelines and success metrics

COMMUNICATION STYLE:
• Professional, clear, and actionable
• Reference specific methodologies and frameworks
• Include quantitative analysis where relevant
• Provide balanced pros/cons with neutral assessment
• Ask strategic questions to uncover key considerations
• Cite industry best practices and case studies

DECISION FRAMEWORK:
For each recommendation, provide:
- Executive summary (key findings)
- Strategic alternatives analysis
- Risk assessment matrix
- Implementation considerations
- Success metrics & KPIs
- Next steps & decision points

Always maintain objectivity while delivering actionable insights that drive business value."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Strategic business analysis with evidence-based frameworks, balanced multi-stakeholder assessment, and implementation-focused recommendations"

    def generate_response(self, user_text: str) -> str:
        """
        Generate a professional strategic analysis response.
        Args:
            user_text (str): User's input question or statement.
        Returns:
            str: Agent's strategic analysis response.
        """
        guidance = """As a Senior Strategic Business Analyst, I will provide a comprehensive, objective analysis following this structure:

EXECUTIVE SUMMARY: Key findings and strategic recommendation

STRATEGIC ANALYSIS:
• Market context & Industry dynamics
• Stakeholder impact assessment
• Risk-benefit analysis matrix
• Resource requirements & Constraints
• Success probability & Critical factors

IMPLEMENTATION FRAMEWORK:
• Phased approach with milestones
• Resource allocation & Timeline
• Key performance indicators
• Risk mitigation strategies
• Governance & Decision points

STRATEGIC QUESTIONS:
I will conclude with 2-3 strategic questions to help you refine the approach and uncover additional considerations.

My analysis will be evidence-based, referencing relevant frameworks, industry benchmarks, and best practices where applicable."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _is_arabic(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        arabic_chars = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويىء')
        return any(char in arabic_chars for char in text)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professional strategic synthesis of multiple perspectives.
        """
        return """**STRATEGIC SYNTHESIS & BALANCED ASSESSMENT**

After analyzing the different perspectives presented, I have identified several important strategic themes:

**OPPORTUNITY CONVERGENCE**: The optimistic viewpoint highlights market potential and growth opportunities aligned with current industry trends. These positive scenarios deserve serious attention given their potential ROI.

**RISK MITIGATION IMPERATIVE**: The skeptical analysis raises critical concerns about implementation challenges, market volatility, and resource constraints. These risk factors require structured mitigation strategies.

**EVIDENCE-BASED INTEGRATION**: Combining these perspectives suggests a balanced approach that maximizes opportunities while addressing legitimate concerns through:
- Phased implementation with stage-gates
- Robust risk monitoring and early warning systems
- Stakeholder alignment and communication protocols
- Resource optimization and contingency planning

**STRATEGIC RECOMMENDATION**: A risk-adjusted approach that pursues high-value opportunities while maintaining defensive positioning. This balanced strategy enables opportunistic growth while preserving strategic flexibility.

**KEY STRATEGIC QUESTIONS**:
1. What are the most critical success factors that could make or break this initiative?
2. How can we structure this to maximize learning while minimizing downside exposure?
3. What stakeholder alignment is required for successful execution?"""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professional consensus building with a strategic framework.
        """
        return """**STRATEGIC CONSENSUS FRAMEWORK**

**INTEGRATED APPROACH**: Balance opportunity pursuit with risk management through a structured, phased implementation strategy.

**CONSENSUS ELEMENTS**:
• **Phase 1 - Validation**: Pilot testing with limited resource commitment
• **Phase 2 - Optimization**: Scale based on validated lessons and market feedback
• **Phase 3 - Expansion**: Full implementation with established success metrics

**GOVERNANCE STRUCTURE**:
- Clear decision authority and escalation paths
- Regular review cycles with go/no-go decision points
- Stakeholder communication and alignment protocols
- Success metrics and performance dashboards

**RISK MITIGATION**: Implement robust monitoring systems, contingency plans, and exit strategies while maintaining strategic flexibility.

**SUCCESS FACTORS**: Stakeholder alignment, resource adequacy, market timing, execution excellence, and adaptive management capabilities.

This balanced approach addresses each perspective while providing a practical path forward that maximizes value creation potential."""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional financial strategy with business frameworks.
        """
        return """**STRATEGIC FINANCIAL ANALYSIS**

**INVESTMENT FRAMEWORK**: Apply Modern Portfolio Theory with strategic asset allocation across risk categories. Implement a systematic approach with:
- **Due Diligence**: Comprehensive financial statement analysis, market research, and competitive positioning
- **Risk Assessment**: Value-at-Risk (VaR) modeling, stress testing, and scenario analysis
- **Portfolio Construction**: Diversification across asset classes, sectors, and geographic regions

**STRATEGIC METHODOLOGY**:
1. **Financial Goals**: Define clear ROI targets, risk tolerance, and investment time horizon
2. **Market Analysis**: Conduct thorough market research with industry reports and competitive intelligence
3. **Implementation Strategy**: Phased approach with regular portfolio rebalancing and performance monitoring

**PROFESSIONAL RESOURCES**: Reference CFA Institute guidelines, institutional research, and peer-reviewed financial literature for evidence-based decision-making.

**SUCCESS METRICS**: Track performance against benchmarks, monitor risk-adjusted returns, and maintain detailed documentation for continuous improvement.

**STRATEGIC QUESTION**: How does this investment align with your overall financial strategy and risk management framework?"""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional career strategy with development frameworks.
        """
        return """**STRATEGIC CAREER DEVELOPMENT FRAMEWORK**

**CAREER STRATEGY ANALYSIS**: Apply proven methods for career advancement and professional development:

**STRATEGIC ASSESSMENT**:
- **Competency Gap Analysis**: Map current capabilities against target role requirements
- **Market Intelligence**: Analyze industry trends, salary benchmarks, and growth forecasts with LinkedIn Insights, Bureau of Labor Statistics, and industry reports
- **Competitive Positioning**: Assess unique value proposition and differentiation strategies

**DEVELOPMENT OVERVIEW**:
1. **Competency Development**: Targeted learning plan with measurable milestones
2. **Network Building**: Strategic relationship building with industry leaders
3. **Brand Building**: Professional reputation management and thought leadership
4. **Experience Acquisition**: Structured approach to gaining relevant experience

**SUCCESS FRAMEWORK**: Use SMART goals with regular progress reviews and adaptive planning based on market feedback and opportunities.

**STRATEGIC QUESTIONS**:
- What specific skills or experiences would make you indispensable in your target role?
- How can you build strategic relationships that accelerate your career progression?
- What market trends should influence your career development strategy?"""
    
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional relationship management with evidence-based frameworks.
        """
        return """**STRATEGIC RELATIONSHIP FRAMEWORK**

**EVIDENCE-BASED APPROACH**: Apply research-based methods from relationship psychology and organizational behavior:

**RELATIONSHIP ASSESSMENT**:
- **Compatibility Analysis**: Values alignment, communication styles, and life compatibility
- **Relationship Dynamics**: Apply Gottman Institute research on relationship predictors
- **Stakeholder Impact**: Consider effects on family, career, and social networks

**STRATEGIC DEVELOPMENT**:
1. **Communication Protocols**: Establish clear expectations and feedback mechanisms
2. **Conflict Management**: Apply structured methods for handling conflicts
3. **Shared Goals**: Align on common objectives and success metrics
4. **Continuous Improvement**: Regular relationship reviews and adjustment strategies

**SUCCESS METRICS**: Track relationship satisfaction, communication effectiveness, and progress toward shared goals.

**PROFESSIONAL RESOURCES**: Reference peer-reviewed research in relationship psychology and evidence-based practices for relational development.

**STRATEGIC QUESTION**: How can you structure this relationship to maximize mutual value while preserving individual growth and development?"""
    
    def _generate_health_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional health strategy with evidence-based frameworks.
        """
        return """**STRATEGIC HEALTH OPTIMIZATION FRAMEWORK**

**EVIDENCE-BASED HEALTH STRATEGY**: Apply systematic approach to health and wellness optimization:

**HEALTH ASSESSMENT**:
- **Baseline Analysis**: Comprehensive health metrics and risk factor assessment
- **Goal Setting**: SMART health objectives aligned with lifestyle and priorities
- **Evidence Review**: Reference clinical guidelines, peer-reviewed research, and professional recommendations

**IMPLEMENTATION STRATEGY**:
1. **Professional Consultation**: Engage qualified healthcare providers for personalized guidance
2. **Systematic Approach**: Gradual implementation with measurable milestones
3. **Monitoring & Adjustment**: Regular progress tracking and strategy refinement
4. **Risk Management**: Identify potential obstacles and develop mitigation strategies

**SUCCESS FRAMEWORK**: Track key health indicators, lifestyle adherence, and quality of life improvements.

**PROFESSIONAL RESOURCES**: Consult medical professionals, reference clinical guidelines, and utilize evidence-based health interventions.

**STRATEGIC QUESTION**: What sustainable changes would provide the highest impact on your long-term health and quality of life?"""
    
    def _generate_education_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional education strategy with development frameworks.
        """
        return """**STRATEGIC LEARNING & DEVELOPMENT FRAMEWORK**

**EDUCATIONAL STRATEGY ANALYSIS**: Apply systematic approach to learning and skill development:

**LEARNING ASSESSMENT**:
- **Skills Gap Analysis**: Map current knowledge against career and personal objectives
- **Market Research**: Analyze industry demands, certification requirements, and skill premiums
- **ROI Analysis**: Evaluate cost-benefit of different educational pathways

**STRATEGIC APPROACH**:
1. **Learning Objectives**: Define clear, measurable learning outcomes
2. **Curriculum Design**: Select high-quality, accredited programs with strong track records
3. **Implementation Plan**: Balance learning with work/life commitments
4. **Success Metrics**: Establish benchmarks for knowledge acquisition and application

**PROFESSIONAL DEVELOPMENT**: Focus on continuously relevant skills, industry certifications, and thought leadership development.

**VALIDATION**: Reference accreditation bodies, industry standards, and peer reviews for educational quality assessment.

**STRATEGIC QUESTIONS**:
- Which skills will provide the highest career ROI over the next 5-10 years?
- How can you structure learning to maximize knowledge retention and practical application?"""
    
    def _generate_travel_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional travel strategy with risk management frameworks.
        """
        return """**STRATEGIC TRAVEL PLANNING FRAMEWORK**

**TRAVEL STRATEGY ANALYSIS**: Apply comprehensive planning methodology for optimal travel experiences:

**STRATEGIC ASSESSMENT**:
- **Objective Definition**: Clarify travel goals (business, leisure, cultural, educational)
- **Risk Assessment**: Evaluate security, health, and logistical considerations using government advisories
- **Resource Planning**: Budget optimization and resource allocation strategies

**IMPLEMENTATION FRAMEWORK**:
1. **Research & Planning**: Comprehensive destination research and itinerary optimization
2. **Risk Mitigation**: Travel insurance, health precautions, and emergency protocols
3. **Cultural Intelligence**: Preparation for cultural norms and business practices
4. **Documentation**: Passport, visa, and legal requirement compliance

**SUCCESS METRICS**: Safety, objective achievement, cultural learning, and cost-effectiveness.

**PROFESSIONAL RESOURCES**: Reference government travel advisories, professional travel organizations, and cultural intelligence frameworks.

**STRATEGIC QUESTION**: How can you structure this travel to maximize personal/professional development while managing risks and costs effectively?"""
    
    def _generate_technology_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional technology strategy with business frameworks.
        """
        return """**STRATEGIC TECHNOLOGY ADOPTION FRAMEWORK**

**TECHNOLOGY STRATEGY ANALYSIS**: Apply systematic approach to technology evaluation and implementation:

**STRATEGIC ASSESSMENT**:
- **Needs Analysis**: Map technology requirements to business/personal objectives
- **Technology Evaluation**: Assess solutions using established criteria (functionality, scalability, security, cost)
- **Market Research**: Analyze vendor landscape, industry standards, and best practices

**IMPLEMENTATION STRATEGY**:
1. **Pilot Testing**: Limited scope implementation for validation
2. **Change Management**: Training, support, and adoption strategies
3. **Integration Planning**: Ensure compatibility with existing systems and workflows
4. **Performance Monitoring**: Establish metrics for technology ROI and effectiveness

**RISK MANAGEMENT**: Address security, privacy, compliance, and vendor risk considerations.

**PROFESSIONAL RESOURCES**: Reference industry standards (ISO, NIST), technology research firms (Gartner, Forrester), and peer-reviewed technology assessments.

**STRATEGIC QUESTIONS**:
- What specific business/personal outcomes will this technology enable?
- How does this technology align with your long-term digital strategy?"""
    
    def _generate_general_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professional general strategy with comprehensive frameworks.
        """
        return """**STRATEGIC DECISION FRAMEWORK**

**SYSTEMATIC ANALYSIS APPROACH**: Apply proven business methodology for optimal decision-making:

**STRATEGIC METHODOLOGY**:
1. **Objective Definition**: Clarify goals, success criteria, and constraints
2. **Information Gathering**: Comprehensive research using credible sources and data
3. **Option Analysis**: Evaluate alternatives using structured decision matrices
4. **Stakeholder Consultation**: Engage relevant experts and affected parties
5. **Implementation Planning**: Develop detailed action plans with timelines and resources

**DECISION CRITERIA**:
- **Strategic Alignment**: Consistency with long-term objectives
- **Resource Requirements**: Time, money, and capability demands
- **Risk Assessment**: Probability and impact of potential outcomes
- **Success Probability**: Likelihood of achieving desired results

**PROFESSIONAL APPROACH**: Document decision rationale, establish success metrics, and plan regular reviews for continuous improvement.

**STRATEGIC QUESTIONS**:
- What are the most critical factors that will determine success or failure?
- How can you structure this decision to maximize learning and minimize regret?
- What additional information would significantly improve your decision confidence?"""
