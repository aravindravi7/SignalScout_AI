from typing import Any, Dict

import requests
import streamlit as st

# Fixed n8n webhook URL for this assignment.
# If you change the workflow, update this value.
WEBHOOK_URL = st.secrets["N8N_WEBHOOK_URL"]

def render_about() -> None:
    with st.expander("About SignalScout AI", expanded=False):
        st.markdown(
            """
**What it does**  
SignalScout AI turns raw AI research feeds into a weekly research brief by evaluating relevance, summarizing key findings, and synthesizing dominant + emerging themes.

**Who it’s for**  
- AI/ML engineers tracking LLM evaluation, safety, and agents  
- Researchers who want “signal over noise” from new papers  
- Product/strategy folks monitoring capability and evaluation trends

**Tech stack**  
- **Streamlit** (UI)  
- **n8n** (workflow orchestration)  
- **LLM-based evaluation + summarization** inside the n8n pipeline  
- Returns **structured JSON** + **HTML brief** for export/sharing
"""
        )


def fmt_dt(iso_like: Any) -> str:
    """Format ISO-ish timestamps into a compact display string."""
    if not iso_like:
        return "—"
    s = str(iso_like)
    # Basic formatting: 2026-02-13T05:41:49.002-05:00 -> 2026-02-13 05:41:49
    s = s.replace("T", " ")
    if "." in s:
        s = s.split(".")[0]
    if "+" in s:
        s = s.split("+")[0].strip()
    return s.strip()


def score_of(item: Dict[str, Any]) -> int:
    o = item.get("output") or item
    try:
        return int(o.get("eval_relevance_score") or o.get("score") or 0)
    except Exception:
        return 0


def tags_of(item: Dict[str, Any]) -> str:
    o = item.get("output") or {}
    tags = (
        o.get("topic_tags")
        or o.get("tags")
        or item.get("topic_tags")
        or item.get("tags")
        or []
    )
    if isinstance(tags, list):
        return ", ".join([str(x) for x in tags if str(x).strip()])
    return str(tags).strip()


