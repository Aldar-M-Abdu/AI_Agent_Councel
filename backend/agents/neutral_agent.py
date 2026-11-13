from .base_agent import BaseAgent

class NeutralAgent(BaseAgent):
    """
    Professional Strategic Analyst providing objective, evidence-based recommendations with comprehensive business analysis.
    Specializes in balanced decision frameworks, risk-benefit analysis, and multi-stakeholder perspectives.
    """
    def __init__(self):
        super().__init__(
            agent_name="Neutral Agent", 
            system_prompt="""You are a Senior Strategic Business Analyst with 15+ years of consulting experience from Fortune 500 companies.

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
        """Kontrollera om text innehåller arabiska tecken"""
        arabic_chars = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويىء')
        return any(char in arabic_chars for char in text)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professionell strategisk syntes av flera perspektiv.
        """
        return """**STRATEGISK SYNTES & BALANSERAD BEDÖMNING**

Efter att ha analyserat de olika perspektiven som presenterats, har jag identifierat flera viktiga strategiska teman:

**MÖJLIGHETSKONVERGENS**: Det optimistiska synsättet belyser marknadspotential och tillväxtmöjligheter som stämmer överens med nuvarande branschtrender. Dessa positiva scenarier förtjänar seriös uppmärksamhet givet deras potentiella ROI.

**RISKBEGRÄNSNINGSIMPERATIV**: Den skeptiska analysen väcker kritiska bekymmer om implementeringsutmaningar, marknadsvolatilitet och resursbegränsningar. Dessa riskfaktorer kräver strukturerade begränsningsstrategier.

**EVIDENSBASERAD INTEGRATION**: Att kombinera dessa perspektiv föreslår en balanserad approach som maximerar möjligheter samtidigt som legitima bekymmer hanteras genom:
- Fasad implementering med stage-gates
- Robust riskövervaknings- och varningssystem
- Stakeholderanpassnings- och kommunikationsprotokoll
- Resursoptimering och beredskapsplanering

**STRATEGISK REKOMMENDATION**: En riskjusterad approach som eftersträvar högt värde möjligheter samtidigt som defensiv positionering upprätthålls. Denna balanserade strategi möjliggör opportunistisk tillväxt samtidigt som strategisk flexibilitet bevaras.

**VIKTIGA STRATEGISKA FRÅGOR**:
1. Vilka är de mest kritiska framgångsfaktorerna som kan göra eller förstöra detta initiativ?
2. Hur kan vi strukturera detta för att maximera lärande samtidigt som nedsidans exponering minimeras?
3. Vilken stakeholderanpassning krävs för framgångsrik genomförande?"""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professionell konsensusbyggnad med strategiskt ramverk.
        """
        return """**STRATEGISKT KONSENSUSRAMVERK**

**INTEGRERAD APPROACH**: Balansera möjlighetssträvan med riskhantering genom en strukturerad, fasad implementeringsstrategi.

**KONSENSUSELEMENT**:
• **Fas 1 - Validering**: Pilottestning med begränsat resursåtagande
• **Fas 2 - Optimering**: Skala baserat på validerade lärdomar och marknadsfeedback  
• **Fas 3 - Expansion**: Full implementering med etablerade framgångsmått

**STYRNINGSSTRUKTUR**:
- Tydlig beslutsmyndighet och eskaleringsstigar
- Regelbundna granskningscykler med go/no-go beslutspunkter
- Stakeholderkommunikations- och anpassningsprotokoll
- Framgångsmått och prestandainstrumentpaneler

**RISKBEGRÄNSNING**: Implementera robusta övervakningssystem, beredskapsplaner och exitstrategier samtidigt som strategisk flexibilitet upprätthålls.

**FRAMGÅNGSFAKTORER**: Stakeholderanpassning, resurstillräcklighet, marknadstiming, genomförandeexcellens och adaptiva hanteringsförmågor.

Denna balanserade approach hanterar varje perspektiv samtidigt som den tillhandahåller en praktisk väg framåt som maximerar värdeskapandepotential."""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professionell finansiell strategi med affärsramverk.
        """
        return """**STRATEGISK FINANSIELL ANALYS**

**INVESTERINGS​RAMVERK**: Tillämpa Modern Portföljteori med strategisk tillgångsallokering över riskkategorier. Implementera systematisk approach med:
- **Due Diligence**: Omfattande finansiell rapportanalys, marknadsundersökning och konkurrenspositionering
- **Riskbedömning**: Value-at-Risk (VaR) modellering, stresstestning och scenarioanalys
- **Portföljkonstruktion**: Diversifiering över tillgångsklasser, sektorer och geografiska regioner

**STRATEGISK METODIK**:
1. **Finansiella Mål**: Definiera tydliga ROI-mål, risktolerans och investeringstidslag
2. **Marknadsanalys**: Genomför grundlig marknadsundersökning med branschrapporter och konkurrensintelligens
3. **Implementeringsstrategi**: Fasad approach med regelbunden portföljbalansering och prestandaövervakning

**PROFESSIONELLA RESURSER**: Referera CFA Institute riktlinjer, institutionell forskning och peer-reviewed finansiell litteratur för evidensbaserat beslutsfattande.

**FRAMGÅNGSMÅTT**: Spåra prestanda mot benchmarks, övervaka riskjusterad avkastning och upprätthåll detaljerad dokumentation för kontinuerlig förbättring.

**STRATEGISK FRÅGA**: Hur stämmer denna investering överens med din övergripande finansiella strategi och riskhanteringsramverk?"""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professionell karriärstrategi med utvecklingsramverk.
        """
        return """**STRATEGISKT KARRIÄRUTVECKLINGSRAMVERK**

**KARRIÄRSTRATEGI​ANALYS**: Tillämpa beprövade metoder för karriärframsteg och professionell utveckling:

**STRATEGISK BEDÖMNING**:
- **Kompetensgrapsanalys**: Kartlägg nuvarande förmågor mot målrollskrav
- **Marknadsintelligens**: Analysera branschtrender, lönebenchmarks och tillväxtprognoser med LinkedIn Insights, Bureau of Labor Statistics och branschrapporter
- **Konkurrenspositionering**: Bedöm unikt värdeförslag och differentieringsstrategier

**UTVECKLINGSÖVERSIKT**:
1. **Kompetensutveckling**: Riktad lärplan med mätbara milstolpar
2. **Nätverksbyggnad**: Strategisk relationsuppbyggnad med branschledare
3. **Varumärkesbyggnad**: Professionell reputationshantering och tankeledarskap
4. **Erfarenhetsförvärv**: Strukturerad approach för att få relevant erfarenhet

**FRAMGÅNGSRAMVERK**: Använd SMART-mål med regelbundna framstegsöversyner och adaptiv planering baserat på marknadsfeedback och möjligheter.

**STRATEGISKA FRÅGOR**:
- Vilka specifika färdigheter eller erfarenheter skulle göra dig oumbärlig i din målroll?
- Hur kan du bygga strategiska relationer som accelererar din karriärprogression?
- Vilka marknadstrender bör påverka din karriärutvecklingsstrategi?"""
    
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Professionell relationshantering med evidensbaserade ramverk.
        """
        return """**STRATEGISKT RELATIONSRAMVERK**

**EVIDENSBASERAD APPROACH**: Tillämpa forskningsbaserade metoder från relationspsykologi och organisatoriskt beteende:

**RELATIONSBEDÖMNING**:
- **Kompatibilitetsanalys**: Värdeanpassning, kommunikationsstilar och livskompatibilitet
- **Relationsdynamik**: Tillämpa Gottman Institutes forskning om relationsprediktorer
- **Stakeholderpåverkan**: Överväg effekter på familj, karriär och sociala nätverk

**STRATEGISK UTVECKLING**:
1. **Kommunikationsprotokoll**: Upprätta tydliga förväntningar och feedbackmekanismer
2. **Konflikthantering**: Tillämpa strukturerade metoder för att hantera konflikter
3. **Delade mål**: Alignera på gemensamma objektiv och framgångsmått
4. **Kontinuerlig förbättring**: Regelbunden relationsöversyn och justeringsstrategier

**FRAMGÅNGSMÅTT**: Spåra relationstillfredsställelse, kommunikationseffektivitet och framgångsprocent progress.

**PROFESSIONELLA RESURSER**: Referera peer-reviewed forskning i relationspsykologi och evidensbaserad praxis för relationell utveckling.

**STRATEGISK FRÅGA**: Hur kan du strukturera denna relation för att maximera gemensamt värde samtidigt som individutveckling och -utveckling bevaras?"""
    
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