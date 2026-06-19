import streamlit as st
import tempfile
import pandas as pd
import plotly.express as px
import time

from services.factcheck_pipeline import run_pipeline
from utils.report_generator import generate_csv

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="FactCheck AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================
# LOAD CSS
# ======================

def load_css():
    st.markdown("""
<div class="circle1"></div>
<div class="circle2"></div>
""", unsafe_allow_html=True)
    try:
        with open(
                "static/style.css",
                "r",
                encoding="utf-8"
        ) as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    except:
        pass


load_css()

# ======================
# SIDEBAR
# ======================

with st.sidebar:

    st.markdown(
        """
        # 🔎 FactCheck AI
        """
    )

    st.caption(
        "AI-powered PDF Fact Verification"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Analytics",
            "📄 Reports",
            "⚙️ Settings",
            "ℹ️ About"
        ]
    )

    st.divider()

    st.markdown("""
<div class='success-card'>

<h4>🚀 Tech Stack</h4>

• Gemini 2.5 Flash<br>
• Tavily Search<br>
• Streamlit<br>
• PyMuPDF

</div>
""",
unsafe_allow_html=True)

# ======================
# HERO SECTION
# ======================

st.markdown("""
<div class="hero-card">

<div class="hero-badge">
🤖 AI Powered Fact Verification
</div>

<h1 class="hero-title">
🔎 FactCheck AI
</h1>

<p class="hero-subtitle">
Detect fake statistics, misleading claims and outdated information inside PDF documents using Gemini AI and live web evidence.
</p>

</div>
""", unsafe_allow_html=True)

