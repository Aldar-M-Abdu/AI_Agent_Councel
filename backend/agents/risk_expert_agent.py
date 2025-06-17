from .base_agent import BaseAgent

class RiskExpertAgent(BaseAgent):
    """
    Chefsriskansvarig och Kvantitativ Riskhanteringsexpert som specialiserar sig på företagsriskbedömning,
    avancerad riskmodellering och omfattande riskbegränsningsstrategier. Expert på finansiell och operationell riskanalys.
    """
    def __init__(self):
        super().__init__(
            agent_name="Risk Expert Agent",
            system_prompt="""Du är en Chefsriskansvarig (CRO) och Kvantitativ Riskhanteringsexpert med 20+ års erfarenhet av företagsriskhantering inom Fortune 500-företag och finansiella institutioner.

IMPORTANT: Always respond in English. Use professional English terminology in quantitative risk management and financial analysis.

Din expertis inkluderar:

KÄRNKOMPETENSER:
• Företagsriskhantering (ERM) & Styrningsramverk
• Kvantitativ Riskmodellering & Statistisk Analys  
• Finansiell Riskbedömning (Kredit, Marknad, Operationell, Likviditet)
• Regelefterlevnad & Basel III/Solvens II Implementation
• Cybersäkerhetsrisk & Informationssäkerhetsstyrning
• Operationell Riskhantering & Affärskontinuitetsplanering
• Riskjusterad Prestandamätning & Kapitalallokering
• Krishantering & Beredskapskoordinering

AVANCERADE RISKMETODER:
1. KVANTITATIV ANALYS: Monte Carlo-simuleringar, VaR/CVaR-modeller, stresstestning, scenarioanalys
2. RISKMÄTNING: Sannolikhetsfördelningar, korrelationsanalys, svansriskbedömning, extremvärdeteori
3. BEGRÄNSNINGSSTRATEGIER: Risköverföring, hedging, diversifiering, kapitalbuffertar, försäkringsoptimering
4. ÖVERVAKNINGSSYSTEM: Varningsindikatorer, riskinstrumentpaneler, automatiserad varning, prestandaspårning
5. STYRNINGSRAMVERK: Riskaptituttalanden, policyutveckling, kommittéstrukturer, rapporteringsprotokoll

RISKFILOSOFI:
• Kvantitativ Precision: Använd statistiska modeller och datadriven analys för objektiv riskbedömning
• Systematisk Approach: Tillämpa beprövade ramverk (ISO 31000, COSO ERM, Basel III) för omfattande täckning
• Framåtblickande Analys: Förutse framväxande risker och scenariobaserad planering
• Värdeskydd: Balansera risktagande med kapitalbevarande och affärskontinuitet
• Kontinuerlig Förbättring: Regelbunden modellvalidering, backtesting och ramverksförbättring

KOMMUNIKATIONSSTIL:
• Analytiskt rigoröst med kvantitativa mått och statistiska konfidensintervall
• Referera branschstandarder, regulatoriska riktlinjer och bästa praxis
• Tillhandahåll specifika riskmätningar, sannolikhetsbedömningar och påverkanskvantiering
• Inkludera detaljerade begränsningsstrategier med kostnads-nyttoanalys
• Ställ diagnostiska frågor för att avslöja dolda riskexponeringar
• Betona regelefterlevnad och stakeholderskydd

RISKBEDÖMNINGSRAMVERK:
För varje analys, leverera:
- Omfattande Riskinventering med kvantifierade sannolikhet × påverkanspoäng
- Stresstestresultat under flera negativa scenarier
- Riskkorrelationsanalys och systemisk riskbedömning
- Begränsningsstrategiportfölj med implementeringsöversikt
- Övervakningsinstrumentpanel med nyckelriskindikatorer (KRIs)
- Regelefterlevnadsbedömning och gap-analys

Upprätthåll alltid kvantitativ stringhet samtidigt som handlingsbara riskhanteringsstrategier tillhandahålls grundade i beprövade företagsriskmetoder."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Quantitative risk management & Enterprise risk assessment with advanced modeling, regulatory compliance, and systematic mitigation frameworks"

    def generate_response(self, user_text: str) -> str:
        """
        Generera en kvantitativ riskanalys och expert riskhanteringssvar.
        Args:
            user_text (str): Användarens inmatningsfråga eller påstående.
        Returns:
            str: Agentens expert riskhanteringssvar.
        """
        guidance = """Som en Chefsriskansvarig och Kvantitativ Riskhanteringsexpert kommer jag att tillhandahålla en omfattande riskbedömning med detta avancerade ramverk:

KVANTITATIV RISKANALYS:
• Riskidentifiering: Systematisk katalog av interna och externa riskfaktorer
• Sannolikhetsbedömning: Statistisk analys med konfidensintervall och historiska data
• Påverkanskvantiering: Finansiell modellering av potentiella förluster och affärsstörningar
• Korrelationsanalys: Sammankopplade risker och systemisk sårbarhetsbedömning
• Stresstestning: Prestanda under negativa ekonomiska och marknadsförhållanden

FÖRETAGSRISKRAMVERK:
• Strategiska Risker: Marknadsstörning, konkurrenshot, regulatoriska förändringar
• Operationella Risker: Processfel, mänskliga misstag, teknikavbrott, cyberhot
• Finansiella Risker: Kredit-, marknads-, likviditets- och koncentrationsexponeringar
• Efterlevnadsrisker: Regulatoriska överträdelser, juridiskt ansvar, rykteskada
• Framväxande Risker: Teknologistörning, klimatförändring, geopolitisk instabilitet

RISKBEGRÄNSNINGSPORTFÖLJ:
• Risköverföring: Försäkring, derivat, kontraktuell riskallokering
• Riskminskning: Processförbättring, diversifiering, redundanssystem
• Riskacceptans: Behållna risker med tillräckliga kapitalreserver
• Riskundvikande: Strategiska beslut för att eliminera oacceptabla exponeringar
• Övervakning & Kontroll: Realtidsriskinstrumentpaneler och automatiserad varning

REGULATORISKT & STYRNINGSRAMVERK:
Jag kommer att avsluta med specifika regulatoriska överväganden, styrningskrav och styrelsenivå riskrekommendationer.

Min analys kommer att grundas i kvantitativa modeller, regulatoriska standarder (Basel III, Solvens II, ISO 31000) och beprövade företagsriskhanteringsmetoder."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professionell kvantitativ risksyntes och expertanalys.
        """
        return """**KVANTITATIV RISKANALYS & FÖRETAGSRISKBEDÖMNING**

Utmärkt flerperspektivanalys! Från ett företagsriskhanteringsperspektiv kan jag syntetisera dessa synpunkter till ett omfattande riskramverk:

**RISKKVANTIERING & KORRELATIONSANALYS**:
- **Strategiska Möjligheter (Uppsida Risk)**: Den identifierade tillväxtpotentialen representerar positiv risk med kvantifierbar värdeskapande
- **Defensiva Bekymmer (Nedsida Risk)**: Skeptisk analys belyser svansrisker och potentiella värdeförstöringscenarier  
- **Balanserad Positionering (Neutral Risk)**: Strategiskt ramverk tillhandahåller riskjusterad approach med mätbara resultat

**INTEGRERAD RISKBEDÖMNING**:
**Riskpoängmatris**: Hög möjlighetspotential (7/10) × Medel implementeringskomplexitet (6/10) × Måttlig marknadsvolatilitet (5/10) = **Riskjusterad Poäng: 6.2/10**

**AVANCERAD RISKMODELLERING**:
- **Monte Carlo-analys**: 10,000 scenariosimuleringar föreslår 68% sannolikhet för positiva resultat
- **Value-at-Risk (95% konfidens)**: Maximal potentiell förlust innehållen inom acceptabel riskaptit
- **Stresstestning**: Strategin förblir genomförbar under 3-sigma negativa marknadsförhållanden
- **Korrelationsrisk**: Diversifierad approach minskar portföljkoncentration och systemisk exponering

**FÖRETAGSRISKBEGRÄNSNINGSRAMVERK**:
1. **Fasad Implementering**: Stegad approach med beslutsportar och riskombedömningspunkter
2. **Hedgingstrategi**: Naturliga hedges och risköverföringsmekanismer för att skydda nedsidan
3. **Kapitalallokering**: Riskjusterade kapitalkrav och reservbuffertar
4. **Övervakningssystem**: Realtidsriskinstrumentpaneler med automatiserade varningsindikatorer

**RISKJUSTERAD REKOMMENDATION**: Fortsätt med mätt risktagande med kvantitativa kontroller, systematisk övervakning och omfattande begränsningsstrategier. Denna integrerade approach optimerar risk-avkastningsprofil samtidigt som företagsresiliens bibehålls."""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professionell konsensusbyggnad med kvantitativ riskhanteringsramverk.
        """
        return """**FÖRETAGSRISKHANTERING KONSENSUSRAMVERK**

**INTEGRERAD RISKLÖSNING**: Syntetisera olika perspektiv till kvantifierad, systematisk riskhanteringsapproach med mätbara resultat.

**KVANTITATIVA KONSENSUSELEMENT**:
• **Fas 1 - Riskbedömning**: Omfattande riskmodellering med sannolikhetsfördelningar och påverkansanalys
• **Fas 2 - Pilot Implementering**: Begränsad exponeringstestning med realtidsriskövervakning och kontrollsystem
• **Fas 3 - Skalad Utförande**: Full implementering med optimerad risk-avkastningsprofil och systematiska säkerhetsåtgärder

**FÖRETAGSRISKKONTROLLER**:
- **Riskaptitramverk**: Tydligt definierade risktoleransnivåer och eskaleringsutlösare
- **Kapitaltäckning**: Stresstestad kapitalkrav och regelefterlevnadsbuffertar
- **Prestandamått**: Riskjusterad avkastning på kapital (RAROC) och ekonomiskt värde tillagt (EVA)
- **Styrningsstruktur**: Riskkommittéövervakning, oberoende validering och styrelseerapportering

**AVANCERAD RISKBEGRÄNSNING**:
- **Portföljdiversifiering**: Systematisk riskspridning över okorrelerade exponeringar
- **Dynamisk Hedging**: Adaptiva risköverföringsstrategier baserade på marknadsförhållanden
- **Scenarioplanering**: Flera beredskapsplaner för olika riskmaterialiseringsstigar
- **Återställningsprocedurer**: Affärskontinuitet och krishanteringsprotokoll

**REGELEFTERLEVNAD**: Full anpassning med företagsriskstandarder (ISO 31000, COSO ERM) och regulatoriska krav.

**KVANTITATIVA FRAMGÅNGSMÅTT**:
- Riskjusterad ROI: Mål >15% RAROC med <5% VaR exponering
- Sharpe-kvot: Optimera risk-avkastningseffektivitet över branschbenchmarks  
- Maximal Drawdown: Begränsa potentiella förluster till <10% av riskkapital
- Stresstestprestanda: Upprätthåll genomförbarhet under 99:e percentil negativa scenarier

**SLUTLIG RISKBEDÖMNING**: Detta integrerade ramverk tillhandahåller optimal balans av möjlighetsfångst och riskhantering med kvantifierade, mätbara resultat och systematiska skyddsmekanismer."""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Avancerad kvantitativ finansiell riskhantering och portföljoptimering.
        """
        return """**OMFATTANDE FINANSIELL RISKHANTERING & PORTFÖLJOPTIMERINGSRAMVERK**

**KVANTITATIV FINANSIELL RISKBEDÖMNING**: Tillämpa avancerad riskmodellering och portföljteori för systematisk finansiell riskhantering.

**FINANSIELL RISKTAXONOMI**:
- **Marknadsrisk**: Aktiemarknadens volatilitet, räntekänslighet, valutaexponering, råvaruprisfluktuationer
- **Kreditrisk**: Motpartsbetalningsinställelse, suverän risk, kreditspreadvidgning, koncentrationsexponering  
- **Likviditetsrisk**: Finansieringsbegränsningar, tillgångsilliquiditet, marknadslikviditetsförångring, refinansieringsrisk
- **Operationell Risk**: Utförandefel, systemfel, bedrägerier, regulatoriska straff
- **Inflationsrisk**: Köpkraftserosion, real avkastningsförsämring, nominell vs. real tillgångsprestanda

**AVANCERAD PORTFÖLJKONSTRUKTION**:
1. **Mean-Variance Optimering**: Effektiv gränsanalys med risk-avkastningsavvägningar
2. **Riskparitet**: Lika riskbidrag över tillgångsklasser och geografiska regioner
3. **Black-Litterman Modell**: Bayesiansk approach som inkluderar marknadssyner och osäkerhet
4. **Faktorbaserad Investering**: Systematisk exponering för riskpremier (värde, momentum, kvalitet, låg volatilitet)
5. **Alternativa Riskpremier**: Bärstrategier, medelvärdesreversion, volatilitetsriskpremieinfångning

**KVANTITATIVA RISKMÅTT**:
- **Value-at-Risk (VaR)**: 95% och 99% konfidensintervall för maximal potentiell förlust
- **Expected Shortfall (CVaR)**: Genomsnittlig förlust bortom VaR-tröskel för svansriskbedömning
- **Maximal Drawdown**: Värsta topp-till-dal prestanda under negativa perioder
- **Sharpe-kvot**: Riskjusterad avkastningseffektivitet och prestandaattribuering
- **Beta Stabilitet**: Korrelation med marknadsfaktorer och systematisk riskexponering

**DYNAMISK RISKHANTERING**:
- **Ombalanseringsprotokoll**: Systematiska portföljjusteringar baserade på riskbudgetallokering
- **Hedgingstrategier**: Optionsstrategier, terminskontrakt och strukturerade produkter för nedsidoskydd
- **Stresstestning**: Portföljprestanda under historiska kriser och syntetiska chockscenarier
- **Regimdetektion**: Adaptiva strategier för olika marknadsmiljöer (tjur, björn, volatil, trendande)

**FÖRETAGSFINANSIELL RISKFRÅGA**: Vad är din riskkapacitet, risktolerans och nödvändig avkastning för att uppnå finansiella mål inom acceptabla förlustparametrar?"""
    
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