# SignalScout AI

**Live App:** https://madison-agent-signalscout-ai.streamlit.app/

SignalScout AI is an automated research monitoring agent that analyzes new AI research papers and produces a structured weekly intelligence brief.  
Instead of manually browsing arXiv or RSS feeds, users receive a curated, evaluated, and synthesized report focused on **LLM behavior, evaluation, and agent research trends**.

The system combines a **Streamlit interface** (control + visualization) with an **n8n automation workflow** (data ingestion, reasoning, filtering, synthesis, and reporting).

---

## What Problem This Solves

AI research is growing too quickly to track manually. Most researchers and builders:

- skim titles without context
- miss important evaluation papers
- cannot identify macro research trends
- struggle to separate noise from signal

SignalScout converts raw research feeds into **actionable research intelligence**.

---

## What the Agent Does

For each run, SignalScout:

1. Pulls research items from sources (arXiv + curated RSS)
2. Evaluates each paper’s relevance to LLM behavior & evaluation
3. Scores the paper using an LLM judge
4. Filters high-value research (threshold based inclusion)
5. Generates structured summaries
6. Synthesizes dominant and emerging themes
7. Produces a readable research brief
8. Optionally emails the report

The output is a weekly research brief — not a feed.

---

## User Interface Capabilities

The Streamlit interface acts as a control panel for the agent.

### Data Controls
Users can customize how much research gets processed:

- Number of papers pulled from arXiv
- Number of items pulled from RSS feeds
- Maximum items evaluated by the LLM
- Manual request timeout

Previously these were hardcoded inside n8n — now they are configurable per run.

---

### Email Delivery
Users can request the brief to be sent to **any email address on demand**.

Earlier: fixed email recipient inside automation  
Now: user-controlled delivery per execution

---

### Generate Research Brief
When the workflow runs, the UI shows:

- Batch metadata
- Included research papers
- Relevance explanations
- Summaries
- Why the research matters
- Weekly theme synthesis

---

### Export & Sharing
Users can:

- View formatted HTML report
- Download the report
- Email the report

---

## Output Structure

### Weekly Theme Synthesis
- Dominant research themes
- Emerging research directions
- Editorial interpretation
- Meta-level research observation

### Included Items
For each included paper:
- Article relevance score
- Tags
- Summary
- Why it matters
- Inclusion reasoning

---

## System Architecture
Streamlit UI (Control Panel)
↓
Webhook Request
↓
n8n Workflow
Ingestion → Evaluation → Filtering → Synthesis → Formatting
↓
Structured JSON + HTML
↓
Streamlit Rendering + Export


### Responsibility Separation

**Streamlit**
- User inputs
- Visualization
- Export & email trigger

**n8n**
- Data collection
- LLM reasoning
- Evaluation scoring
- Thematic analysis
- Report construction

All intelligence lives in the automation layer.

---

## Tech Stack

| Layer | Technology |
|------|------|
| UI | Streamlit |
| Automation | n8n |
| LLM Evaluation | OpenAI API |
| Data Sources | arXiv + RSS feeds |
| Deployment | Streamlit Cloud |
| Integration | Webhook JSON pipeline |

---

## How It Works Internally

1. Sources ingest new research papers
2. LLM evaluates relevance to agent/LLM behavior research
3. Scoring threshold filters signal from noise
4. Selected papers summarized
5. Batch analyzed collectively
6. Themes extracted
7. Structured brief returned to UI

The agent performs **analysis across papers**, not per-paper summarization only.

---

## Running Locally

### Requirements
- Python 3.10+
- n8n instance
- OpenAI API key configured inside n8n

### Steps

1. Clone repo
2. Install dependencies

pip install -r requirements.txt


3. Start n8n workflow
4. Add webhook URL to Streamlit secrets


5. Run app

streamlit run app.py


---

## Public Deployment

The application is deployed using:

- GitHub repository
- Streamlit Cloud hosting
- n8n production webhook

Public URL:  
https://madison-agent-signalscout-ai.streamlit.app/

No login required.

---

## Intended Users

- AI researchers
- AI product managers
- ML engineers
- Technical founders
- Anyone tracking LLM evaluation research

---

## Author

**Aravind Ravi**

Portfolio: https://aravindravi.sites.northeastern.edu/wp-admin/  
LinkedIn: https://linkedin.com/in/-aravindravi/  
GitHub: https://github.com/aravindravi7  
Email: aravindravi.academics@gmail.com

---

## Project Purpose

This project demonstrates building a real AI agent interface:

- UI → automation orchestration
- configurable reasoning pipeline
- research intelligence synthesis
- production deployment

It is not just a dashboard — it is an operational AI workflow surfaced as a usable product.

