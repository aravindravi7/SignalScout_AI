# Madison Research Brief – n8n Webhook UI

This small Streamlit app provides a UI for triggering your n8n workflow (the one defined in `workflow_v2.json`) via **webhook** and viewing the resulting research brief.

## Prerequisites

- Python 3.9+ recommended
- Your n8n workflow must:
  - Start from a **Webhook** trigger (instead of Manual Trigger)
  - Be configured so the webhook **response** returns the JSON from the node that builds the brief (e.g. the `Build Research Brief HTML` node, which outputs `report_title` and `report_html`).

## Setup

From this `A5` folder:

```bash
python -m venv .venv
source .venv/bin/activate  # on macOS / Linux
# .venv\Scripts\activate   # on Windows (PowerShell / cmd)

pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

This will open the Streamlit UI in your browser.

## Using the UI

1. **In the sidebar**, paste your full n8n **Webhook URL**  
   (e.g. `https://<your-host>/webhook/<id>` or `/webhook-test/<id>`).
2. Optionally adjust the **JSON payload** (defaults to `{}`), if your workflow expects input.
3. Click **“Run n8n Workflow”**.
4. The app will:
   - Show the **HTTP status code**.
   - Show the **raw JSON** returned by n8n.
   - If it finds a `report_html` field anywhere in the JSON, it will render the
     research brief nicely inside the page.

If you don’t see the rendered brief, double‑check that your webhook’s response
is configured to return the node that contains `report_html`.

