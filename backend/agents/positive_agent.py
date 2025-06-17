from .base_agent import BaseAgent

class PositiveAgent(BaseAgent):
    """
    Chefsinnovationsdirektör och Tillväxtstrategi-expert som specialiserar sig på möjlighetsidentifiering, 
    marknadsexpansion och transformationsledarskap. Fokuserar på värdeskapande och konkurrensfördelar.
    """
    def __init__(self):
        super().__init__(
            agent_name="Positive Agent", 
            system_prompt="""Du är en Chefsinnovationsdirektör (CIO) och Tillväxtstrategi-expert med 20+ års erfarenhet av att skala startups till Fortune 500-företag. 

IMPORTANT: Always respond in English. Use professional English terminology in business and strategy areas.

Din expertis inkluderar:

KÄRNKOMPETENSER:
• Innovationsstrategi & Digital Transformation
• Marknadsmöjlighetsbedömning & Expansion
• Growth Hacking & Intäktsoptimering  
• Förändringsledarskap & Organisationsutveckling
• Strategiska Partnerskap & Affärsutveckling
• Riskkapital & Investeringsstrategi
• Teknikadoption & Konkurrensfördelar
• Prestandaoptimering & Operationell Excellens

INNOVATIONSMETODIK:
1. MÖJLIGHETSKARTLÄGGNING: Identifiera marknadsgap, framväxande trender och konkurrensfördelar
2. VÄRDEPROPOSITIONSDESIGN: Skapa övertygande kundvärdepropositioner med Jobs-to-be-Done ramverk
3. TILLVÄXTSTRATEGI: Utveckla skalbara affärsmodeller med nätverkseffekter och virala koefficienter
4. GENOMFÖRANDEEXCELLENS: Implementera agila metoder med snabb iteration och kontinuerlig förbättring
5. PRESTANDAMÅTT: Etablera KPI:er för tillväxtspårning och optimering

LEDARSKAPSFILOSOFI:
• Tillväxttänk: Varje utmaning är en lärandemöjlighet
• Datadriven Optimism: Basera entusiasm på marknadsbevis och kundvalidering
• Hållbar Innovation: Fokusera på långsiktig värdeskapande över kortsiktiga vinster
• Teamstärkande: Möjliggör för andra att uppnå genombryttsprestanda
• Strategisk Vision: Koppla nuvarande handlingar till framtida marknadsmöjligheter

KOMMUNIKATIONSSTIL:
• Inspirerande och handlingsorienterad med konkreta nästa steg
• Referera framgångsrika fallstudier och beprövade tillväxtstrategier
• Tillhandahåll specifika ramverk och metoder
• Inkludera kvantitativa mål och framgångsmått
• Ställ visionexpanderande frågor om potential och möjligheter
• Betona konkurrensfördelar och marknadsdifferentiering

TILLVÄXTRAMVERK:
För varje möjlighet, leverera:
- Marknadsmöjlighetsanalys (TAM, SAM, SOM)
- Konkurrensfördelbedömning  
- Intäktstillväxtprognoser
- Implementeringsöversikt med Snabba Vinster
- Framgångsmått & Tillväxt KPI:er
- Skalningsstrategi & Resurskrav

Upprätthåll alltid strategisk optimism samtidigt som rekommendationer grundas i marknadsrealiteter och beprövade tillväxtmetoder."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Growth strategy & Innovation leadership with opportunity-focused analysis, market expansion frameworks, and performance optimization methods"

    def generate_response(self, user_text: str) -> str:
        """
        Generera ett innovations- och tillväxtfokuserat strategiskt svar.
        Args:
            user_text (str): Användarens inmatningsfråga eller påstående.
        Returns:
            str: Agentens tillväxtstrategisvar.
        """
        guidance = """Som en Chefsinnovationsdirektör och Tillväxtstrategi-expert kommer jag att tillhandahålla en möjlighetsfokuserad analys med detta ramverk:

MARKNADSMÖJLIGHETSBEDÖMNING:
• Tillväxtpotential & Marknadsstorleksanalys
• Konkurrenslandskap & Differentieringsmöjligheter  
• Kundvärdeproposition & Marknadspassform
• Intäktsmodeller & Monetiseringsstrategier
• Teknikaktivering & Innovationsmöjligheter

STRATEGISKT TILLVÄXTRAMVERK:
• Snabba Vinster: Omedelbara värdeskapande handlingar (0-3 månader)
• Tillväxtdrivare: Skalbara initiativ för expansion (3-12 månader)  
• Transformation: Långsiktig konkurrensfördel (1-3 år)
• Framgångsmått: KPI:er för att spåra framsteg och optimering
• Resursstrategi: Investeringskrav och ROI-prognoser

INNOVATIONSKATALYSATORFRÅGOR:
Jag kommer att avsluta med strategiska frågor designade för att låsa upp ytterligare tillväxtmöjligheter och expandera tänkandet om marknadspotential.

Mina rekommendationer kommer att grundas i beprövade tillväxtmetoder, framgångsrika fallstudier och kvantitativ marknadsanalys samtidigt som strategisk optimism om uppnåeliga resultat bibehålls."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professionell tillväxtstrategisyntes och möjlighetsförstärkning.
        """
        return """**STRATEGISK TILLVÄXTMÖJLIGHETSSYNTES**

Jag är energieffektiv av de olika perspektiven som delats! Denna flerdimensionella analys avslöjar betydande tillväxtpotential när vi kombinerar strategiskt tänkande:

**INNOVATIONSKONVERGENS**: Den balanserade bedömningen tillhandahåller utmärkt riskmedvetenhet som kommer att stärka vårt genomförande, medan den skeptiska analysen hjälper oss att bygga anti-fragila strategier. Dessa input är ovärderliga för att skapa robusta tillväxtsystem.

**MARKNADSMÖJLIGHETSFÖRSTÄRKNING**: Istället för att se bekymmer som begränsningar, låt oss omrankka dem som konkurrensintelligens. Varje identifierad utmaning representerar ett marknadsbehov som väntar på en innovativ lösning. Detta skapar blå ocean-möjligheter för första-mover-fördel.

**STRATEGISK FÖRDELSSKAPANDE**:
- **Riskbegränsning som Konkurrensvallar**: Hantera bekymmer proaktivt för att bygga hållbara konkurrensfördelar
- **Stakeholdervärdesskapande**: Förvandla skeptisk feedback till kundinsikter och produktförbättringar  
- **Innovationsacceleration**: Använd olika perspektiv för att identifiera genombrytsmöjligheter andra missar

**TILLVÄXTKATALYSATORRAMVERK**: Kombinera den strategiska stringheten av balanserad analys med den skyddande planeringen av riskhantering för att skapa en ostoppbar tillväxtmotor.

**EXPONENTIELLA MÖJLIGHETSFRÅGOR**:
1. Hur kan vi förvandla de identifierade utmaningarna till våra största konkurrensfördelar?
2. Vad händer om riskerna blir grunden för innovativa lösningar som fångar marknadsandelar?
3. Hur kan vi utnyttja denna olika intelligens för att skapa genombrytande värdepropositioner?

Detta är den perfekta grunden för genombrytsinnovation och marknadsledarskap! 🚀"""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professionell konsensusbyggnad med tillväxtaccelerationsramverk.
        """
        return """**STRATEGISKT TILLVÄXTKONSENSUSRAMVERK** 

**INNOVATIONSINTEGRATIONSSTRATEGI**: Förvandla olika perspektiv till konkurrensfördelar genom systematisk innovation.

**TILLVÄXTACCELERATIONSELEMENT**:
• **Fas 1 - Marknadsvalidering**: Snabb prototyping med kundfeedbackloopar
• **Fas 2 - Tillväxtoptimering**: Skala validerade lösningar med prestandamått
• **Fas 3 - Marknadsledarskap**: Expandera till angränsande marknader med beprövade metoder

**KONKURRENSFÖRDELSKAPANDE**:
- **Intelligensintegration**: Använd skeptiska insikter som produktutvecklingsintelligens
- **Riskjusterad Innovation**: Bygg robusta lösningar som konkurrenter inte enkelt kan replikera
- **Stakeholdervärdoptimering**: Skapa win-win scenarier som accelererar adoption
- **Prestandaexcellens**: Etablera branschledande standarder och benchmarks

**EXPONENTIELLA TILLVÄXTAKTIVERING**: Utnyttja beprövade metoder (Lean Startup, Design Thinking, OKRs) för att skapa hållbara konkurrensfördelar samtidigt som smidighet och innovationshastighet bibehålls.

**FRAMGÅNGSFÖRSTÄRKNING**: Denna integrerade approach positionerar oss för marknadsledarskap genom att kombinera strategisk stringhet med innovationexcellens och genomförandedisciplin.

**GENOMBRYTPOTENTIAL**: Vi löser inte bara ett problem - vi skapar en ny marknadskategori med hållbara konkurrensvallar! 

Syntesen av dessa perspektiv skapar exponentiell möjlighet för värdeskapande och marknadspåverkan! 💡"""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Tillväxtorienterad finansiell strategi med innovationsramverk.
        """
        return """**STRATEGISK VÄLSTÅNDSSKAPANDE & INVESTERINGSEXCELLENS**

**EXPONENTIELLT TILLVÄXTRAMVERK**: Förvandla finansiella beslut till välståndsbyggande motorer med beprövade metoder:

**INVESTERINGSINNOVATIONSSTRATEGI**:
- **Marknadsledapositionering**: Fokusera på tillväxtsektorer med stark grund (teknologi, hälsovård, hållbarhet)
- **Diversifierad Tillväxtportfölj**: Balansera högtillväxtmöjligheter med stabila inkomstgeneratorer
- **Sammansatt Tillväxtoptimering**: Utnyttja tid och återinvestering för exponentiell välståndsskapande
- **Innovationsinvestering**: Allokera del till framväxande teknologier och disruptiva affärsmodeller

**VÄLSTÅNDSBYGGANDEEXCELLENS**:
1. **Strategisk Tillgångsallokering**: Modern Portföljteori med tillväxtorienterad viktning
2. **Prestandaoptimering**: Regelbunden ombalansering och skatteeffektiva strategier
3. **Riskjusterad Avkastning**: Maximera avkastning samtidigt som lämplig riskhantering bibehålls
4. **Marknadsintelligens**: Utnyttja forskning, trendanalys och professionella nätverk

**FINANSIELLA FRAMGÅNGSACCELERATORER**:
- **Automatiserat Välståndsbyggande**: Systematisk investering och sammansatt tillväxtstrategier
- **Skatteoptimering**: Maximera efterskatteavkastning genom strategisk planering
- **Professionell Utveckling ROI**: Investera i färdigheter som ökar intjäningspotential

**GENOMBRYTSMÖJLIGHET**: Din finansiella framtid har obegränsad potential när du kombinerar strategiskt tänkande med disciplinerat genomförande och långsiktig vision!

**TILLVÄXTKATALYSATORFRÅGA**: Vad händer om din investeringsstrategi inte bara kunde bygga välstånd utan också positionera dig som en tankeleadare inom framväxande marknadsmöjligheter?"""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Karriäracceleration och professionell utvecklingsexcellens.
        """
        return """**STRATEGISK KARRIÄRACCELERATION & LEDARSKAPSUTVEKLING**

**EXPONENTIELLT KARRIÄRTILLVÄXTRAMVERK**: Förvandla karriärbeslut till ledarskpsmöjligheter och marknadsinflytande:

**KARRIÄRINNOVATIONSSTRATEGI**:
- **Marknadspositioneringsexcellens**: Bygg unik värdeproposition som gör dig oumbärlig
- **Färdighetsframtidssäkring**: Bemästra framväxande teknologier och tvärfunktionella förmågor
- **Nätverk Strategisk Utveckling**: Odla relationer med branschledare och beslutsfattare
- **Tankeledarskapskapande**: Etablera expertis och inflytande inom ditt område

**PROFESSIONELL EXCELLENSÖVERSIKT**:
1. **Förmågebedömning**: Kartlägg nuvarande färdigheter till marknadsmöjligheter och framtida trender
2. **Strategisk Lärande**: Rikta in dig på högpåverkansfärdigheter med omedelbara tillämpningsmöjligheter  
3. **Erfarenhetsacceleration**: Sök sträckuppdrag och ledarskapsansvar
4. **Varumärkesbyggnad**: Utveckla professionell rykte och branscherkännande
5. **Värdeskapande**: Fokusera på att leverera mätbar affärspåverkan och innovation

**KARRIÄRFRAMGÅNGSMULTIPLIKATORER**:
- **Tvärbranchintelligens**: Tillämpa bästa praxis från flera sektorer
- **Innovationsledarskap**: Driva förändring och transformationsinitiativ
- **Mentorskapsexcellens**: Både lära av ledare och utveckla andra

**GENOMBRYTPOTENTIAL**: Din karriärbana kan bli en modell för andra samtidigt som den skapar extraordinärt värde för organisationer och stakeholders.

**EXPONENTIELLA OPPORTUNITSFRÅGOR**:
- Hur kan du bli den ledande experten inom ett framväxande område som är kritiskt för företagsframgång?
- Vad händer om din karriärspåg kan influera branschstandarder och bästa praxis?"""
    
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Relationship optimization and connection excellence.
        """
        return """**STRATEGIC RELATIONSHIP EXCELLENCE & CONNECTION OPTIMIZATION**

**RELATIONSHIP INNOVATION FRAMEWORK**: Transform connections into mutual growth engines and value creation partnerships:

**CONNECTION EXCELLENCE STRATEGY**:
- **Mutual Value Creation**: Focus on win-win outcomes that accelerate both parties' success
- **Communication Mastery**: Develop exceptional listening, empathy, and influence skills
- **Growth Partnership**: Support each other's aspirations and breakthrough achievements
- **Emotional Intelligence**: Master relationship dynamics and conflict transformation

**RELATIONSHIP SUCCESS ACCELERATORS**:
1. **Shared Vision Creation**: Align on compelling mutual goals and success metrics
2. **Performance Partnership**: Establish systems for continuous improvement and celebration
3. **Innovation Together**: Create new experiences and breakthrough moments
4. **Network Integration**: Expand relationships through strategic introductions and collaboration
5. **Legacy Building**: Focus on creating lasting positive impact together

**CONNECTION OPTIMIZATION TOOLS**:
- **Active Appreciation**: Regular recognition and celebration of achievements
- **Growth Mindset**: Embrace challenges as opportunities to strengthen bonds
- **Adventure Partnership**: Create memorable experiences and shared adventures

**EXPONENTIAL RELATIONSHIP POTENTIAL**: Great relationships compound over time, creating exponential value for both parties through mutual support, shared opportunities, and collective growth.

**BREAKTHROUGH CONNECTION QUESTIONS**:
- How can this relationship become a catalyst for both parties achieving their biggest dreams?
- What if together you could create value that neither could achieve alone?"""
    
    def _generate_health_fallback(self, user_text: str, guidance: str) -> str:
        """
        Health optimization and peak performance excellence.
        """
        return """**STRATEGIC HEALTH OPTIMIZATION & PEAK PERFORMANCE EXCELLENCE**

**EXPONENTIAL WELLNESS FRAMEWORK**: Transform health decisions into performance advantages and life optimization:

**HEALTH INNOVATION STRATEGY**:
- **Biohacking Excellence**: Leverage data and technology for optimal health outcomes
- **Performance Nutrition**: Fuel your body for peak mental and physical performance
- **Recovery Optimization**: Master sleep, stress management, and restoration practices
- **Longevity Investment**: Focus on sustainable practices that compound over decades

**WELLNESS SUCCESS ACCELERATORS**:
1. **Baseline Optimization**: Comprehensive health assessment and personalized protocols
2. **Habit Stacking**: Build sustainable systems that integrate seamlessly into lifestyle
3. **Performance Tracking**: Monitor key biomarkers and adjust strategies for continuous improvement
4. **Social Support**: Engage health-conscious communities and accountability partners
5. **Innovation Adoption**: Integrate cutting-edge wellness technologies and methodologies

**HEALTH SUCCESS MULTIPLIERS**:
- **Energy Optimization**: Maximize sustained energy for peak productivity
- **Cognitive Enhancement**: Improve mental clarity, focus, and decision-making capability
- **Stress Resilience**: Develop anti-fragile systems that thrive under pressure

**EXPONENTIAL HEALTH POTENTIAL**: Optimal health creates a positive feedback loop affecting every aspect of life - career, relationships, creativity, and life satisfaction.

**PEAK PERFORMANCE QUESTIONS**:
- How can exceptional health become your competitive advantage in life and career?
- What if your wellness journey could inspire others to achieve breakthrough health outcomes?"""
    
    def _generate_education_fallback(self, user_text: str, guidance: str) -> str:
        """
        Learning acceleration and knowledge mastery excellence.
        """
        return """**STRATEGIC LEARNING ACCELERATION & KNOWLEDGE MASTERY FRAMEWORK**

**EXPONENTIAL LEARNING STRATEGY**: Transform education into competitive advantages and market leadership:

**LEARNING INNOVATION APPROACH**:
- **Future Skills Mastery**: Focus on emerging capabilities that create market differentiation
- **Cross-Disciplinary Excellence**: Combine knowledge from multiple fields for breakthrough insights
- **Applied Learning**: Immediate implementation for rapid skill development and validation
- **Teaching Integration**: Master concepts by teaching others and building thought leadership

**EDUCATION SUCCESS ACCELERATORS**:
1. **Learning ROI Optimization**: Select high-impact skills with immediate application opportunities
2. **Accelerated Mastery**: Use proven methodologies (Feynman Technique, Deliberate Practice, Spaced Repetition)
3. **Network Building**: Connect with leading experts and practitioners in your field
4. **Knowledge Application**: Create projects that demonstrate and reinforce learning
5. **Continuous Innovation**: Stay ahead of trends and emerging best practices

**LEARNING SUCCESS MULTIPLIERS**:
- **Knowledge Integration**: Synthesize learning across disciplines for unique insights
- **Teaching Excellence**: Build influence and expertise by helping others learn
- **Innovation Application**: Use new knowledge to create value and solve complex problems

**EXPONENTIAL LEARNING POTENTIAL**: Strategic learning compounds over time, creating exponential advantages in market value, problem-solving capability, and innovation potential.

**BREAKTHROUGH LEARNING QUESTIONS**:
- How can your learning journey position you as an industry thought leader?
- What if your educational investments could create new market opportunities and revenue streams?"""
    
    def _generate_travel_fallback(self, user_text: str, guidance: str) -> str:
        """
        Travel optimization and global opportunity creation.
        """
        return """**STRATEGIC TRAVEL EXCELLENCE & GLOBAL OPPORTUNITY CREATION**

**EXPONENTIAL TRAVEL FRAMEWORK**: Transform travel into competitive advantages, network expansion, and personal growth acceleration:

**TRAVEL INNOVATION STRATEGY**:
- **Global Market Intelligence**: Gain insights into emerging markets and business opportunities
- **Cultural Competency Development**: Build cross-cultural leadership and communication skills  
- **Network Expansion**: Connect with international leaders and potential collaborators
- **Innovation Inspiration**: Expose yourself to different approaches and breakthrough thinking

**TRAVEL SUCCESS ACCELERATORS**:
1. **Strategic Destination Selection**: Choose locations that align with professional and personal growth objectives
2. **Cultural Intelligence**: Prepare thoroughly to maximize cultural learning and relationship building
3. **Professional Networking**: Attend industry events and connect with local thought leaders
4. **Experience Documentation**: Capture insights and learning for future application and sharing
5. **Adventure Optimization**: Balance structured learning with spontaneous discovery and exploration

**GLOBAL SUCCESS MULTIPLIERS**:
- **Market Expansion Intelligence**: Understand global trends and business opportunities
- **Innovation Cross-Pollination**: Apply solutions from one culture to problems in another
- **Personal Growth Acceleration**: Challenge comfort zones and develop resilience and adaptability

**EXPONENTIAL TRAVEL POTENTIAL**: Strategic travel creates compound benefits - cultural intelligence, global networks, market insights, and personal development that accelerate success across all life domains.

**GLOBAL OPPORTUNITY QUESTIONS**:
- How can your travel experiences become a source of competitive intelligence and innovation?
- What if your global adventures could open doors to international business opportunities?"""
    
    def _generate_technology_fallback(self, user_text: str, guidance: str) -> str:
        """
        Technology innovation and digital transformation excellence.
        """
        return """**STRATEGIC TECHNOLOGY INNOVATION & DIGITAL TRANSFORMATION EXCELLENCE**

**EXPONENTIAL TECHNOLOGY FRAMEWORK**: Transform technology adoption into competitive advantages and market leadership:

**TECHNOLOGY INNOVATION STRATEGY**:
- **Early Adopter Advantage**: Leverage emerging technologies before mainstream adoption
- **Digital Transformation Leadership**: Use technology to create new business models and value propositions
- **Automation Excellence**: Optimize processes and create scalable systems for exponential growth
- **AI Integration**: Harness artificial intelligence for decision-making and performance optimization

**TECHNOLOGY SUCCESS ACCELERATORS**:
1. **Innovation Pipeline**: Continuously evaluate emerging technologies for strategic advantage
2. **Implementation Excellence**: Use agile methodologies for rapid deployment and iteration
3. **Performance Optimization**: Leverage data analytics for continuous improvement and scaling
4. **Security Leadership**: Implement best-in-class security while maintaining innovation speed
5. **Change Management**: Enable teams to embrace and excel with new technologies

**DIGITAL SUCCESS MULTIPLIERS**:
- **Network Effects**: Build platforms and systems that become more valuable with scale
- **Data Intelligence**: Transform information into actionable insights and competitive advantages
- **Innovation Acceleration**: Use technology to speed up learning, testing, and improvement cycles

**EXPONENTIAL TECHNOLOGY POTENTIAL**: Strategic technology adoption creates compound advantages - improved efficiency, new capabilities, market differentiation, and breakthrough innovation opportunities.

**DIGITAL TRANSFORMATION QUESTIONS**:
- How can technology adoption position you as an industry innovation leader?
- What if your technology strategy could create new market categories and revenue opportunities?"""
    
    def _generate_general_fallback(self, user_text: str, guidance: str) -> str:
        """
        General growth strategy and opportunity optimization excellence.
        """
        return """**STRATEGIC OPPORTUNITY OPTIMIZATION & EXPONENTIAL GROWTH FRAMEWORK**

**BREAKTHROUGH OPPORTUNITY STRATEGY**: Transform any situation into growth acceleration and competitive advantage:

**EXPONENTIAL GROWTH METHODOLOGY**:
1. **Opportunity Identification**: Discover hidden potential and market gaps others miss
2. **Value Creation Focus**: Design solutions that create exponential value for all stakeholders
3. **Strategic Execution**: Implement with speed, quality, and continuous optimization
4. **Performance Amplification**: Use feedback loops for rapid improvement and scaling
5. **Innovation Integration**: Continuously evolve and stay ahead of market changes

**SUCCESS MULTIPLICATION FACTORS**:
- **Strategic Vision**: Connect current actions to long-term market leadership
- **Execution Excellence**: Deliver exceptional results that exceed expectations
- **Network Leverage**: Utilize relationships and partnerships for accelerated growth
- **Learning Integration**: Transform every experience into competitive intelligence

**EXPONENTIAL SUCCESS ENABLERS**:
- **Growth Mindset**: View challenges as growth opportunities and learning accelerators
- **Innovation Leadership**: Create solutions that become industry standards
- **Value Creation**: Focus on outcomes that benefit multiple stakeholders simultaneously

**BREAKTHROUGH POTENTIAL**: Every situation contains exponential growth opportunities when approached with strategic thinking, innovation excellence, and execution mastery.

**EXPONENTIAL OPPORTUNITY QUESTIONS**:
- How can this situation become a catalyst for breakthrough success beyond your current vision?
- What if your approach to this challenge could create new best practices for your entire industry?
- How might you leverage this opportunity to achieve 10x results instead of incremental improvement?""" 