# ======================
# KPI CARDS
# ======================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-icon'>⚡</div>
        <div class='metric-label'>Speed</div>
        <div class='metric-value'>&lt;30 sec</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-icon'>🌐</div>
        <div class='metric-label'>Sources</div>
        <div class='metric-value'>5+</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-icon'>🤖</div>
        <div class='metric-label'>Models</div>
        <div class='metric-value'>
        Gemini<br>Tavily
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-icon'>📄</div>
        <div class='metric-label'>PDF Support</div>
        <div class='metric-value'>200 MB</div>
    </div>
    """, unsafe_allow_html=True)

# ======================
# DASHBOARD
# ======================

if page == "🏠 Dashboard":

 upload_container = st.container()

 with upload_container:

    st.markdown("""
    <div class="upload-card">
        <div class="section-title">
         📄 Upload PDF Document
        </div>

        <div class="section-subtitle">
         Upload your document and let AI extract,
         verify and generate evidence-based reports.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        st.markdown(f"""
        <div class='success-card'>

        ✅ <b>{uploaded_file.name}</b>

        <br><br>

        📦 Size:
        {round(uploaded_file.size/(1024*1024),2)} MB

        </div>
        """, unsafe_allow_html=True)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp:

            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        progress_bar = st.progress(0)
        status = st.empty()

        start_time = time.time()

        try:

            status.markdown("""
            <div class='loading-card'>
            🧠 Reading PDF...
            </div>
            """, unsafe_allow_html=True)

            progress_bar.progress(30)

            status.markdown("""
            <div class='loading-card'>
            🌐 Searching Web Evidence...
            </div>
            """, unsafe_allow_html=True)

            results = run_pipeline(pdf_path)

            progress_bar.progress(100)

            status.markdown("""
            <div class='loading-card'>
            🤖 Verifying Claims...
            </div>
            """, unsafe_allow_html=True)

            processing_time = round(
                time.time() - start_time,
                2
            )

            if not results:
                st.warning(
                    "No factual claims found."
                )
                st.stop()

            df = pd.DataFrame(results)

            verified = (
                df["status"] == "Verified"
            ).sum()

            false = (
                df["status"] == "False"
            ).sum()

            inaccurate = (
                df["status"] == "Inaccurate"
            ).sum()

            avg_conf = round(
                df["confidence"].mean(),
                2
            )

            st.subheader(
                "📊 Verification Summary"
            )

            a, b, c, d, e = st.columns(5)

            a.metric(
                "Claims",
                len(df)
            )

            b.metric(
                "Verified",
                verified
            )

            c.metric(
                "False",
                false
            )

            d.metric(
                "Inaccurate",
                inaccurate
            )

            e.metric(
                "Confidence",
                f"{avg_conf}%"
            )

            st.success(
                f"Completed in {processing_time} sec"
            )

            st.divider()

            left, right = st.columns(2)

            with left:

                fig = px.pie(
                    df,
                    names="status",
                    title="Claim Distribution",
                    hole=0.45
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with right:

                chart_df = (
                    df["status"]
                    .value_counts()
                    .reset_index()
                )

                chart_df.columns = [
                    "status",
                    "count"
                ]

                fig2 = px.bar(
                    chart_df,
                    x="status",
                    y="count",
                    title="Status Breakdown"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            st.divider()

            st.subheader(
                "🔍 Search & Filter"
            )

            col1, col2 = st.columns(2)

            with col1:

                selected = st.multiselect(
                    "Status",
                    df["status"].unique(),
                    default=df["status"].unique()
                )

            with col2:

                search = st.text_input(
                    "Search Claim"
                )

            filtered_df = df[
                df["status"].isin(
                    selected
                )
            ]

            if search:

                filtered_df = filtered_df[
                    filtered_df["claim"]
                    .str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

            st.subheader(
                "📝 Results"
            )

            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=450
            )

            st.divider()

            st.subheader(
                "📚 Detailed Evidence"
            )

            for _, row in filtered_df.iterrows():

                with st.expander(
                    f"📝 {row['claim'][:90]}..."
                ):

                    st.write(
                        f"### Status: {row['status']}"
                    )

                    st.write(
                        f"### Confidence: {row['confidence']}%"
                    )

                    if row.get(
                        "corrected_fact"
                    ):
                        st.write(
                            "#### Correct Fact"
                        )
                        st.write(
                            row["corrected_fact"]
                        )

                    if row.get(
                        "evidence"
                    ):
                        st.write(
                            "#### Evidence"
                        )
                        st.write(
                            row["evidence"]
                        )

                    source = row.get(
                        "source"
                    )

                    if source:

                        st.write(
                            "#### Sources"
                        )

                        if isinstance(
                            source,
                            list
                        ):

                            for url in source:
                                st.markdown(
                                    f"- {url}"
                                )

                        else:
                            st.write(
                                source
                            )

            csv_path = generate_csv(
                results
            )

            with open(
                csv_path,
                "rb"
            ) as f:

                st.download_button(
                    label="⬇️ Download Fact Verification Report",
                    data=f,
                    file_name="factcheck_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

# ======================
# ANALYTICS PAGE
# ======================

elif page == "📊 Analytics":

    st.title(
        "📊 Analytics Dashboard"
    )

    st.info(
        "Upload a PDF first to view analytics."
    )

# ======================
# REPORTS PAGE
# ======================

elif page == "📄 Reports":

    st.title(
        "📄 Reports"
    )

    st.write(
        "Generated reports will appear here."
    )

# ======================
# SETTINGS PAGE
# ======================

elif page == "⚙️ Settings":

    st.title(
        "⚙️ Settings"
    )

    st.selectbox(
        "Gemini Model",
        [
            "gemini-2.5-flash"
        ]
    )

    st.slider(
        "Maximum Claims",
        5,
        50,
        20
    )

# ======================
# ABOUT PAGE
# ======================

elif page == "ℹ️ About":

    st.title(
        "ℹ️ About FactCheck AI"
    )

    st.write(
        """
        FactCheck AI is an AI-powered document
        verification system.

        Features:

        • PDF Parsing
        • Claim Extraction
        • Web Search
        • Fact Verification
        • Evidence Generation
        • CSV Report Download
        """
    )

st.markdown("---")
st.caption(
    "Built with ❤️ using Streamlit • Gemini • Tavily • PyMuPDF"
)