# 🏢 AI-Agent Råd

> **Strategiskt Beslutsstödsystem för Företag**

En professionell beslutsplattform som använder flera specialiserade AI-agenter för att tillhandahålla omfattande strategisk analys och rekommendationer på verkställande nivå för komplexa affärsbeslut.

## 🎯 Översikt

AI-Agent Råd är ett företagsfokuserat beslutsstödsystem som simulerar ett styrelserum av expertförfattare. Varje AI-agent bidrar med ett unikt perspektiv till strategiska frågor och levererar strukturerad analys med beprövade affärsramverk som SWOT, kostnad-nyttoanalys och riskbedömningsmetoder.

## ✨ Huvudfunktioner

### 🔬 **Professionellt Beslutsramverk**
- **Strategisk Analys**: McKinsey-graderade strukturerade beslutsramverk
- **Multi-Agent Konsensus**: Delphi-metod och viktad konsensusbyggnad  
- **Verkställande Rapportering**: C-suite färdiga rapporter och instrumentpaneler
- **Riskbedömning**: Omfattande riskanalys med begränsningsstrategier
- **Implementeringsplanering**: Detaljerade handlingsplaner med tidslinjer och framgångsmått

### 🤖 **AI-Agent Förmågor**
- **4 Specialiserade Agenter**: Neutral Analytiker, Strategisk Rådgivare, Riskexpert och Skeptiker
- **Flera AI-Modeller**: OpenRouter-integration med 200+ företagsmodeller
- **Förtroendebetyg**: Automatiserad bedömning av rekommendationstillförlitlighet
- **Kvalitetssäkring**: Inbyggd validering av beslutsprocesser

### 🏗️ **Företagsarkitektur**
- **FastAPI Backend**: Högpresterande API med automatisk dokumentation
- **React Frontend**: Modernt, responsivt webbgränssnitt
- **Realtidsanalys**: Omedelbar strategisk konsultation från flera perspektiv
- **LangGraph Orkestrering**: Avancerad arbetsflödeshantering för komplexa beslut
- **Skalbar Design**: Hanterar enkla frågor till komplexa strategiska initiativ

## 🚀 Snabbstart

### Förutsättningar
- Python 3.8+
- Node.js 16+ (för frontend)
- OpenRouter API-nyckel (för AI-modeller)

### Installation

```bash
# Klona repositoriet
git clone <din-repo-url>
cd ai-agent-council

# Skapa och aktivera virtuell miljö
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Installera beroenden
pip install -r requirements.txt

# Konfigurera miljövariabler
cp .env.example .env
# Redigera .env med din OpenRouter API-nyckel
```

### Köra Applikationen

**Starta Backend:**
```bash
uvicorn backend.main_api:app --reload --host 0.0.0.0 --port 8001
```

**Starta Frontend (valfritt):**
```bash
cd frontend
npm install
npm start
```

### Åtkomstpunkter
- **Frontend**: http://localhost:3000 (React-app)
- **Backend API**: http://localhost:8001
- **API-dokumentation**: http://localhost:8001/docs
- **Hälsokontroll**: http://localhost:8001/api/health

## 🎯 Användningsexempel

### Strategiska Affärsbeslut
```
"Vi överväger att förvärva en konkurrent för 50 miljoner kronor. 
Vilka är de kritiska faktorerna att utvärdera?"
```

### Marknadsexpansion
```
"Bör vårt företag ta sig in på den asiatiska marknaden? 
Analysera marknadsmöjligheter, risker och implementeringsstrategi."
```

### Teknikinvestering
```
"Vi planerar ett AI-transformationsinitiativ för 100 miljoner kronor. 
Utvärdera ROI, risker och implementeringsöversikt."
```

### Organisationsförändring
```
"Bör vi anta en hybridarbetsmodell efter pandemin? 
Analysera kostnader, fördelar och implementeringsutmaningar."
```

## 📊 API-referens

### Professionell Beslutsanalys

#### `POST /api/professional-decision`
Generera strategisk analys på företagsnivå med verkställande rapportering.

