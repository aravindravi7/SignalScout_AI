# SignalScout AI

SignalScout AI is an automated research monitoring agent that gathers recent AI research items, evaluates their relevance to LLM behavior and evaluation, synthesizes themes, and produces a structured weekly research brief.

The system combines a Streamlit interface with an n8n workflow to create a repeatable research intelligence pipeline.

---

## What the Agent Does

For each run, the agent:

1. Pulls research items from configured sources (e.g., arXiv + RSS feeds)
2. Evaluates each item’s relevance using an LLM
3. Filters items above a relevance threshold
4. Generates structured summaries
5. Synthesizes dominant and emerging research themes
6. Produces a readable research brief (native UI + HTML export)
7. Optionally emails the report

The goal is to transform raw research feeds into actionable intelligence.

---

## User Actions

From the UI, the user can:

### Configure Data Collection
- Set how many items to pull from each source
- Limit how many items get evaluated by the model

### Generate Research Brief
- Trigger the evaluation workflow
- View the structured brief directly in the app
- Inspect included research items and explanations

### Export / Share
- Download formatted HTML report
- Send the brief via email

---

## System Architecture (Minimal Overview)

Streamlit UI  
→ sends parameters to  
n8n Workflow (Webhook Trigger)  
→ ingestion → evaluation → filtering → synthesis → formatting  
→ returns structured JSON + HTML report  
→ Streamlit renders native view + export

The Streamlit app is only a control and visualization layer.  
All reasoning and orchestration logic lives inside the n8n workflow.

---

## Running Locally

### 1. Start n8n
The app expects the workflow webhook to be running locally.

Example:
