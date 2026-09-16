import streamlit as st
from engine.engine import WikiVerifyEngine
import os

# Page Config
st.set_page_config(page_title="WikiVerify Pro", page_icon="🛡️", layout="wide")

st.title("🛡️ WikiVerify Pro")
st.markdown("### The Intelligence Auditor for Global Knowledge")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    en_data_path = st.text_input(
        "English Data Path",
        value="./data/enwiki/*.parquet",
        help="Path to English Wikipedia Parquet files."
    )
    fr_data_path = st.text_input(
        "French Data Path",
        value="./data/frwiki/*.parquet",
        help="Path to French Wikipedia Parquet files."
    )
    llm_key = st.text_input("LLM API Key", type="password", help="Provide an API key to enable AI-powered summaries.")

    st.divider()
    st.info("WikiVerify Pro now supports cross-language auditing and AI summaries.")

# Main UI
topic = st.text_input("What would you like to verify?", placeholder="e.g., Quantum Computing")

if topic:
    if not en_data_path:
        st.error("Please provide the English Data Path in the sidebar.")
    else:
        try:
            engine = WikiVerifyEngine(en_data_path)

            with st.spinner(f"Auditing '{topic}'..."):
                article = engine.search_article(topic)

            if article:
                report = engine.analyze_credibility(article)

                # --- CROSS LANGUAGE AUDIT ---
                st.subheader("🌍 Global Knowledge Audit")
                if fr_data_path:
                    audit_res = engine.cross_language_audit(topic, fr_data_path)
                    c1, c2, c3 = st.columns([1, 1, 2])

                    en_score = audit_res['en']['overall_score'] if audit_res['en'] else 0
                    fr_score = audit_res['fr']['overall_score'] if audit_res['fr'] else 0

                    c1.metric("English Score", f"{en_score}%")
                    c2.metric("French Score", f"{fr_score}%")
                    c3.info(f"**Verdict:** {audit_res['comparison']}")
                else:
                    st.warning("Provide French Data Path in sidebar to enable Global Audit.")

                st.divider()

                # Top Metrics
                col1, col2, col3, col4 = st.columns(4)
                score = report['overall_score']
                col1.metric("Local Credibility", f"{score}%")
                col2.metric("Verified Sections", report['verified_sections'])
                col3.metric("Unsupported Claims", report['unsupported_claims'], delta_color="inverse")
                col4.metric("Unique Sources", report['source_count'])

                # Tabs for different views
                tab1, tab2, tab3 = st.tabs(["🛡️ Credibility Report", "📌 Intelligence Summary", "🗺️ Visual Structure"])

                with tab1:
                    left_col, right_col = st.columns(2)
                    with left_col:
                        st.subheader("🔍 Evidence Breakdown")
                        st.write(f"**Article:** {report['name']}")
                        st.write(f"**URL:** [Link]({report['url']})")
                        st.write("#### Trust Level")
                        st.progress(score / 100, text=f"Overall Trust: {score}%")
                        st.write(f"- **Risk Areas:** {report['risk_areas']}")
                        st.write(f"- **Gaps:** {report['unsupported_claims']}")

                    with right_col:
                        st.subheader("📚 Source Health")
                        st.write(f"**Diversity Level:** {report['diversity']}")
                        st.write(f"**Total Unique Citations:** {report['source_count']}")
                        st.bar_chart({"Verified": report['verified_sections'], "Risky": report['risk_areas'], "Unsupported": report['unsupported_claims']})

                with tab2:
                    st.subheader("📌 Article Intelligence")
                    if llm_key:
                        st.success("AI-powered summarization active.")

                    points = engine.extract_key_points(article, llm_api_key=llm_key)
                    for p in points:
                        st.markdown(f"✅ {p}")

                with tab3:
                    st.subheader("🗺️ Visual Content Map")
                    flowchart_code = engine.generate_flowchart(article)
                    img_url = engine.get_mermaid_url(flowchart_code)

                    # Display the rendered image
                    st.image(img_url, caption="Interactive Article Structure Map")

                    with st.expander("View Mermaid Code"):
                        st.code(flowchart_code, language="mermaid")

            else:
                st.warning("No article found matching that topic. Try being more specific.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
