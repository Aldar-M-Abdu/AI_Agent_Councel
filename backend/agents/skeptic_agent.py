from .base_agent import BaseAgent

class SkepticAgent(BaseAgent):
    """
    Chief Risk Officer and Critical Analysis expert specializing in threat assessment,
    vulnerability analysis, and defensive strategy. Focuses on protecting value and preventing losses.
    """
    def __init__(self):
        super().__init__(
            agent_name="Skeptic Agent", 
            system_prompt="""You are a Chief Risk Officer (CRO) and Critical Analysis expert with 20+ years of experience protecting large enterprises from strategic threats.

IMPORTANT: Always respond in English. Use professional English terminology in risk and security areas.

Your expertise includes:

CORE COMPETENCIES:
• Enterprise Risk Management (ERM) & Compliance
• Cybersecurity & Information Security Strategy
• Financial Risk Analysis & Stress Testing
• Operational Risk Assessment & Business Continuity
• Strategic Threat Intelligence & Competitive Analysis
• Crisis Management & Contingency Planning
• Regulatory Compliance & Legal Risk Mitigation
• Due Diligence & Investigative Methods

CRITICAL ANALYSIS METHODOLOGY:
1. THREAT IDENTIFICATION: Systematically identify internal and external risks with established frameworks
2. VULNERABILITY ASSESSMENT: Analyze weaknesses in systems, processes, and strategic positions
3. IMPACT ANALYSIS: Quantify potential losses and consequences with probabilistic models
4. DEFENSIVE STRATEGY: Develop multi-layered protection and mitigation strategies
5. CONTINGENCY PLANNING: Create response protocols for various failure scenarios

RISK PHILOSOPHY:
• Evidence-Based Skepticism: Challenge assumptions with data and historical precedents
• Defense in Depth: Multiple layers of protection against potential threats
• Worst-Case Preparedness: Plan for low-probability, high-impact scenarios
• Continuous Vigilance: Ongoing monitoring and threat landscape assessment
• Cautious Conservatism: Protect existing value before pursuing risky opportunities

COMMUNICATION STYLE:
• Direct and analytically rigorous with supporting evidence
• Reference historical failures, case studies, and lessons learned
• Provide specific risk metrics and probability assessments
• Include concrete mitigation strategies and control measures
• Ask probing questions to reveal hidden vulnerabilities
• Emphasize protective measures and downside protection

RISK ASSESSMENT FRAMEWORK:
For each analysis, deliver:
- Comprehensive Risk Register with probability × impact scores
- Threat landscape analysis (competitors, market, regulatory)
- Vulnerability assessment with exploitability ratings
- Defensive Strategy with layered protective measures
- Contingency plans for various failure scenarios
- Monitoring systems for early warning indicators

Always maintain analytical rigor while providing actionable protective strategies grounded in proven risk management methods."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Critical risk analysis & Threat assessment with defensive strategy, vulnerability identification, and loss prevention methods"

    def generate_response(self, user_text: str) -> str:
        """
        Generate a critical analysis and risk assessment response.
        Args:
            user_text (str): The user's input question or statement.
        Returns:
            str: The agent's risk analysis response.
        """
        guidance = """As a Chief Risk Officer and Critical Analysis expert, I will provide a comprehensive risk assessment with this framework:

THREAT LANDSCAPE ANALYSIS:
• Market risks & Competitive threats
• Operational Vulnerabilities & System failures
• Financial Exposures & Liquidity risks
• Regulatory Changes & Compliance gaps
• Reputational risks & Stakeholder concerns

CRITICAL RISK ASSESSMENT:
• High-Impact Scenarios: Low-probability events with severe consequences
• Medium-Probability Risks: Likely challenges requiring immediate attention
• Systemic Vulnerabilities: Interconnected risks that can cascade
• Control Failures: Points where existing protections may break down
• External Shocks: Market disruptions and environmental factors

DEFENSIVE STRATEGY FRAMEWORK:
• Risk Mitigation: Reduce probability of adverse events
• Impact Limitation: Minimize consequences when risks materialize
• Contingency Planning: Response protocols for various scenarios
• Monitoring Systems: Early warning indicators and dashboards
• Recovery Procedures: Business continuity and restoration plans

CRITICAL ANALYSIS QUESTIONS:
I will conclude with challenging questions designed to stress-test assumptions and reveal potential blind spots.

My assessment will be grounded in historical precedents, statistical analysis, and proven risk management frameworks while maintaining analytical objectivity."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professional critical analysis and risk synthesis.
        """
        return """**CRITICAL RISK ASSESSMENT & THREAT ANALYSIS**

While I appreciate the strategic vision and optimistic projections, my risk analysis reveals several critical vulnerabilities that require immediate attention:

**STRATEGIC RISK EVALUATION**: The growth opportunities identified are compelling, but the risk-reward calculations may be overly optimistic. Historical data shows that 70% of strategic initiatives fail to meet projections due to execution risks and market volatility.

**VULNERABILITY IDENTIFICATION**:
- **Overconfidence Bias**: Optimistic scenarios often underestimate implementation complexity
- **Market Timing Risk**: Economic cycles and competitive responses can derail even well-planned strategies
- **Resource Strain**: Aggressive growth can overextend capabilities and jeopardize core operations
- **Regulatory Exposure**: Rapid expansion often triggers compliance issues and regulatory scrutiny

**DEFENSIVE STRATEGY REQUIREMENTS**:
- **Stress Testing**: All projections should be tested against adverse scenarios
- **Downside Protection**: Establish clear stop-loss criteria and exit strategies
- **Resource Reserves**: Maintain adequate capital buffers for unexpected challenges
- **Incremental Validation**: Phased implementation with go/no-go decision points

**CRITICAL RISK QUESTIONS**:
1. What specific evidence supports the optimistic market projections beyond anecdotal success stories?
2. How will we detect warning signs that assumptions are breaking down?
3. What happens if we are wrong about market timing or competitive response?

**RISK-ADJUSTED RECOMMENDATION**: Proceed with extreme caution, robust monitoring, and comprehensive contingency planning. Protection of existing value must take priority over speculative opportunities."""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professional consensus building with a risk management framework.
        """
        return """**RISK-ADJUSTED CONSENSUS FRAMEWORK**

**DEFENSIVE INTEGRATION STRATEGY**: While growth opportunities are acknowledged, we must prioritize risk mitigation and downside protection.

**CRITICAL CONSENSUS ELEMENTS**:
• **Phase 1 - Risk Assessment**: Comprehensive due diligence and vulnerability analysis
• **Phase 2 - Controlled Testing**: Limited-exposure pilot with strict risk controls
• **Phase 3 - Conditional Scaling**: Expansion only after validation of risk assumptions

**MANDATORY RISK CONTROLS**:
- **Investment Limits**: Cap resource exposure at acceptable loss levels
- **Performance Triggers**: Automatic review points based on leading indicators
- **Exit Protocols**: Predefined criteria for stopping or pivoting strategies
- **Monitoring Systems**: Real-time dashboards for early warning detection

**PROTECTIVE MECHANISMS**: Implement multiple defense layers including financial controls, operational safeguards, and strategic hedges against adverse outcomes.

**NON-NEGOTIABLE REQUIREMENTS**:
- Comprehensive insurance coverage for identified risks
- Legal review of all contractual commitments
- Independent validation of key assumptions
- Board-level oversight of major strategic decisions

**SKEPTICAL VALIDATION**: Every optimistic assumption must be challenged with historical data, competitive analysis, and worst-case scenario planning.

**FINAL RISK ASSESSMENT**: Progress is possible, but only with robust risk management discipline and conservative resource allocation. Protect what we have before chasing what we might win."""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical financial risk analysis and protective strategies.
        """
        return """**COMPREHENSIVE FINANCIAL RISK ASSESSMENT & PROTECTION STRATEGY**

**CRITICAL FINANCIAL THREATS**: Financial markets are fundamentally unpredictable and historical performance provides no guarantee of future results.

**HIGH-RISK FINANCIAL VULNERABILITIES**:
- **Market Volatility**: Economic cycles can destroy decades of gains in months
- **Inflation Erosion**: Currency devaluation reduces real purchasing power over time
- **Liquidity Crises**: Inability to access capital when it is needed most
- **Behavioral Biases**: Emotional decisions often lead to permanent capital loss
- **Concentration Risk**: Overexposure to single assets, sectors, or strategies

**DEFENSIVE FINANCIAL STRATEGY**:
1. **Capital Preservation**: Prioritize protection of existing wealth over aggressive growth
2. **Diversification Excellence**: Spread risk across uncorrelated asset classes and geographies
3. **Liquidity Management**: Maintain significant emergency reserves (12+ months of expenses)
4. **Stress Testing**: Model portfolio performance under various crisis scenarios
5. **Professional Oversight**: Independent financial advisors with fiduciary responsibility

**FINANCIAL PROTECTIVE MEASURES**:
- **Insurance Coverage**: Comprehensive protection against disability, liability, and property loss
- **Legal Structures**: Asset protection strategies and estate planning
- **Tax Efficiency**: Minimize tax drag on investment returns
- **Debt Management**: Conservative leverage ratios and fixed-rate financing

**CRITICAL FINANCIAL QUESTIONS**:
- What percentage of your portfolio can you afford to lose without affecting your lifestyle?
- How will you maintain discipline during market euphoria or panic?
- What specific events could force you to liquidate investments at unfavorable prices?

**RISK REALITY CHECK**: Most investment strategies fail due to poor timing, excessive fees, or emotional decision-making. Focus on what you can control: costs, taxes, and risk management."""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical career risk analysis and defensive strategies.
        """
        return """**STRATEGIC CAREER RISK ASSESSMENT & DEFENSIVE POSITIONING**

**CAREER THREAT LANDSCAPE**: Professional markets are increasingly volatile with accelerating technological disruption and economic uncertainty.

**CRITICAL CAREER VULNERABILITIES**:
- **Skill Obsolescence**: Automation and AI threaten traditional job categories
- **Industry Disruption**: Entire sectors can become obsolete within decades
- **Ageism Reality**: Career advancement becomes significantly harder after 45-50
- **Economic Volatility**: Recessions disproportionately impact newer employees
- **Geographic Concentration**: Over-dependence on single markets or employers

**DEFENSIVE CAREER STRATEGY**:
1. **Skill Diversification**: Develop capabilities across multiple domains and industries
2. **Network Insurance**: Maintain relationships across various companies and sectors
3. **Financial Independence**: Build assets that reduce dependence on employment income
4. **Reputation Protection**: Avoid risky career moves that could damage professional standing
5. **Continuous Validation**: Regularly test market value through interviews and consulting

**CAREER PROTECTION MEASURES**:
- **Emergency Fund**: 12+ months of living expenses for career transitions
- **Portable Benefits**: Retirement accounts, health insurance, and professional certifications
- **Legal Protection**: Understanding of employment law and contract terms
- **Performance Documentation**: Detailed records of achievements and contributions

**CRITICAL CAREER QUESTIONS**:
- What happens to your financial security if your industry experiences major disruption?
- How quickly could you find equivalent employment if your position was eliminated?
- What specific skills do you have that cannot be easily automated or outsourced?

**CAREER REALITY CHECK**: Most career changes result in temporary income reduction and require 2-3 years to recover previous compensation levels. Plan conservatively and maintain strong defensive positioning."""
    
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical relationship risk analysis and protective strategies.
        """
        return """**COMPREHENSIVE RELATIONSHIP RISK ASSESSMENT & PROTECTION FRAMEWORK**

**RELATIONSHIP THREAT ANALYSIS**: Personal relationships involve significant emotional, financial, and social risks that require careful management.

**CRITICAL RELATIONSHIP VULNERABILITIES**:
- **Communication Breakdown**: Most relationships fail due to unresolved conflicts and poor communication
- **Financial Stress**: Money disagreements are a primary cause of relationship dissolution
- **Life Stage Misalignment**: Different goals and timelines create irreconcilable differences
- **External Pressures**: Family, career, and social influences can destabilize relationships
- **Unrealistic Expectations**: Romantic idealization often leads to disappointment and conflict

**RELATIONSHIP RISK MITIGATION**:
1. **Expectation Management**: Establish realistic goals and boundaries based on historical patterns
2. **Financial Protection**: Maintain separate assets and clear financial agreements
3. **Communication Protocols**: Structured approaches to conflict resolution and decision-making
4. **Independence Preservation**: Maintain individual identity, interests, and support networks
5. **Exit Planning**: Understand legal and financial implications of relationship dissolution

**PROTECTIVE RELATIONSHIP MEASURES**:
- **Prenuptial Agreements**: Legal protection of assets and financial interests
- **Regular Relationship Audits**: Honest assessment of compatibility and satisfaction
- **Professional Counseling**: Objective guidance for major relationship decisions
- **Support Network Diversification**: Avoid over-dependence on a single relationship for emotional needs

**CRITICAL RELATIONSHIP QUESTIONS**:
- What specific behaviors or changes would make this relationship unacceptable to you?
- How would you maintain financial and emotional stability if this relationship ended?
- What evidence do you have that core compatibility issues can be resolved?

**RELATIONSHIP REALITY CHECK**: Statistics show that 50% of marriages end in divorce, and most long-term relationships experience significant challenges. Protect your interests while maintaining realistic expectations about relationship permanence."""
    
    def _generate_health_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical health risk analysis and medical protection strategies.
        """
        return """**COMPREHENSIVE HEALTH RISK ASSESSMENT & MEDICAL PROTECTION STRATEGY**

**HEALTH THREAT LANDSCAPE**: Healthcare is expensive, often ineffective, and subject to significant fraud and misinformation.

**CRITICAL HEALTH VULNERABILITIES**:
- **Chronic Disease Risk**: Lifestyle-related illnesses affect 60% of adults and worsen with age
- **Medical Error Exposure**: Healthcare mistakes are a leading cause of death in developed countries
- **Insurance Limitations**: Coverage gaps and cost escalation threaten financial security
- **Treatment Complexity**: Many interventions have limited efficacy and significant side effects
- **Genetic Predispositions**: Family history creates unavoidable risk factors for serious conditions

**DEFENSIVE HEALTH STRATEGY**:
1. **Prevention Excellence**: Focus on proven interventions with the strongest evidence base
2. **Medical Skepticism**: Question all recommendations and seek second opinions for major decisions
3. **Insurance Optimization**: Comprehensive coverage including disability and long-term care protection
4. **Provider Quality**: Research physician credentials, hospital ratings, and treatment outcomes
5. **Self-Advocacy**: Become an educated healthcare consumer with detailed medical records

**HEALTH PROTECTION MEASURES**:
- **Emergency Preparedness**: Advance directives, medical power of attorney, and emergency contacts
- **Financial Protection**: Health savings accounts and medical expense insurance
- **Quality Validation**: Independent research on treatment options and provider quality
- **Risk Factor Management**: Address modifiable risks while accepting genetic limitations

**CRITICAL HEALTH QUESTIONS**:
- What specific evidence supports this treatment recommendation beyond anecdotal reports?
- How will you maintain quality of life if this health intervention fails or causes complications?
- What are the long-term costs and side effects of proposed treatments?

**HEALTH REALITY CHECK**: Most health problems worsen over time despite medical intervention. Focus on proven prevention strategies while maintaining skepticism about miracle cures and expensive treatments with limited evidence."""
    
    def _generate_education_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical education risk analysis and learning protection strategies.
        """
        return """**STRATEGIC EDUCATION RISK ASSESSMENT & LEARNING PROTECTION FRAMEWORK**

**EDUCATIONAL THREAT ANALYSIS**: Education markets are oversaturated with questionable quality and declining economic returns on investment.

**CRITICAL EDUCATION VULNERABILITIES**:
- **Credential Inflation**: Degree requirements increase while job market value decreases
- **Skills Mismatch**: Academic learning often lacks practical workplace application
- **Debt Accumulation**: Student loans create long-term financial burden with uncertain returns
- **Technology Disruption**: Online alternatives reduce value of traditional educational institutions
- **Market Saturation**: Oversupply of graduates in many fields depresses compensation

**DEFENSIVE EDUCATION STRATEGY**:
1. **ROI Analysis**: Calculate realistic cost-benefit ratios for educational investments
2. **Skill Validation**: Prioritize learning with immediate practical application and market demand
3. **Debt Avoidance**: Minimize educational debt through scholarships, employer funding, and alternative credentials
4. **Quality Assessment**: Research employment outcomes, graduation rates, and employer satisfaction
5. **Flexible Learning**: Choose options that allow career advancement without significant opportunity costs

**EDUCATION PROTECTION MEASURES**:
- **Financial Limits**: Cap educational spending at levels that don't compromise financial security
- **Performance Tracking**: Monitor learning progress and market relevance of acquired skills
- **Alternative Validation**: Consider certifications, apprenticeships, and portfolio-based credentials
- **Market Research**: Analyze employment trends and compensation data for target fields

**CRITICAL EDUCATION QUESTIONS**:
- What specific evidence shows this educational investment will increase earning potential?
- How will you recover costs if the credential fails to provide expected career advancement?
- What alternative learning paths could achieve similar outcomes with lower risk and cost?

**EDUCATION REALITY CHECK**: Many educational programs fail to deliver promised outcomes while creating significant financial obligations. Focus on practical skill development with proven market value rather than prestigious credentials with questionable ROI."""
    
    def _generate_travel_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical travel risk analysis and safety protection strategies.
        """
        return """**COMPREHENSIVE TRAVEL RISK ASSESSMENT & SAFETY PROTECTION FRAMEWORK**

**TRAVEL THREAT LANDSCAPE**: International travel involves significant safety, health, financial, and legal risks that are often underestimated.

**CRITICAL TRAVEL VULNERABILITIES**:
- **Security Threats**: Crime, terrorism, and political instability in many destinations
- **Health Hazards**: Disease exposure, medical emergencies, and inadequate healthcare systems
- **Financial Exposure**: Currency fluctuation, theft, fraud, and unexpected expenses
- **Legal Risks**: Arrest, detention, and legal system differences in foreign countries
- **Transportation Dangers**: Accident rates, safety standards, and infrastructure quality variations

**DEFENSIVE TRAVEL STRATEGY**:
1. **Risk Assessment**: Comprehensive research on destination safety, health, and political conditions
2. **Insurance Coverage**: Travel medical, evacuation, and trip cancellation protection
3. **Safety Protocols**: Communication plans, emergency contacts, and situation awareness training
4. **Health Precautions**: Vaccinations, medical kit, and healthcare facility identification
5. **Legal Preparation**: Document backup, embassy registration, and legal emergency contacts

**TRAVEL PROTECTION MEASURES**:
- **Emergency Funds**: Accessible cash reserves for unexpected situations
- **Communication Systems**: Multiple ways to contact help (satellite phone, embassy, family)
- **Health Documentation**: Medical records, prescription information, and emergency contacts
- **Security Awareness**: Training on common scams, dangerous areas, and threat recognition

**CRITICAL TRAVEL QUESTIONS**:
- What specific emergency protocols will you follow if serious problems arise?
- How will you handle medical emergencies in countries with poor healthcare systems?
- What evidence suggests this destination is safe for travelers with your profile?

**TRAVEL REALITY CHECK**: Travel insurance claims data show that medical emergencies, theft, and trip cancellations are common occurrences. Many destinations marketed as safe have significant unreported crime and infrastructure problems affecting tourists."""
    
    def _generate_technology_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical technology risk analysis and security protection strategies.
        """
        return """**COMPREHENSIVE TECHNOLOGY RISK ASSESSMENT & CYBERSECURITY PROTECTION FRAMEWORK**

**TECHNOLOGY THREAT LANDSCAPE**: Digital systems are inherently vulnerable to cyberattacks, data breaches, and technological obsolescence.

**CRITICAL TECHNOLOGY VULNERABILITIES**:
- **Cybersecurity Threats**: Ransomware, identity theft, and financial fraud targeting individuals and organizations
- **Privacy Erosion**: Data collection, surveillance, and loss of personal information control
- **System Dependencies**: Over-reliance on technology creates failure points and service disruptions
- **Obsolescence Risk**: Rapid technological change makes investments quickly outdated
- **Vendor Lock-in**: Proprietary systems create expensive switching costs and reduced flexibility

**DEFENSIVE TECHNOLOGY STRATEGY**:
1. **Security-First Approach**: Implement robust cybersecurity measures before adoption
2. **Privacy Protection**: Minimize data exposure and maintain control over personal information
3. **Redundancy Planning**: Backup systems and offline alternatives for critical functions
4. **Vendor Assessment**: Evaluate company stability, security practices, and exit strategies
5. **Cost-Benefit Analysis**: Calculate total ownership costs including security, training, and replacement

**TECHNOLOGY PROTECTION MEASURES**:
- **Multi-Factor Authentication**: Enhanced security for all critical accounts and systems
- **Regular Backups**: Offline data protection against ransomware and system failures
- **Security Monitoring**: Continuous surveillance for threats and unauthorized access
- **Privacy Controls**: Strict limits on data sharing and tracking permissions

**CRITICAL TECHNOLOGY QUESTIONS**:
- What specific security vulnerabilities does this technology introduce to your systems?
- How will you maintain functionality if this technology fails or becomes unavailable?
- What evidence suggests this vendor will remain viable and secure long-term?

**TECHNOLOGY REALITY CHECK**: Most technology implementations experience security breaches, cost overruns, and functionality problems. Focus on proven solutions with strong security track records rather than cutting-edge technologies with unproven reliability."""
    
    def _generate_general_fallback(self, user_text: str, guidance: str) -> str:
        """
        General critical analysis and comprehensive risk assessment.
        """
        return """**COMPREHENSIVE RISK ASSESSMENT & CRITICAL ANALYSIS FRAMEWORK**

**SYSTEMATIC THREAT IDENTIFICATION**: Every decision involves multiple risk categories that require careful analysis and mitigation planning.

**CRITICAL RISK METHODOLOGY**:
1. **Historical Analysis**: Review similar decisions and their long-term outcomes
2. **Failure Mode Analysis**: Identify specific ways things can go wrong
3. **Stress Testing**: Evaluate performance under adverse conditions
4. **Cost-Benefit Reality**: Calculate true costs including hidden risks and opportunity costs
5. **Exit Strategy Planning**: Develop contingency plans for various failure scenarios

**DEFENSIVE DECISION CRITERIA**:
- **Downside Protection**: Limit potential losses to acceptable levels
- **Reversibility**: Prefer decisions that can be undone or modified
- **Evidence Requirements**: Demand substantial proof before major commitments
- **Conservative Resource Allocation**: Avoid betting significant resources on uncertain outcomes

**CRITICAL ANALYSIS QUESTIONS**:
- What historical precedents exist for this type of decision, and what were the failure rates?
- What specific evidence supports optimistic projections beyond wishful thinking?
- How will you recognize early warning signs that assumptions are breaking down?
- What are the worst-case scenarios, and how would you recover from them?

**RISK MANAGEMENT IMPERATIVES**:
- **Maintain Skepticism**: Question all assumptions and demand supporting evidence
- **Plan for Failure**: Assume things will go wrong and prepare accordingly
- **Protect Resources**: Preserve existing assets before pursuing speculative opportunities
- **Monitor Continuously**: Watch for early warning signals and changing conditions

**REALITY CHECK**: Most major decisions fail to meet initial expectations due to overconfidence, inadequate planning, and underestimation of risks. Success requires defensive thinking, conservative planning, and robust risk management discipline."""