def render_report_native(container: Dict[str, Any]) -> None:
    """Render the research brief using native Streamlit components."""
    st.subheader(container.get("report_title", "Madison Agent Research Brief"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Batch", container.get("export_batch_id", "—"))
    with col2:
        st.metric("Generated", fmt_dt(container.get("generated_at", "—")))
    with col3:
        st.metric(
            "Included",
            int(container.get("included_count") or len(container.get("included_items") or [])),
        )

    theme = container.get("theme_synthesis") or {}
    if theme:
        # Keep it open; still uses expander, but no toggle UX needed
        with st.expander("Weekly theme synthesis", expanded=True):
            themes_block = theme.get("themes") or {}

            dominant = (
                themes_block.get("dominant")
                or themes_block.get("dominant_themes")
                or theme.get("dominant_themes")
                or []
            )
            emerging = (
                themes_block.get("emerging")
                or themes_block.get("emerging_themes")
                or theme.get("emerging_themes")
                or []
            )

            tcol1, tcol2 = st.columns(2)

            with tcol1:
                st.markdown("**Top themes**")
                if not dominant:
                    st.write("None")
                else:
                    for t in dominant:
                        if isinstance(t, dict):
                            nm = t.get("theme") or t.get("name") or ""
                            desc = t.get("description") or ""
                            if nm:
                                st.markdown(f"- **{nm}** — {desc}")
                        else:
                            st.markdown(f"- {t}")

            with tcol2:
                st.markdown("**Emerging themes**")
                if not emerging:
                    st.write("None")
                else:
                    for t in emerging:
                        if isinstance(t, dict):
                            nm = t.get("theme") or t.get("name") or ""
                            desc = t.get("description") or ""
                            if nm:
                                st.markdown(f"- **{nm}** — {desc}")
                        else:
                            st.markdown(f"- {t}")

            editorial = (
                (theme.get("editorial_insight") or {}).get("summary")
                if isinstance(theme.get("editorial_insight"), dict)
                else theme.get("editorial_insight")
            )
            meta = (
                (theme.get("meta_observation") or {}).get("note")
                if isinstance(theme.get("meta_observation"), dict)
                else theme.get("meta_observation")
            )

            if editorial:
                st.markdown(f"**Editorial insight:** {editorial}")
            if meta:
                st.markdown(f"*Meta observation:* {meta}")

    items = container.get("included_items") or []
    st.markdown("---")
    st.subheader("Included items")

    if not items:
        st.info("No items met the include threshold (score ≥ 70). Try running again or adjust limits.")
        return

    for it in sorted(items, key=score_of, reverse=True):
        sc = score_of(it)

        # ✅ NEW: hardcode header format, remove "Item" + remove title usage
        header = f"Article Relevance Score - {sc}"

        with st.expander(header):
            tags = tags_of(it)
            if tags:
                st.markdown(f"**Tags:** {tags}")

            o = it.get("output") or {}
            summary = o.get("clean_summary") or o.get("summary") or it.get("summary") or ""
            why = o.get("why_it_matters") or ""
            reason = o.get("action_reason") or ""

            if summary:
                st.markdown(f"**Summary:** {summary}")
            if why:
                st.markdown(f"**Why it matters:** {why}")
            if reason:
                st.markdown(f"*{reason}*")


def main() -> None:
    st.set_page_config(
        page_title="Madison SignalScout AI",
        page_icon="📄",
        layout="wide",
    )

    st.title("Madison SignalScout AI")
    st.caption(
        "Generate a weekly research brief from your configured feeds: "
        "the workflow pulls items, evaluates relevance, summarizes key findings, "
        "extracts dominant + emerging themes and produces a clean brief with the top included papers."
    )

    with st.sidebar:
        st.subheader("Send brief by email")
        send_email_flag = st.checkbox("Send brief by email in this run", value=False)
        email = st.text_input(
            "Your email (Gmail or any)",
            placeholder="you@example.com",
            disabled=not send_email_flag,
        )

        st.markdown("---")

        st.subheader("Data Source Limits")
        st.caption("How many items to pull from each feed and how many to evaluate.")

        arxiv_limit = st.number_input(
            "Arxiv (cs.AI) limit",
            min_value=10,
            max_value=200,
            value=50,
            step=5,
        )
        smol_limit = st.number_input(
            "Smol RSS limit",
            min_value=10,
            max_value=200,
            value=50,
            step=5,
        )
        max_items_eval = st.number_input(
            "Max items to evaluate (up to 320)",
            min_value=10,
            max_value=320,
            value=25,
            step=5,
        )

        st.markdown("---")

        timeout_sec = st.slider(
            "Request timeout (seconds)",
            min_value=10,
            max_value=180,
            value=60,
            step=10,
        )
        
        st.markdown("---")
        st.caption("Built by **Aravind Ravi**")

        cols = st.columns(2)
        with cols[0]:
            st.link_button("GitHub", "https://github.com/aravindravi7")
            st.link_button("LinkedIn", "https://linkedin.com/in/-aravindravi/")
        with cols[1]:
            st.link_button("Portfolio", "https://aravindravi.sites.northeastern.edu/")
            st.link_button("Email", "mailto:aravindravi.academics@gmail.com")

    run_clicked = st.button("▶️ Run workflow and generate brief", use_container_width=True)

    def build_controls() -> Dict[str, Any]:
        return {
            "controls": {
                "arxiv_limit": int(arxiv_limit),
                "smol_limit": int(smol_limit),
                "max_items_eval": int(max_items_eval),
                "send_email": bool(send_email_flag and email),
                "email": email or "",
                # Always use your own API key in n8n; no user-provided key from Streamlit.
                "openai_api_key": None,
            }
        }

    if run_clicked:
        if send_email_flag and not email:
            st.sidebar.error("Please enter an email address or uncheck 'Send brief by email in this run'.")
            return

        payload = build_controls()

        with st.spinner("Calling n8n workflow via webhook..."):
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json=payload,
                    timeout=timeout_sec,
                )
            except requests.RequestException as exc:
                st.error(f"Request to n8n failed: {exc}")
                return

        # Expect JSON from n8n
        try:
            container = response.json()
        except ValueError:
            st.error("n8n did not return JSON. Showing raw text below.")
            st.code(response.text or "<empty response>", language="text")
            return

        # Summary banner
        included_items = container.get("included_items") or []

        num_included = container.get("included_count")
        if num_included is None:
            num_included = len(included_items)

        num_evaled = container.get("evaluated_count")

        # Fallback to user-selected evaluation limit if n8n didn’t return it
        if num_evaled is None:
            num_evaled = int(max_items_eval)

        st.success(
            f"Done. Evaluated **{num_evaled}** items, **{num_included}** included in the brief."
        )

        # Main UI
        render_report_native(container)

        # ✅ NEW: HTML preview/export ALWAYS visible (no expander)
        st.markdown("---")
        st.subheader("HTML preview / export")

        report_html = container.get("report_html", "")
        if report_html:
            st.components.v1.html(report_html, height=700, scrolling=True)
            st.download_button(
                "Download report (HTML)",
                report_html,
                file_name=f"research_brief_{container.get('export_batch_id', 'report')}.html",
                mime="text/html",
            )
        else:
            st.info("No report_html returned from n8n.")


if __name__ == "__main__":
    main()