**Förfrågan:**
```json
{
  "user_text": "Strategisk fråga eller beslutsscenario",
  "urgency_level": "medium",
  "stakeholder_context": "Styrelse, VD, CFO, aktieägare", 
  "budget_constraints": "Budgetbegränsningar om tillämpligt",
  "timeline_requirements": "Beslutsstidslinje",
  "enable_executive_reporting": true,
  "decision_framework": "auto"
}
```

**Svar:**
```json
{
  "request_id": "unik-identifierare",
  "user_query": "Ursprunglig fråga",
  "professional_decision": {
    "analysis_type": "Fortune 500 Företagsststrategisk Analys",
    "confidence_score": 0.92,
    "strategic_framework": "McKinsey Strategiska Analysramverk",
    "full_analysis": "Detaljerad strategisk analys..."
  },
  "executive_summary": "Verkställandefärdig rekommendation",
  "decision_quality_score": 0.94,
  "confidence_level": "mycket hög",
  "implementation_timeline": "12-18 månaders strategisk implementering",
  "next_actions": ["Åtgärdspunkter..."],
  "risk_assessment": "Riskanalyssammanfattning"
}
```

#### `GET /api/executive-dashboard/{request_id}`
Hämta verkställande instrumentpanelvy av beslutsanalys.

#### `POST /api/export-professional-report/{request_id}`
Exportera professionella rapporter i flera format (HTML, PDF).

### Standardkonsultation

#### `POST /api/decision-with-discussion`
Grundläggande multi-agent konsultation med diskussionsrundor.

#### `POST /api/v2/orchestrated-debate`
Avancerad orkestrering med prestandaövervakning.

## 🏗️ Projektstruktur

```
ai-agent-council/
├── backend/                    # AI-agenter och backend-logik
│   ├── agents/                # Individuella AI-agentimplementationer
│   │   ├── base_agent.py              # Grundagentstruktur
│   │   ├── neutral_agent.py           # Neutral analytiker
│   │   ├── positive_agent.py          # Strategisk rådgivare
│   │   ├── skeptic_agent.py           # Kritisk analytiker
│   │   ├── risk_expert_agent.py       # Riskexpert
│   │   ├── decision_framework.py      # Professionella beslutsramverk
│   │   ├── consensus_manager.py       # Konsensusbyggnad
│   │   └── executive_reporter.py      # Verkställande rapportering
│   ├── orchestration/         # Avancerad orkestrering
│   │   └── langgraph_orchestrator.py  # LangGraph-baserade arbetsflöden
│   ├── evaluation/            # Kvalitetsbedömning
│   ├── technical_depth/       # Prestandaanalys
│   ├── main_api.py           # Huvudsaklig FastAPI-applikation
│   └── config.py             # Konfigurationsinställningar
├── frontend/                  # React webbgränssnitt
│   ├── src/
│   │   ├── components/        # React-komponenter
│   │   └── App.js            # Huvudapplikation
│   └── package.json
├── requirements.txt           # Python-beroenden
└── README.md
```

## 🔧 Konfiguration

### Miljövariabler
```bash
# .env-fil
OPENROUTER_API_KEY=din_openrouter_api_nyckel_här
DEFAULT_MODEL=anthropic/claude-3-haiku
MAX_TOKENS=4000
```

## 🔌 Modellkonfiguration

### OpenRouter-integration
Systemet stöder 200+ AI-modeller via OpenRouter:
- **Anthropic Claude-3**: Bäst för strategisk analys
- **GPT-4**: Utmärkt för komplext resonemang
- **Mixtral-8x7B**: Kostnadseffektiv för de flesta användningsfall
- **DeepSeek-R1**: Avancerad logik och matematisk analys

### Modellanpassning
```python
# Anpassa modeller för specifika agenter
AGENT_MODELS = {
    "Neutral Agent": "anthropic/claude-3-sonnet",
    "Risk Expert": "openai/gpt-4-turbo",
    "Skeptic": "mistralai/mixtral-8x7b-instruct"
}
```

## 📈 Avancerade Funktioner

