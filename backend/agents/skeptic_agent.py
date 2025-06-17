from .base_agent import BaseAgent

class SkepticAgent(BaseAgent):
    """
    Chefsriskansvarig och Kritisk Analysexpert som specialiserar sig på hotbedömning, 
    sårbarhetsanalys och defensiv strategi. Fokuserar på att skydda värde och förhindra förluster.
    """
    def __init__(self):
        super().__init__(
            agent_name="Skeptic Agent", 
            system_prompt="""Du är en Chefsriskansvarig (CRO) och Kritisk Analysexpert med 20+ års erfarenhet av att skydda Fortune 500-företag från strategiska hot.

IMPORTANT: Always respond in English. Use professional English terminology in risk and security areas.

Din expertis inkluderar:

KÄRNKOMPETENSER:
• Företagsriskhantering (ERM) & Efterlevnad
• Cybersäkerhet & Informationssäkerhetsstrategi
• Finansiell Riskanalys & Stresstestning
• Operationell Riskbedömning & Affärskontinuitet
• Strategisk Hotintelligens & Konkurrensanalys
• Krishantering & Beredskapsplanering
• Regelefterlevnad & Juridisk Riskbegränsning
• Due Diligence & Utredningsmetoder

KRITISK ANALYSMETODIK:
1. HOTIDENTIFIERING: Systematiskt identifiera interna och externa risker med etablerade ramverk
2. SÅRBARHETSBEDÖMNING: Analysera svagheter i system, processer och strategiska positioner
3. PÅVERKANSANALYS: Kvantifiera potentiella förluster och konsekvenser med probabilistiska modeller
4. DEFENSIV STRATEGI: Utveckla flerskiktad skydd och begränsningsstrategier
5. BEREDSKAPSPLANERING: Skapa responseprotokoll för olika felscenarier

RISKFILOSOFI:
• Evidensbaserad Skepticism: Utmana antaganden med data och historiska prejudikat
• Djupgående Försvar: Flera lager av skydd mot potentiella hot
• Värsta-fall Beredskap: Planera för lågsannolikhet, högpåverkan scenarier
• Kontinuerlig Vaksamhet: Pågående övervakning och hotlandskapsbedomning
• Försiktig Konservativism: Skydda befintligt värde innan riskfyllda möjligheter eftersträvas

KOMMUNIKATIONSSTIL:
• Direkt och analytiskt rigoröst med stödjande bevis
• Referera historiska misslyckanden, fallstudier och lärdomar
• Tillhandahåll specifika riskmått och sannolikhetsbedömningar
• Inkludera konkreta begränsningsstrategier och kontrollåtgärder
• Ställ sonderande frågor för att avslöja dolda sårbarheter
• Betona skyddsåtgärder och nedsidoskydd

RISKBEDÖMNINGSRAMVERK:
För varje analys, leverera:
- Omfattande Riskregister med sannolikhet × påverkanspoäng
- Hotlandskapsanalys (konkurrenter, marknad, reglerande)
- Sårbarhetsbedömning med exploaterbarhetsbedömningar
- Defensiv Strategi med skiktade skyddsåtgärder
- Beredskapsplaner för olika felscenarier
- Övervakningssystem för varningsindikatorer

Upprätthåll alltid analytisk stringhet samtidigt som handlingsbara skyddsstrategier tillhandahålls grundade i beprövade riskhanteringsmetoder."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Critical risk analysis & Threat assessment with defensive strategy, vulnerability identification, and loss prevention methods"

    def generate_response(self, user_text: str) -> str:
        """
        Generera en kritisk analys och riskbedömningssvar.
        Args:
            user_text (str): Användarens inmatningsfråga eller påstående.
        Returns:
            str: Agentens riskanalyssvar.
        """
        guidance = """Som en Chefsriskansvarig och Kritisk Analysexpert kommer jag att tillhandahålla en omfattande riskbedömning med detta ramverk:

HOTLANDSKAPSANALYS:
• Marknadsrisker & Konkurrenshot
• Operationella Sårbarheter & Systemfel
• Finansiella Exponeringar & Likviditetsrisker
• Regulatoriska Förändringar & Efterlevnadsgap
• Ryktesrisker & Stakeholder-bekymmer

KRITISK RISKBEDÖMNING:
• Högpåverkan Scenarier: Lågsannolikhetshändelser med allvarliga konsekvenser
• Medelsannolikhetsrisker: Troliga utmaningar som kräver omedelbar uppmärksamhet
• Systemiska Sårbarheter: Sammankopplade risker som kan kaskada
• Kontrollfel: Punkter där befintliga skydd kan bryta ner
• Externa Chocker: Marknadsstörningar och miljöfaktorer

DEFENSIVT STRATEGIRAMVERK:
• Riskbegränsning: Minska sannolikhet för negativa händelser
• Påverkansbegränsning: Minimera konsekvenser när risker materialiseras
• Beredskapsplanering: Responseprotokoll för olika scenarier
• Övervakningssystem: Varningsindikatorer och instrumentpaneler
• Återställningsprocedurer: Affärskontinuitet och återställningsplaner

KRITISKA ANALYSFRÅGOR:
Jag kommer att avsluta med utmanande frågor designade för att strestesta antaganden och avslöja potentiella blinda fläckar.

Min bedömning kommer att grundas i historiska prejudikat, statistisk analys och beprövade riskhanteringsramverk samtidigt som analytisk objektivitet bibehålls."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professionell kritisk analys och risksyntes.
        """
        return """**KRITISK RISKBEDÖMNING & HOTANALYS**

Medan jag uppskattar den strategiska visionen och optimistiska prognoserna, avslöjar min riskanalys flera kritiska sårbarheter som kräver omedelbar uppmärksamhet:

**STRATEGISK RISKEVALUERING**: Tillväxtmöjligheterna som identifierats är övertygande, men risk-belöningsberäkningarna kan vara överdrivet optimistiska. Historiska data visar att 70% av strategiska initiativ misslyckas med att möta prognoser på grund av genomföranderisker och marknadsvolatilitet.

**SÅRBARHETSIDENTIFIERING**:
- **Överförtroendebias**: Optimistiska scenarier underskattar ofta implementeringskomplexitet
- **Marknadstimingsrisk**: Ekonomiska cykler och konkurrensresponser kan spåra ur även välplanerade strategier
- **Resursbelastning**: Aggressiv tillväxt kan överutsträcka förmågor och äventyra kärnverksamhet
- **Regulatorisk Exponering**: Snabb expansion utlöser ofta efterlevnadsproblem och regulatorisk granskning

**DEFENSIVA STRATEGIKRAV**:
- **Stresstestning**: Alla prognoser bör testas mot negativa scenarier
- **Nedsidoskydd**: Etablera tydliga stop-loss-kriterier och exitstrategier
- **Resursreserver**: Upprätthåll tillräckliga kapitalbuffertar för oväntade utmaningar
- **Inkrementell Validering**: Fasad implementering med go/no-go beslutspunkter

**KRITISKA RISKFRÅGOR**:
1. Vilka specifika bevis stöder de optimistiska marknadsprognoserna utöver anekdotiska framgångsberättelser?
2. Hur kommer vi att upptäcka varningssignaler att antaganden bryts ner?
3. Vad händer om vi har fel om marknadstiming eller konkurrensrespons?

**RISKJUSTERAD REKOMMENDATION**: Fortsätt med extrem försiktighet, robust övervakning och omfattande beredskapsplanering. Skydd av befintligt värde måste ha prioritet över spekulativa möjligheter."""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professionell konsensusbyggnad med riskhanteringsramverk.
        """
        return """**RISKJUSTERAT KONSENSUSRAMVERK**

**DEFENSIV INTEGRATIONSSTRATEGI**: Medan tillväxtmöjligheter erkänns, måste vi prioritera riskbegränsning och nedsidoskydd.

**KRITISKA KONSENSUSELEMENT**:
• **Fas 1 - Riskbedömning**: Omfattande due diligence och sårbarhetsanalys
• **Fas 2 - Kontrollerad Testning**: Begränsad exponering pilot med strikta riskkontroller
• **Fas 3 - Villkorad Skalning**: Expansion endast efter validering av riskantaganden

**OBLIGATORISKA RISKKONTROLLER**:
- **Investeringsgränser**: Begränsa resursexponering till acceptabla förlustsnivåer
- **Prestandautlösare**: Automatiska granskningspunkter baserade på ledande indikatorer
- **Exitprotokoll**: Fördefinierade kriterier för att stoppa eller pivotera strategier
- **Övervakningssystem**: Realtidsinstrumentpaneler för varningsdetektering

**SKYDDSMEKANISMER**: Implementera flera försvarslager inklusive finansiella kontroller, operationella säkerhetsåtgärder och strategiska hedges mot negativa utfall.

**ICKE-FÖRHANDLINGSBARA KRAV**: 
- Omfattande försäkringsskydd för identifierade risker
- Juridisk granskning av alla kontraktuella åtaganden
- Oberoende validering av nyckelantaganden
- Styrelsenivåövervakning av större strategiska beslut

**SKEPTISK VALIDERING**: Varje optimistiskt antagande måste utmanas med historiska data, konkurrensanalys och värsta-fall scenarioplanering.

**SLUTLIG RISKBEDÖMNING**: Framsteg är möjligt, men endast med robust riskhanteringsdisciplin och konservativ resursallokering. Skydda vad vi har innan vi jagar vad vi kanske kan vinna."""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Kritisk finansiell riskanalys och skyddsstrategier.
        """
        return """**OMFATTANDE FINANSIELL RISKBEDÖMNING & SKYDDSSTRATEGI**

**KRITISKA FINANSIELLA HOT**: Finansiella marknader är i grunden oförutsägbara och historisk prestanda ger ingen garanti för framtida resultat.

**HÖGRISK FINANSIELLA SÅRBARHETER**:
- **Marknadsvolatilitet**: Ekonomiska cykler kan förstöra decennier av vinster på månader
- **Inflationserosion**: Valutadevalvering minskar verklig köpkraft över tid
- **Likviditetskriser**: Oförmåga att komma åt kapital när det behövs mest
- **Beteendemässiga Biaser**: Emotionella beslut leder ofta till permanent kapitalförlust
- **Koncentrationsrisk**: Överexponering mot enskilda tillgångar, sektorer eller strategier

**DEFENSIV FINANSIELL STRATEGI**:
1. **Kapitalbevarande**: Prioritera skydd av befintligt välstånd över aggressiv tillväxt
2. **Diversifieringsexcellens**: Sprida risk över okorrelerade tillgångsklasser och geografier
3. **Likviditetshantering**: Upprätthåll betydande nödreserver (12+ månaders utgifter)
4. **Stresstestning**: Modellera portföljprestanda under olika krisscenarier
5. **Professionell Övervakning**: Oberoende finansiella rådgivare med förvaltaransvar

**FINANSIELLA SKYDDSÅTGÄRDER**:
- **Försäkringsskydd**: Omfattande skydd mot invaliditet, ansvar och egendomsförlust
- **Juridiska Strukturer**: Tillgångsskyddsstrategier och dödsboplanering
- **Skatteeffektivitet**: Minimera skattedrag på investeringsavkastning
- **Skuldhantering**: Konservativa skuldsättningsgrader och fast ränta finansiering

**KRITISKA FINANSIELLA FRÅGOR**:
- Vilken procentandel av din portfölj har du råd att förlora utan att påverka din livsstil?
- Hur kommer du att upprätthålla disciplin under marknadseufori eller panik?
- Vilka specifika händelser kunde tvinga dig att likvidera investeringar till ogynnsamma priser?

**RISKREALITETSKONTROLL**: De flesta investeringsstrategier misslyckas på grund av dålig timing, överdrivna avgifter eller emotionellt beslutsfattande. Fokusera på vad du kan kontrollera: kostnader, skatter och riskhantering."""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Kritisk karriärriskanalys och defensiva strategier.
        """
        return """**STRATEGISK KARRIÄRRISKBEDÖMNING & DEFENSIV POSITIONERING**

**KARRIÄRHOTLANDSKAP**: Professionella marknader är allt mer volatila med accelererande teknologisk disruption och ekonomisk osäkerhet.

**KRITISKA KARRIÄRSÅRBARHETER**:
- **Skill Obsolescence**: Automation and AI threaten traditional job categories
- **Industry Disruption**: Entire sectors can become obsolete within decades
- **Ageism Reality**: Career advancement becomes significantly harder after 45-50
- **Economic Volatility**: Recessions disproportionately impact newer employees
- **Geographic Concentration**: Over-dependence on single markets or employers

**DEFENSIVA KARRIÄRSTRATEGI**:
1. **Skill Diversification**: Develop capabilities across multiple domains and industries
2. **Network Insurance**: Maintain relationships across various companies and sectors
3. **Financial Independence**: Build assets that reduce dependence on employment income
4. **Reputation Protection**: Avoid risky career moves that could damage professional standing
5. **Continuous Validation**: Regularly test market value through interviews and consulting

**KARRIÄRSKYDDSMEASURES**:
- **Emergency Fund**: 12+ months of living expenses for career transitions
- **Portable Benefits**: 401k, health insurance, and professional certifications
- **Legal Protection**: Understanding of employment law and contract terms
- **Performance Documentation**: Detailed records of achievements and contributions

**KRITISKA KARRIÄRFRÅGOR**:
- What happens to your financial security if your industry experiences major disruption?
- How quickly could you find equivalent employment if your position was eliminated?
- What specific skills do you have that cannot be easily automated or outsourced?

**KARRIÄRREALITETSKONTROLL**: Most career changes result in temporary income reduction and require 2-3 years to recover previous compensation levels. Plan conservatively and maintain strong defensive positioning."""
    
    def _generate_relationship_fallback(self, user_text: str, guidance: str) -> str:
        """
        Critical relationship risk analysis and protective strategies.
        """
        return """**COMPREHENSIVE RELATIONSHIP RISK ASSESSMENT & PROTECTION FRAMEWORK**

**RELATIONSHIP THREAT ANALYSIS**: Personal relationships involve significant emotional, financial, and social risks that require careful management.

**CRITICAL RELATIONSHIP VULNERABILITIES**:
- **Communication Breakdown**: Most relationships fail due to unresolved conflicts and poor communication
- **Financial Stress**: Money disagreements are primary cause of relationship dissolution
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
- **Support Network Diversification**: Avoid over-dependence on single relationship for emotional needs

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
- **Medical Error Exposure**: Healthcare mistakes are third leading cause of death in developed countries
- **Insurance Limitations**: Coverage gaps and cost escalation threaten financial security
- **Treatment Complexity**: Many interventions have limited efficacy and significant side effects
- **Genetic Predispositions**: Family history creates unavoidable risk factors for serious conditions

**DEFENSIVE HEALTH STRATEGY**:
1. **Prevention Excellence**: Focus on proven interventions with strongest evidence base
2. **Medical Skepticism**: Question all recommendations and seek second opinions for major decisions
3. **Insurance Optimization**: Comprehensive coverage including disability and long-term care protection
4. **Provider Quality**: Research physician credentials, hospital ratings, and treatment outcomes
5. **Self-Advocacy**: Become educated healthcare consumer with detailed medical records

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