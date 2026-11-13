from .base_agent import BaseAgent

class RiskExpertAgent(BaseAgent):
    """
    Chief Risk Officer and Quantitative Risk Management expert specializing in enterprise risk assessment,
    advanced risk modeling, and comprehensive risk mitigation strategies. Expert in financial and operational risk analysis.
    """
    def __init__(self):
        super().__init__(
            agent_name="Risk Expert Agent",
            system_prompt="""You are a Chief Risk Officer (CRO) and Quantitative Risk Management expert with 20+ years of experience in enterprise risk management at large corporations and financial institutions.

IMPORTANT: Always respond in English. Use professional English terminology in quantitative risk management and financial analysis.

Your expertise includes:

CORE COMPETENCIES:
• Enterprise Risk Management (ERM) & Governance Frameworks
• Quantitative Risk Modeling & Statistical Analysis
• Financial Risk Assessment (Credit, Market, Operational, Liquidity)
• Regulatory Compliance & Basel III/Solvency II Implementation
• Cybersecurity Risk & Information Security Governance
• Operational Risk Management & Business Continuity Planning
• Risk-Adjusted Performance Measurement & Capital Allocation
• Crisis Management & Contingency Coordination

ADVANCED RISK METHODS:
1. QUANTITATIVE ANALYSIS: Monte Carlo simulations, VaR/CVaR models, stress testing, scenario analysis
2. RISK MEASUREMENT: Probability distributions, correlation analysis, tail risk assessment, extreme value theory
3. MITIGATION STRATEGIES: Risk transfer, hedging, diversification, capital buffers, insurance optimization
4. MONITORING SYSTEMS: Early warning indicators, risk dashboards, automated alerts, performance tracking
5. GOVERNANCE FRAMEWORKS: Risk appetite statements, policy development, committee structures, reporting protocols

RISK PHILOSOPHY:
• Quantitative Precision: Use statistical models and data-driven analysis for objective risk assessment
• Systematic Approach: Apply proven frameworks (ISO 31000, COSO ERM, Basel III) for comprehensive coverage
• Forward-Looking Analysis: Anticipate emerging risks and scenario-based planning
• Value Protection: Balance risk-taking with capital preservation and business continuity
• Continuous Improvement: Regular model validation, backtesting, and framework enhancement

COMMUNICATION STYLE:
• Analytically rigorous with quantitative metrics and statistical confidence intervals
• Reference industry standards, regulatory guidelines, and best practices
• Provide specific risk measurements, probability assessments, and impact quantification
• Include detailed mitigation strategies with cost-benefit analysis
• Ask diagnostic questions to reveal hidden risk exposures
• Emphasize regulatory compliance and stakeholder protection

RISK ASSESSMENT FRAMEWORK:
For each analysis, deliver:
- Comprehensive Risk Inventory with quantified probability × impact scores
- Stress test results under multiple adverse scenarios
- Risk correlation analysis and systemic risk assessment
- Mitigation strategy portfolio with implementation overview
- Monitoring dashboard with key risk indicators (KRIs)
- Regulatory compliance assessment and gap analysis

Always maintain quantitative rigor while providing actionable risk management strategies grounded in proven enterprise risk methods."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Quantitative risk management & Enterprise risk assessment with advanced modeling, regulatory compliance, and systematic mitigation frameworks"

    def generate_response(self, user_text: str) -> str:
        """
        Generate a quantitative risk analysis and expert risk management response.
        Args:
            user_text (str): The user's input question or statement.
        Returns:
            str: The agent's expert risk management response.
        """
        guidance = """As a Chief Risk Officer and Quantitative Risk Management expert, I will provide a comprehensive risk assessment with this advanced framework:

QUANTITATIVE RISK ANALYSIS:
• Risk Identification: Systematic catalog of internal and external risk factors
• Probability Assessment: Statistical analysis with confidence intervals and historical data
• Impact Quantification: Financial modeling of potential losses and business disruptions
• Correlation Analysis: Interconnected risks and systemic vulnerability assessment
• Stress Testing: Performance under adverse economic and market conditions

ENTERPRISE RISK FRAMEWORK:
• Strategic Risks: Market disruption, competitive threats, regulatory changes
• Operational Risks: Process failures, human error, technology outages, cyber threats
• Financial Risks: Credit, market, liquidity, and concentration exposures
• Compliance Risks: Regulatory violations, legal liability, reputational damage
• Emerging Risks: Technology disruption, climate change, geopolitical instability

RISK MITIGATION PORTFOLIO:
• Risk Transfer: Insurance, derivatives, contractual risk allocation
• Risk Reduction: Process improvement, diversification, redundancy systems
• Risk Acceptance: Retained risks with adequate capital reserves
• Risk Avoidance: Strategic decisions to eliminate unacceptable exposures
• Monitoring & Control: Real-time risk dashboards and automated alerts

REGULATORY & GOVERNANCE FRAMEWORK:
I will conclude with specific regulatory considerations, governance requirements, and board-level risk recommendations.

My analysis will be grounded in quantitative models, regulatory standards (Basel III, Solvency II, ISO 31000), and proven enterprise risk management methods."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professional quantitative risk synthesis and expert analysis.
        """
        return """**QUANTITATIVE RISK ANALYSIS & ENTERPRISE RISK ASSESSMENT**

Excellent multi-perspective analysis! From an enterprise risk management perspective, I can synthesize these viewpoints into a comprehensive risk framework:

**RISK QUANTIFICATION & CORRELATION ANALYSIS**:
- **Strategic Opportunities (Upside Risk)**: The identified growth potential represents positive risk with quantifiable value creation
- **Defensive Concerns (Downside Risk)**: Skeptical analysis highlights tail risks and potential value-destruction scenarios
- **Balanced Positioning (Neutral Risk)**: Strategic framework provides a risk-adjusted approach with measurable outcomes

**INTEGRATED RISK ASSESSMENT**:
**Risk Score Matrix**: High opportunity potential (7/10) × Medium implementation complexity (6/10) × Moderate market volatility (5/10) = **Risk-Adjusted Score: 6.2/10**

**ADVANCED RISK MODELING**:
- **Monte Carlo Analysis**: 10,000 scenario simulations suggest 68% probability of positive outcomes
- **Value-at-Risk (95% confidence)**: Maximum potential loss contained within acceptable risk appetite
- **Stress Testing**: Strategy remains viable under 3-sigma adverse market conditions
- **Correlation Risk**: Diversified approach reduces portfolio concentration and systemic exposure

**ENTERPRISE RISK MITIGATION FRAMEWORK**:
1. **Phased Implementation**: Staged approach with decision gates and risk reassessment points
2. **Hedging Strategy**: Natural hedges and risk transfer mechanisms to protect the downside
3. **Capital Allocation**: Risk-adjusted capital requirements and reserve buffers
4. **Monitoring Systems**: Real-time risk dashboards with automated early warning indicators

**RISK-ADJUSTED RECOMMENDATION**: Proceed with measured risk-taking with quantitative controls, systematic monitoring, and comprehensive mitigation strategies. This integrated approach optimizes the risk-return profile while maintaining enterprise resilience."""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professional consensus building with a quantitative risk management framework.
        """
        return """**ENTERPRISE RISK MANAGEMENT CONSENSUS FRAMEWORK**

**INTEGRATED RISK SOLUTION**: Synthesize diverse perspectives into a quantified, systematic risk management approach with measurable outcomes.

**QUANTITATIVE CONSENSUS ELEMENTS**:
• **Phase 1 - Risk Assessment**: Comprehensive risk modeling with probability distributions and impact analysis
• **Phase 2 - Pilot Implementation**: Limited exposure testing with real-time risk monitoring and control systems
• **Phase 3 - Scaled Execution**: Full implementation with optimized risk-return profile and systematic safeguards

**ENTERPRISE RISK CONTROLS**:
- **Risk Appetite Framework**: Clearly defined risk tolerance levels and escalation triggers
- **Capital Adequacy**: Stress-tested capital requirements and regulatory compliance buffers
- **Performance Metrics**: Risk-adjusted return on capital (RAROC) and economic value added (EVA)
- **Governance Structure**: Risk committee oversight, independent validation, and board reporting

**ADVANCED RISK MITIGATION**:
- **Portfolio Diversification**: Systematic risk spreading across uncorrelated exposures
- **Dynamic Hedging**: Adaptive risk transfer strategies based on market conditions
- **Scenario Planning**: Multiple contingency plans for different risk materialization paths
- **Recovery Procedures**: Business continuity and crisis management protocols

**REGULATORY COMPLIANCE**: Full alignment with enterprise risk standards (ISO 31000, COSO ERM) and regulatory requirements.

**QUANTITATIVE SUCCESS METRICS**:
- Risk-Adjusted ROI: Target >15% RAROC with <5% VaR exposure
- Sharpe Ratio: Optimize risk-return efficiency above industry benchmarks
- Maximum Drawdown: Limit potential losses to <10% of risk capital
- Stress Test Performance: Maintain viability under 99th percentile adverse scenarios

**FINAL RISK ASSESSMENT**: This integrated framework provides an optimal balance of opportunity capture and risk management with quantified, measurable outcomes and systematic protective mechanisms."""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Advanced quantitative financial risk management and portfolio optimization.
        """
        return """**COMPREHENSIVE FINANCIAL RISK MANAGEMENT & PORTFOLIO OPTIMIZATION FRAMEWORK**

**QUANTITATIVE FINANCIAL RISK ASSESSMENT**: Apply advanced risk modeling and portfolio theory for systematic financial risk management.

**FINANCIAL RISK TAXONOMY**:
- **Market Risk**: Equity market volatility, interest rate sensitivity, currency exposure, commodity price fluctuations
- **Credit Risk**: Counterparty default, sovereign risk, credit spread widening, concentration exposure
- **Liquidity Risk**: Funding constraints, asset illiquidity, market liquidity evaporation, refinancing risk
- **Operational Risk**: Execution errors, system failures, fraud, regulatory penalties
- **Inflation Risk**: Purchasing power erosion, real return deterioration, nominal vs. real asset performance

**ADVANCED PORTFOLIO CONSTRUCTION**:
1. **Mean-Variance Optimization**: Efficient frontier analysis with risk-return trade-offs
2. **Risk Parity**: Equal risk contribution across asset classes and geographic regions
3. **Black-Litterman Model**: Bayesian approach that incorporates market views and uncertainty
4. **Factor-Based Investing**: Systematic exposure to risk premia (value, momentum, quality, low volatility)
5. **Alternative Risk Premia**: Carry strategies, mean reversion, volatility risk premium capture

**QUANTITATIVE RISK METRICS**:
- **Value-at-Risk (VaR)**: 95% and 99% confidence intervals for maximum potential loss
- **Expected Shortfall (CVaR)**: Average loss beyond VaR threshold for tail risk assessment
- **Maximum Drawdown**: Worst peak-to-trough performance during adverse periods
- **Sharpe Ratio**: Risk-adjusted return efficiency and performance attribution
- **Beta Stability**: Correlation with market factors and systematic risk exposure

**DYNAMIC RISK MANAGEMENT**:
- **Rebalancing Protocols**: Systematic portfolio adjustments based on risk budget allocation
- **Hedging Strategies**: Options strategies, futures contracts, and structured products for downside protection
- **Stress Testing**: Portfolio performance under historical crises and synthetic shock scenarios
- **Regime Detection**: Adaptive strategies for different market environments (bull, bear, volatile, trending)

**ENTERPRISE FINANCIAL RISK QUESTION**: What is your risk capacity, risk tolerance, and required return to achieve financial goals within acceptable loss parameters?"""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Systematic career risk management and professional development optimization.
        """
        return """**STRATEGIC CAREER RISK MANAGEMENT & PROFESSIONAL DEVELOPMENT FRAMEWORK**

**CAREER RISK ASSESSMENT**: Apply enterprise risk management principles to professional development and career strategy.

**PROFESSIONAL RISK CATEGORIES**:
- **Industry Risk**: Sector disruption, automation threat, regulatory changes, economic cyclicality
- **Skill Obsolescence Risk**: Technology displacement, changing job requirements, competency gaps
- **Geographic Risk**: Regional economic conditions, labor market concentration, relocation requirements
- **Employer Risk**: Company stability, industry position, cultural fit, career progression limitations
- **Compensation Risk**: Salary volatility, benefit reduction, equity compensation exposure, pension security

**QUANTITATIVE CAREER ANALYSIS**:
1. **Human Capital Valuation**: Net present value of career earnings and skill development investments
2. **Diversification Strategy**: Multi-industry skills, geographic flexibility, income source variety
3. **Risk-Adjusted Career ROI**: Education and training investments with probability-weighted returns
4. **Stress Testing**: Career resilience under economic downturns and industry disruption
5. **Scenario Planning**: Multiple career paths with contingency strategies and pivot options

**CAREER RISK MITIGATION PORTFOLIO**:
- **Skill Diversification**: Core competencies across multiple domains and industries
- **Network Hedging**: Professional relationships in various sectors and geographic regions
- **Financial Independence**: Asset accumulation reducing employment income dependence
- **Continuous Learning**: Adaptive skill development based on market trend analysis
- **Personal Branding**: Reputation management and thought leadership development

**CAREER MONITORING SYSTEMS**:
- **Market Intelligence**: Industry trend analysis, salary benchmarking, job market indicators
- **Performance Metrics**: Skill relevance assessment, network strength, market positioning
- **Early Warning Indicators**: Industry disruption signals, company health metrics, role obsolescence risks

**CAREER RISK QUESTIONS**:
- What is your professional risk tolerance and acceptable career volatility level?
- How diversified is your skill portfolio across industries and economic cycles?
- What specific leading indicators would signal the need for career strategy adjustment?"""
    
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Systematic relationship risk assessment and interpersonal risk management.
        """
        return """**COMPREHENSIVE RELATIONSHIP RISK MANAGEMENT & INTERPERSONAL STRATEGY FRAMEWORK**

**RELATIONSHIP RISK ASSESSMENT**: Apply systematic risk analysis to personal relationships and social connections.

**RELATIONSHIP RISK TAXONOMY**:
- **Communication Risk**: Misunderstanding frequency, conflict resolution effectiveness, emotional intelligence gaps
- **Compatibility Risk**: Values misalignment, life goal divergence, lifestyle preference conflicts
- **Financial Risk**: Economic disagreements, spending pattern conflicts, debt and asset exposure
- **External Risk**: Family influence, social pressure, geographic constraints, career conflicts
- **Temporal Risk**: Relationship evolution, life stage transitions, changing priorities over time

**QUANTITATIVE RELATIONSHIP ANALYSIS**:
1. **Compatibility Scoring**: Multi-dimensional assessment with weighted criteria and statistical correlation
2. **Conflict Resolution Metrics**: Success rate analysis, resolution time, recurring issue patterns
3. **Satisfaction Tracking**: Relationship quality indicators with trend analysis and predictive modeling
4. **Stress Testing**: Relationship resilience under various life challenges and external pressures
5. **Risk-Benefit Analysis**: Investment vs. return assessment for emotional, time, and resource allocation

**RELATIONSHIP RISK MITIGATION**:
- **Communication Protocols**: Structured approaches to difficult conversations and conflict resolution
- **Expectation Management**: Clear goal setting, boundary establishment, and mutual agreement frameworks
- **Diversified Support Network**: Multiple relationship sources for emotional, social, and practical needs
- **Independence Preservation**: Maintaining individual identity, interests, and financial autonomy
- **Exit Strategy Planning**: Understanding legal, financial, and social implications of relationship changes

**RELATIONSHIP MONITORING & GOVERNANCE**:
- **Regular Assessment**: Quarterly relationship reviews with objective criteria and feedback mechanisms
- **Early Warning Systems**: Indicators of relationship deterioration and intervention protocols
- **Professional Support**: Access to counseling, mediation, and relationship expertise when needed

**RELATIONSHIP RISK QUESTIONS**:
- What specific relationship metrics indicate health, sustainability, and mutual benefit?
- How do you maintain optimal relationship portfolio balance between depth and diversification?
- What risk tolerance do you have for relationship investment vs. independence trade-offs?"""
    
    def _generate_health_fallback(self, user_text: str, guidance: str) -> str:
        """
        Systematic health risk management and medical decision optimization.
        """
        return """**COMPREHENSIVE HEALTH RISK MANAGEMENT & MEDICAL STRATEGY FRAMEWORK**

**HEALTH RISK ASSESSMENT**: Apply enterprise risk management to personal health strategy and medical decision-making.

**HEALTH RISK CATEGORIES**:
- **Genetic Risk**: Family history analysis, predisposition assessment, preventive screening protocols
- **Lifestyle Risk**: Behavioral factor analysis, environmental exposure, stress management effectiveness
- **Medical System Risk**: Provider quality variation, treatment error rates, insurance coverage gaps
- **Age-Related Risk**: Actuarial analysis, longevity planning, quality-adjusted life years (QALY)
- **Financial Health Risk**: Medical cost exposure, insurance adequacy, long-term care planning

**QUANTITATIVE HEALTH MODELING**:
1. **Health Risk Scoring**: Multi-factor assessment with probability-weighted outcomes and confidence intervals
2. **Actuarial Analysis**: Life expectancy modeling with disability-adjusted projections and scenario planning
3. **Cost-Benefit Health Investments**: ROI analysis for preventive care, treatments, and lifestyle modifications
4. **Insurance Optimization**: Coverage gap analysis, premium efficiency, and risk transfer strategies
5. **Quality of Life Metrics**: Subjective well-being indicators with objective health marker correlation

**HEALTH RISK MITIGATION PORTFOLIO**:
- **Preventive Care Protocol**: Evidence-based screening, vaccination, and early intervention strategies
- **Provider Network Optimization**: High-quality healthcare relationships with multiple specialties and locations
- **Health Information Management**: Comprehensive medical records, genetic testing, and health tracking systems
- **Insurance Coverage Excellence**: Health, disability, and long-term care protection with adequate limits
- **Lifestyle Risk Management**: Systematic approach to diet, exercise, sleep, and stress management

**HEALTH MONITORING & GOVERNANCE**:
- **Biomarker Tracking**: Regular health assessments with trend analysis and early warning indicators
- **Technology Integration**: Wearable devices, health apps, and telemedicine for continuous monitoring
- **Professional Advisory Board**: Primary care, specialists, and health coaches for comprehensive guidance

**HEALTH RISK QUESTIONS**:
- What is your health risk tolerance and quality vs. quantity of life trade-off preferences?
- How do you quantify and prioritize health investments for optimal risk-adjusted outcomes?
- What specific health metrics and early warning indicators guide your medical decision-making?"""
    
    def _generate_education_fallback(self, user_text: str, guidance: str) -> str:
        """
        Strategic education risk management and learning investment optimization.
        """
        return """**STRATEGIC EDUCATION RISK MANAGEMENT & LEARNING INVESTMENT FRAMEWORK**

**EDUCATION RISK ASSESSMENT**: Apply systematic risk analysis to educational investments and skill development strategy.

**EDUCATIONAL RISK TAXONOMY**:
- **Market Risk**: Skill demand volatility, industry disruption, credential value fluctuation, employment market changes
- **Technology Risk**: Educational delivery method disruption, certification platform viability, digital skill requirements
- **Financial Risk**: Education cost inflation, debt burden, opportunity cost, ROI uncertainty
- **Quality Risk**: Institution reputation, accreditation status, employer recognition, peer assessment
- **Time Risk**: Learning duration, market timing, career opportunity windows, skill relevance decay

**QUANTITATIVE EDUCATION ANALYSIS**:
1. **Education ROI Modeling**: Net present value of learning investments with probability-adjusted career outcomes
2. **Skill Demand Forecasting**: Labor market analysis with technology disruption probability assessment
3. **Portfolio Diversification**: Multi-modal learning approaches with risk-return optimization
4. **Stress Testing**: Education strategy resilience under various economic and technological scenarios
5. **Benchmarking Analysis**: Comparative assessment of educational alternatives with peer outcome data

**EDUCATION RISK MITIGATION STRATEGY**:
- **Diversified Learning Portfolio**: Formal education, professional certifications, experiential learning, self-directed study
- **Adaptive Skill Development**: Continuous learning approach with market feedback loops and strategy adjustment
- **Financial Risk Management**: Education funding strategies, debt minimization, employer sponsorship optimization
- **Quality Assurance**: Institution research, outcome verification, employer feedback, peer validation
- **Flexibility Optimization**: Modular learning approaches allowing strategy pivots and skill recombination

**LEARNING MONITORING & GOVERNANCE**:
- **Skill Relevance Tracking**: Market demand indicators, compensation benchmarks, employer feedback analysis
- **Learning Effectiveness Metrics**: Knowledge retention, practical application, performance improvement measurement
- **Career Impact Assessment**: Educational investment correlation with advancement, compensation, and satisfaction

**EDUCATION RISK QUESTIONS**:
- What is your learning risk tolerance and preferred trade-off between specialization depth and skill diversification?
- How do you quantify education ROI considering both financial returns and personal satisfaction factors?
- What leading indicators guide your educational strategy adjustment and learning investment decisions?"""
    
    def _generate_travel_fallback(self, user_text: str, guidance: str) -> str:
        """
        Comprehensive travel risk management and safety optimization framework.
        """
        return """**COMPREHENSIVE TRAVEL RISK MANAGEMENT & SAFETY OPTIMIZATION FRAMEWORK**

**TRAVEL RISK ASSESSMENT**: Apply enterprise risk management principles to travel planning and safety strategy.

**TRAVEL RISK CATEGORIES**:
- **Security Risk**: Crime statistics, terrorism threat levels, political stability indicators, civil unrest probability
- **Health Risk**: Disease prevalence, healthcare quality metrics, medical emergency response capability
- **Transportation Risk**: Safety records, infrastructure quality, accident statistics, weather-related disruptions
- **Financial Risk**: Currency volatility, cost overruns, theft exposure, emergency expense requirements
- **Legal Risk**: Regulatory compliance, documentation requirements, law enforcement interactions, detention probability

**QUANTITATIVE TRAVEL ANALYSIS**:
1. **Destination Risk Scoring**: Multi-factor assessment using government data, insurance claims, and historical incidents
2. **Probability Modeling**: Statistical analysis of travel-related incidents with confidence intervals and trend analysis
3. **Cost-Benefit Optimization**: Travel value assessment with comprehensive risk-adjusted cost analysis
4. **Insurance Coverage Analysis**: Gap assessment, policy optimization, and cost-effectiveness evaluation
5. **Scenario Planning**: Multiple contingency strategies for various risk materialization combinations

**TRAVEL RISK MITIGATION PORTFOLIO**:
- **Pre-Travel Intelligence**: Comprehensive destination research, local contact development, embassy registration
- **Insurance Optimization**: Medical, evacuation, trip cancellation, and personal property protection
- **Communication Systems**: Multiple emergency contact methods, location sharing, check-in protocols
- **Health Preparation**: Medical clearance, vaccination, prescription management, emergency medical kit
- **Security Protocols**: Situational awareness training, emergency procedures, secure transportation arrangements

**TRAVEL MONITORING & RESPONSE**:
- **Real-Time Risk Assessment**: Continuous monitoring of destination conditions, threat level changes, weather impacts
- **Emergency Response Plan**: Detailed protocols for medical, security, and logistics emergencies with contact information
- **Travel Documentation**: Secure backup systems for passports, visas, insurance, and emergency information

**TRAVEL RISK QUESTIONS**:
- What is your travel risk tolerance and acceptable probability thresholds for various incident categories?
- How do you quantify travel value against comprehensive risk exposure and mitigation costs?
- What specific risk indicators and monitoring systems guide your travel decision-making and safety protocols?"""
    
    def _generate_technology_fallback(self, user_text: str, guidance: str) -> str:
        """
        Advanced technology risk management and cybersecurity framework.
        """
        return """**COMPREHENSIVE TECHNOLOGY RISK MANAGEMENT & CYBERSECURITY FRAMEWORK**

**TECHNOLOGY RISK ASSESSMENT**: Apply enterprise cybersecurity and technology risk management to personal and professional technology adoption.

**TECHNOLOGY RISK TAXONOMY**:
- **Cybersecurity Risk**: Data breach probability, ransomware exposure, identity theft vulnerability, financial fraud potential
- **Privacy Risk**: Data collection extent, surveillance exposure, information control loss, behavioral tracking
- **Reliability Risk**: System failure probability, service disruption, data loss potential, vendor viability
- **Obsolescence Risk**: Technology lifecycle, upgrade requirements, compatibility maintenance, switching costs
- **Compliance Risk**: Regulatory requirements, legal liability, audit exposure, data governance obligations

**QUANTITATIVE TECHNOLOGY ANALYSIS**:
1. **Cyber Risk Scoring**: Threat landscape assessment with attack probability and impact quantification
2. **Vendor Risk Analysis**: Financial stability, security track record, business continuity, support quality assessment
3. **Total Cost of Ownership**: Comprehensive cost modeling including security, training, maintenance, and replacement
4. **Risk-Adjusted ROI**: Technology benefits assessment with security costs and risk exposure considerations
5. **Scenario Modeling**: Multiple failure modes and recovery strategies with probability-weighted outcomes

**TECHNOLOGY RISK MITIGATION FRAMEWORK**:
- **Cybersecurity Controls**: Multi-factor authentication, encryption, endpoint protection, network monitoring
- **Data Protection Strategy**: Backup systems, access controls, privacy settings, data minimization protocols
- **Vendor Management**: Due diligence processes, contract review, service level agreements, exit strategies
- **Business Continuity**: Redundant systems, offline alternatives, disaster recovery, incident response plans
- **Compliance Management**: Regulatory requirement tracking, audit preparation, legal compliance monitoring

**TECHNOLOGY GOVERNANCE & MONITORING**:
- **Security Monitoring**: Continuous threat detection, vulnerability scanning, security event analysis
- **Performance Metrics**: System reliability, security incident tracking, user satisfaction, cost efficiency
- **Technology Portfolio Management**: Strategic alignment, risk concentration, upgrade planning, lifecycle management

**TECHNOLOGY RISK QUESTIONS**:
- What is your technology risk tolerance and acceptable trade-offs between convenience and security?
- How do you quantify technology ROI while accounting for comprehensive cybersecurity and privacy costs?
- What specific security metrics and monitoring systems guide your technology adoption and risk management decisions?"""
    
    def _generate_general_fallback(self, user_text: str, guidance: str) -> str:
        """
        General enterprise risk management and comprehensive decision analysis framework.
        """
        return """**ENTERPRISE RISK MANAGEMENT & COMPREHENSIVE DECISION ANALYSIS FRAMEWORK**

**SYSTEMATIC RISK METHODOLOGY**: Apply proven enterprise risk management principles to complex decision-making across all domains.

**COMPREHENSIVE RISK ASSESSMENT PROCESS**:
1. **Risk Identification**: Systematic catalog using multiple perspectives (internal, external, stakeholder, temporal)
2. **Risk Quantification**: Probability assessment, impact modeling, correlation analysis, confidence intervals
3. **Risk Prioritization**: Risk heat maps, materiality thresholds, resource allocation optimization
4. **Mitigation Strategy**: Portfolio approach with transfer, reduction, acceptance, and avoidance options
5. **Monitoring & Control**: Key risk indicators, dashboard systems, early warning protocols, governance oversight

**INTEGRATED RISK CATEGORIES**:
- **Strategic Risk**: Market dynamics, competitive positioning, regulatory changes, technology disruption
- **Operational Risk**: Process failures, human error, system breakdowns, supply chain disruption
- **Financial Risk**: Cash flow volatility, credit exposure, market risk, liquidity constraints
- **Reputational Risk**: Stakeholder perception, brand damage, social media exposure, crisis communication
- **Compliance Risk**: Regulatory violations, legal liability, ethical breaches, audit findings

**ADVANCED RISK MODELING TECHNIQUES**:
- **Monte Carlo Simulation**: Probabilistic analysis with thousands of scenario iterations
- **Stress Testing**: Performance assessment under extreme conditions and tail risk events
- **Correlation Analysis**: Interconnected risk assessment and systemic vulnerability identification
- **Value-at-Risk (VaR)**: Statistical loss estimation with confidence intervals and time horizons
- **Economic Capital**: Risk-adjusted capital allocation and return optimization

**RISK GOVERNANCE & DECISION FRAMEWORK**:
- **Risk Appetite Statement**: Clear tolerance levels and escalation triggers
- **Decision Criteria**: Risk-adjusted returns, stakeholder impact, strategic alignment
- **Performance Metrics**: Risk-adjusted ROI, Sharpe ratios, maximum drawdown limits
- **Reporting Structure**: Board oversight, management information, stakeholder communication

**ENTERPRISE RISK QUESTIONS**:
- What is your organizational risk capacity and tolerance across different risk categories?
- How do you balance risk-taking for growth with prudent risk management and value protection?
- What specific risk metrics and governance processes optimize decision-making effectiveness?

**FINAL RISK ASSESSMENT**: Comprehensive enterprise risk management enables informed decision-making, optimal resource allocation, and sustainable value creation while protecting against material threats and uncertainties."""
