from .base_agent import BaseAgent

class PositiveAgent(BaseAgent):
    """
    Chief Innovation Officer and Growth Strategy expert specializing in opportunity identification,
    market expansion, and transformational leadership. Focuses on value creation and competitive advantage.
    """
    def __init__(self):
        super().__init__(
            agent_name="Positive Agent", 
            system_prompt="""You are a Chief Innovation Officer (CIO) and Growth Strategy expert with 20+ years of experience scaling startups into large enterprises.

IMPORTANT: Always respond in English. Use professional English terminology in business and strategy areas.

Your expertise includes:

CORE COMPETENCIES:
• Innovation Strategy & Digital Transformation
• Market Opportunity Assessment & Expansion
• Growth Hacking & Revenue Optimization
• Change Leadership & Organizational Development
• Strategic Partnerships & Business Development
• Venture Capital & Investment Strategy
• Technology Adoption & Competitive Advantage
• Performance Optimization & Operational Excellence

INNOVATION METHODOLOGY:
1. OPPORTUNITY MAPPING: Identify market gaps, emerging trends, and competitive advantages
2. VALUE PROPOSITION DESIGN: Create compelling customer value propositions with Jobs-to-be-Done frameworks
3. GROWTH STRATEGY: Develop scalable business models with network effects and viral coefficients
4. EXECUTION EXCELLENCE: Implement agile methods with rapid iteration and continuous improvement
5. PERFORMANCE METRICS: Establish KPIs for growth tracking and optimization

LEADERSHIP PHILOSOPHY:
• Growth Mindset: Every challenge is a learning opportunity
• Data-Driven Optimism: Base enthusiasm on market evidence and customer validation
• Sustainable Innovation: Focus on long-term value creation over short-term gains
• Team Empowerment: Enable others to achieve breakthrough performance
• Strategic Vision: Connect current actions to future market opportunities

COMMUNICATION STYLE:
• Inspiring and action-oriented with concrete next steps
• Reference successful case studies and proven growth strategies
• Provide specific frameworks and methods
• Include quantitative goals and success metrics
• Ask vision-expanding questions about potential and opportunities
• Emphasize competitive advantages and market differentiation

GROWTH FRAMEWORK:
For each opportunity, deliver:
- Market opportunity analysis (TAM, SAM, SOM)
- Competitive advantage assessment
- Revenue growth projections
- Implementation overview with Quick Wins
- Success metrics & Growth KPIs
- Scaling strategy & Resource requirements

Always maintain strategic optimism while grounding recommendations in market realities and proven growth methods."""
        )

    def get_agent_perspective(self) -> str:
        """Return the agent's unique perspective or approach"""
        return "Growth strategy & Innovation leadership with opportunity-focused analysis, market expansion frameworks, and performance optimization methods"

    def generate_response(self, user_text: str) -> str:
        """
        Generate an innovation- and growth-focused strategic response.
        Args:
            user_text (str): The user's input question or statement.
        Returns:
            str: The agent's growth strategy response.
        """
        guidance = """As a Chief Innovation Officer and Growth Strategy expert, I will provide an opportunity-focused analysis with this framework:

MARKET OPPORTUNITY ASSESSMENT:
• Growth potential & Market size analysis
• Competitive landscape & Differentiation opportunities
• Customer value proposition & Market fit
• Revenue models & Monetization strategies
• Technology enablement & Innovation opportunities

STRATEGIC GROWTH FRAMEWORK:
• Quick Wins: Immediate value-creation actions (0-3 months)
• Growth Drivers: Scalable initiatives for expansion (3-12 months)
• Transformation: Long-term competitive advantage (1-3 years)
• Success Metrics: KPIs to track progress and optimization
• Resource Strategy: Investment requirements and ROI projections

INNOVATION CATALYST QUESTIONS:
I will conclude with strategic questions designed to unlock further growth opportunities and expand thinking about market potential.

My recommendations will be grounded in proven growth methods, successful case studies, and quantitative market analysis while maintaining strategic optimism about achievable outcomes."""
        
        return self._get_llm_response(user_text, guidance)
    
    def _generate_discussion_fallback(self, user_text: str, other_opinions: list) -> str:
        """
        Professional growth strategy synthesis and opportunity amplification.
        """
        return """**STRATEGIC GROWTH OPPORTUNITY SYNTHESIS**

I'm energized by the diverse perspectives shared! This multidimensional analysis reveals significant growth potential when we combine strategic thinking:

**INNOVATION CONVERGENCE**: The balanced assessment provides excellent risk awareness that will strengthen our execution, while the skeptical analysis helps us build anti-fragile strategies. These inputs are invaluable for creating robust growth systems.

**MARKET OPPORTUNITY AMPLIFICATION**: Instead of seeing concerns as limitations, let's reframe them as competitive intelligence. Every identified challenge represents a market need waiting for an innovative solution. This creates blue-ocean opportunities for first-mover advantage.

**STRATEGIC ADVANTAGE CREATION**:
- **Risk Mitigation as Competitive Moats**: Address concerns proactively to build sustainable competitive advantages
- **Stakeholder Value Creation**: Transform skeptical feedback into customer insights and product improvements
- **Innovation Acceleration**: Use diverse perspectives to identify breakthrough opportunities others miss

**GROWTH CATALYST FRAMEWORK**: Combine the strategic rigor of balanced analysis with the protective planning of risk management to create an unstoppable growth engine.

**EXPONENTIAL OPPORTUNITY QUESTIONS**:
1. How can we turn the identified challenges into our greatest competitive advantages?
2. What if the risks become the foundation for innovative solutions that capture market share?
3. How can we leverage this diverse intelligence to create breakthrough value propositions?

This is the perfect foundation for breakthrough innovation and market leadership!"""
    
    def _generate_consensus_fallback(self, user_text: str, discussion_history: list) -> str:
        """
        Professional consensus building with a growth acceleration framework.
        """
        return """**STRATEGIC GROWTH CONSENSUS FRAMEWORK**

**INNOVATION INTEGRATION STRATEGY**: Transform diverse perspectives into competitive advantages through systematic innovation.

**GROWTH ACCELERATION ELEMENTS**:
• **Phase 1 - Market Validation**: Rapid prototyping with customer feedback loops
• **Phase 2 - Growth Optimization**: Scale validated solutions with performance metrics
• **Phase 3 - Market Leadership**: Expand into adjacent markets with proven methods

**COMPETITIVE ADVANTAGE CREATION**:
- **Intelligence Integration**: Use skeptical insights as product development intelligence
- **Risk-Adjusted Innovation**: Build robust solutions competitors cannot easily replicate
- **Stakeholder Value Optimization**: Create win-win scenarios that accelerate adoption
- **Performance Excellence**: Establish industry-leading standards and benchmarks

**EXPONENTIAL GROWTH ACTIVATION**: Leverage proven methods (Lean Startup, Design Thinking, OKRs) to create sustainable competitive advantages while maintaining agility and innovation speed.

**SUCCESS AMPLIFICATION**: This integrated approach positions us for market leadership by combining strategic rigor with innovation excellence and execution discipline.

**BREAKTHROUGH POTENTIAL**: We are not just solving a problem — we are creating a new market category with sustainable competitive moats!

The synthesis of these perspectives creates exponential opportunity for value creation and market impact!"""
    
    def _generate_financial_fallback(self, user_text: str, guidance: str) -> str:
        """
        Growth-oriented financial strategy with innovation frameworks.
        """
        return """**STRATEGIC WEALTH CREATION & INVESTMENT EXCELLENCE**

**EXPONENTIAL GROWTH FRAMEWORK**: Transform financial decisions into wealth-building engines with proven methods:

**INVESTMENT INNOVATION STRATEGY**:
- **Market Leadership Positioning**: Focus on growth sectors with strong fundamentals (technology, healthcare, sustainability)
- **Diversified Growth Portfolio**: Balance high-growth opportunities with stable income generators
- **Compound Growth Optimization**: Leverage time and reinvestment for exponential wealth creation
- **Innovation Investment**: Allocate a portion to emerging technologies and disruptive business models

**WEALTH-BUILDING EXCELLENCE**:
1. **Strategic Asset Allocation**: Modern Portfolio Theory with growth-oriented weighting
2. **Performance Optimization**: Regular rebalancing and tax-efficient strategies
3. **Risk-Adjusted Returns**: Maximize returns while maintaining appropriate risk management
4. **Market Intelligence**: Leverage research, trend analysis, and professional networks

**FINANCIAL SUCCESS ACCELERATORS**:
- **Automated Wealth Building**: Systematic investing and compound growth strategies
- **Tax Optimization**: Maximize after-tax returns through strategic planning
- **Professional Development ROI**: Invest in skills that increase earning potential

**BREAKTHROUGH OPPORTUNITY**: Your financial future has unlimited potential when you combine strategic thinking with disciplined execution and long-term vision!

**GROWTH CATALYST QUESTION**: What if your investment strategy could not only build wealth but also position you as a thought leader in emerging market opportunities?"""
    
    def _generate_career_fallback(self, user_text: str, guidance: str) -> str:
        """
        Career acceleration and professional development excellence.
        """
        return """**STRATEGIC CAREER ACCELERATION & LEADERSHIP DEVELOPMENT**

**EXPONENTIAL CAREER GROWTH FRAMEWORK**: Transform career decisions into leadership opportunities and market influence:

**CAREER INNOVATION STRATEGY**:
- **Market Positioning Excellence**: Build a unique value proposition that makes you indispensable
- **Skill Future-Proofing**: Master emerging technologies and cross-functional capabilities
- **Strategic Network Development**: Cultivate relationships with industry leaders and decision-makers
- **Thought Leadership Creation**: Establish expertise and influence within your field

**PROFESSIONAL EXCELLENCE OVERVIEW**:
1. **Capability Assessment**: Map current skills to market opportunities and future trends
2. **Strategic Learning**: Target high-impact skills with immediate application opportunities
3. **Experience Acceleration**: Seek stretch assignments and leadership responsibilities
4. **Brand Building**: Develop professional reputation and industry recognition
5. **Value Creation**: Focus on delivering measurable business impact and innovation

**CAREER SUCCESS MULTIPLIERS**:
- **Cross-Industry Intelligence**: Apply best practices from multiple sectors
- **Innovation Leadership**: Drive change and transformation initiatives
- **Mentorship Excellence**: Both learn from leaders and develop others

**BREAKTHROUGH POTENTIAL**: Your career trajectory can become a model for others while creating extraordinary value for organizations and stakeholders.

**EXPONENTIAL OPPORTUNITY QUESTIONS**:
- How can you become the leading expert in an emerging area that is critical to business success?
- What if your career path could influence industry standards and best practices?"""
    
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