### LangGraph Orkestrering
- **Dynamiska Arbetsflöden**: AI-drivna beslutsträd
- **Parallellbehandling**: Samtidiga agentanalyser
- **Adaptiv Routing**: Intelligent väg baserat på komplexitet
- **Tillståndshantering**: Beständig kontext mellan rundor

### Metautvärdering
- **Svarskvalitet**: Automatiserad bedömning av agentsvar
- **Konsensusstyrka**: Mäter enighet mellan agenter
- **Förtroendekalibrering**: Justerar förtroendepoäng baserat på historisk noggrannhet
- **Prestationsspårning**: Detaljerade analytiska mått för systemoptimering

### Integrationsmöjligheter
- **REST API**: Fullständig programmatisk åtkomst
- **WebSocket**: Realtidskommunikation för interaktiva sessioner
- **Webhook-stöd**: Automatiserade notifieringar och utlösare
- **Massbehandling**: Hantera flera beslut samtidigt

## 🛡️ Säkerhet och Efterlevnad

### Datahantering
- **Kryptering**: All data krypterad i vila och under transport
- **Åtkomstkontroll**: Rollbaserad behörighetshantering
- **Revision**: Fullständig loggning av alla beslut och interaktioner
- **Datalagring**: Konfigurerbar datalagring med automatisk rensning

### Efterlevnad
- **GDPR-kompatibel**: Inbyggd dataintegritetskontroll
- **SOC2 Typ II**: Säkerhetskontroller på entreprisnivå
- **ISO 27001**: Informationssäkerhetshantering
- **Anpassbar Policy**: Konfigurerbara efterlevnadskontroller

## 🔧 Felsökning

### Vanliga Problem
1. **OpenRouter API-fel**: Kontrollera API-nyckel och begränsningar
2. **Långsamma svar**: Justera timeout-inställningar och modellval
3. **Minnesproblem**: Konfigurera maximal kontext längd
4. **Nätverksproblem**: Verifiera brandvägg och proxy-inställningar

### Felsökningsläge
```bash
# Aktivera detaljerad loggning
export LOG_LEVEL=DEBUG
uvicorn backend.main_api:app --reload
```

## 📚 Utbildning och Support

### Dokumentation
- **API-dokumentation**: Tillgänglig på `/docs` endpoint
- **Utvecklarguide**: Omfattande guider för anpassning
- **Bästa Praxis**: Branschbeprövade implementeringsmönster
- **Användarhandbok**: Steg-för-steg handledning för slutanvändare

### Community Support
- **GitHub Issues**: Bugg rapporter och funktionsförfrågningar
- **Diskussionsforum**: Community-driven support och idéutbyte
- **Exempel och Mallar**: Färdiga lösningar för vanliga användningsfall

## 🚀 Framtida Utveckling

### Planerade Funktioner
- **Flerspråksstöd**: Inbyggd översättning för globala team
- **Mobila Appar**: Native iOS och Android-applikationer
- **Integrationer**: Salesforce, Microsoft Teams, Slack-plugins
- **ML-förbättringar**: Förbättrad prediktiv analys och mönsterigenkänning

### Enterprise-funktioner
- **Single Sign-On (SSO)**: Enterprise-identitetsintegration
- **Anpassade AI-modeller**: Träna modeller på företagsspecifik data
- **Avancerad Analytics**: Detaljerade insikter och rapporter
- **Skalbarhet**: Stöd för stora organisationer och höga volymer

## 📄 Licens

Detta projekt är licensierat under MIT-licensen - se [LICENSE](LICENSE)-filen för detaljer.

## 🤝 Bidrag

Vi välkomnar bidrag! Vänligen läs våra [bidragsriktlinjer](CONTRIBUTING.md) för detaljer om vår hederskodex och processen för att skicka pull requests.

## 📞 Kontakt

- **Projektledare**: Aldar Abdu
- **E-post**: aldar.m.abdu@gmail.com
- **GitHub**: https://github.com/aldarabdu/agent
- **Support**: Skapa en issue på GitHub för teknisk support

---

**🎉 Byggt med ❤️ för att göra strategiska beslut mer intelligenta och datadriven.** 