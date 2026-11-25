import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Research Desk",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- SESSION STATE ----------
if "result" not in st.session_state:
    st.session_state.result = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "stage_status" not in st.session_state:
    st.session_state.stage_status = ["waiting"] * 4
if "error" not in st.session_state:
    st.session_state.error = None

# ---------- STYLES ----------
st.markdown(
    """
    <style>
    :root {
        --bg:         #171816;
        --bg-2:       #20211F;
        --sidebar:    #1C1D1B;
        --surface:    #252623;
        --text:       #E8E6DF;
        --text-2:     #A6A49B;
        --muted:      #77776F;
        --accent:     #8D9679;
        --accent-2:   #A4AD8D;
        --border:     #343530;
        --ok:         #8D9679;
        --run:        #C9A96A;
        --fail:       #B56B6B;
    }

    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", -apple-system, sans-serif;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }
    header[data-testid="stHeader"] { background: transparent; }
    .block-container { padding-top: 2rem; max-width: 1180px; }

    h1, h2, h3, h4 { font-family: Georgia, "Iowan Old Style", serif; color: var(--text); font-weight: 500; }

    /* ---------- MASTHEAD ---------- */
    .eyebrow {
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.72rem;
        color: var(--accent);
        font-weight: 500;
        margin-bottom: 0.9rem;
    }
    .masthead-title {
        font-family: Georgia, serif;
        font-weight: 400;
        font-size: 2.2rem;
        line-height: 1.25;
        color: var(--text);
        margin: 0 0 0.6rem 0;
        letter-spacing: -0.3px;
    }
    .masthead-sub {
        color: var(--text-2);
        font-size: 1rem;
        max-width: 640px;
        line-height: 1.55;
    }
    .thin-rule {
        height: 1px;
        background: var(--border);
        margin: 1.6rem 0;
        border: 0;
    }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }
    .brand {
        font-family: Georgia, serif;
        font-size: 1.3rem;
        color: var(--text);
        margin: 0;
        font-weight: 500;
    }
    .brand-sub {
        color: var(--muted);
        font-size: 0.78rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 0.25rem;
    }
    .side-section-label {
        color: var(--muted);
        font-size: 0.72rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 1.4rem 0 0.7rem 0;
    }
    .side-step {
        padding: 0.6rem 0;
        border-bottom: 1px solid var(--border);
    }
    .side-step:last-child { border-bottom: 0; }
    .side-step .num {
        color: var(--accent);
        font-size: 0.75rem;
        letter-spacing: 1.5px;
        margin-right: 0.6rem;
    }
    .side-step .name {
        color: var(--text);
        font-size: 0.95rem;
        font-weight: 500;
    }
    .side-step .desc {
        color: var(--muted);
        font-size: 0.8rem;
        margin-top: 0.2rem;
        line-height: 1.5;
    }
    .sys-row {
        display: flex;
        justify-content: space-between;
        padding: 0.35rem 0;
        font-size: 0.8rem;
    }
    .sys-row .k { color: var(--muted); }
    .sys-row .v { color: var(--text-2); }

    /* ---------- INPUT / BUTTON ---------- */
    .input-label {
        color: var(--text-2);
        font-size: 0.78rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .stTextArea textarea, .stTextInput input {
        background: var(--bg-2) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        font-family: Georgia, serif !important;
        font-size: 1.02rem !important;
        padding: 0.9rem 1rem !important;
        transition: border-color 0.18s ease;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background: var(--bg-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 2px !important;
        color: var(--text) !important;
    }
    .stButton>button {
        background: var(--accent);
        color: #1a1b18;
        border: 1px solid var(--accent);
        border-radius: 2px;
        padding: 0.7rem 1.6rem;
        font-weight: 500;
        letter-spacing: 1.5px;
        font-size: 0.8rem;
        text-transform: uppercase;
        font-family: "Inter", sans-serif;
        transition: all 0.18s ease;
    }
    .stButton>button:hover {
        background: var(--accent-2);
        border-color: var(--accent-2);
        color: #1a1b18;
    }

    /* ---------- WORKFLOW ---------- */
    .workflow {
        display: flex;
        justify-content: space-between;
        gap: 0;
        margin: 1.5rem 0 0.5rem 0;
        border: 1px solid var(--border);
        background: var(--bg-2);
        padding: 0;
    }
    .wf-stage {
        flex: 1;
        padding: 1rem 1.1rem;
        border-right: 1px solid var(--border);
        position: relative;
    }
    .wf-stage:last-child { border-right: 0; }
    .wf-stage .wf-num {
        color: var(--muted);
        font-size: 0.72rem;
        letter-spacing: 2px;
    }
    .wf-stage .wf-name {
        font-family: Georgia, serif;
        font-size: 1.05rem;
        color: var(--text);
        margin-top: 0.2rem;
    }
    .wf-stage .wf-status {
        margin-top: 0.4rem;
        font-size: 0.74rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--muted);
    }
    .wf-stage.running .wf-num,
    .wf-stage.running .wf-status { color: var(--run); }
    .wf-stage.done .wf-num,
    .wf-stage.done .wf-status    { color: var(--ok); }
    .wf-stage.fail .wf-num,
    .wf-stage.fail .wf-status    { color: var(--fail); }

    /* ---------- TABS ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid var(--border);
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-2);
        padding: 0.7rem 1.3rem;
        border: 0;
        border-bottom: 2px solid transparent;
        font-family: "Inter", sans-serif;
        font-weight: 500;
        font-size: 0.82rem;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        transition: color 0.15s ease, border-color 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text); }
    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
        border-bottom: 2px solid var(--accent) !important;
        background: transparent !important;
    }

    /* ---------- READING PANE ---------- */
    .reading {
        background: transparent;
        padding: 1.6rem 0.2rem 1rem 0.2rem;
        max-width: 760px;
        line-height: 1.75;
        font-size: 1.02rem;
        color: var(--text);
    }
    .reading h1, .reading h2, .reading h3 {
        font-family: Georgia, serif;
        margin-top: 1.6rem;
        margin-bottom: 0.7rem;
    }
    .reading p { margin: 0.7rem 0; }
    .source-list {
        background: var(--bg-2);
        border: 1px solid var(--border);
        padding: 1.1rem 1.3rem;
        margin-top: 0.8rem;
        font-size: 0.93rem;
        line-height: 1.7;
        color: var(--text-2);
        white-space: pre-wrap;
        font-family: "Inter", sans-serif;
    }

    /* ---------- PROGRESS ---------- */
    .stProgress > div > div > div > div { background: var(--accent); }

    /* ---------- INFO BOXES ---------- */
    div[data-testid="stAlert"] {
        background: var(--bg-2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        color: var(--text);
        border-radius: 2px;
    }

    .caption {
        color: var(--muted);
        font-size: 0.8rem;
        font-family: "Inter", sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def workflow_html(statuses):
    stages = [
        ("01", "Search"),
        ("02", "Read"),
        ("03", "Write"),
        ("04", "Review"),
    ]
    labels = {
        "waiting":   "Waiting",
        "running":   "Running",
        "done":      "Completed",
        "fail":      "Failed",
    }
    cls_map = {"waiting": "", "running": "running", "done": "done", "fail": "fail"}

    html = '<div class="workflow">'
    for (num, name), status in zip(stages, statuses):
        html += (
            f'<div class="wf-stage {cls_map[status]}">'
            f'<div class="wf-num">{num}</div>'
            f'<div class="wf-name">{name}</div>'
            f'<div class="wf-status">{labels[status]}</div>'
            f'</div>'
        )
    html += "</div>"
    return html


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown(
        '<p class="brand">Research Desk</p>'
        '<div class="brand-sub">Independent Research Workspace</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="thin-rule" />', unsafe_allow_html=True)

    st.markdown('<div class="side-section-label">Workflow</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="side-step">
          <span class="num">01</span><span class="name">Search</span>
          <div class="desc">Finds recent, relevant sources on the topic.</div>
        </div>
        <div class="side-step">
          <span class="num">02</span><span class="name">Read</span>
          <div class="desc">Extracts the substance of each source.</div>
        </div>
        <div class="side-step">
          <span class="num">03</span><span class="name">Write</span>
          <div class="desc">Composes a structured research report.</div>
        </div>
        <div class="side-step">
          <span class="num">04</span><span class="name">Review</span>
          <div class="desc">Evaluates the draft for depth and clarity.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="side-section-label">System</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="sys-row"><span class="k">Research engine</span><span class="v">LangChain</span></div>
        <div class="sys-row"><span class="k">Web source</span><span class="v">Tavily</span></div>
        <div class="sys-row"><span class="k">Report format</span><span class="v">Markdown</span></div>
        """,
        unsafe_allow_html=True,
    )

# ---------- MASTHEAD ----------
st.markdown(
    """
    <div class="eyebrow">Research Workspace</div>
    <h1 class="masthead-title">Explore a topic. Understand it deeply.</h1>
    <div class="masthead-sub">Gather sources, analyze evidence, and produce structured research reports.</div>
    <hr class="thin-rule" />
    """,
    unsafe_allow_html=True,
)

# ---------- INPUT ----------
st.markdown('<div class="input-label">Research topic</div>', unsafe_allow_html=True)
topic = st.text_area(
    "topic",
    value=st.session_state.topic,
    placeholder="What would you like to investigate?",
    label_visibility="collapsed",
    height=100,
)

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown('<div class="input-label" style="margin-top:0.6rem;">Depth</div>', unsafe_allow_html=True)
    depth = st.selectbox(
        "depth",
        ["Quick research", "Standard research", "Deep research"],
        index=1,
        label_visibility="collapsed",
    )
with col3:
    st.markdown('<div style="height:2.1rem;"></div>', unsafe_allow_html=True)
    run = st.button("Start Research", use_container_width=True)

# ---------- WORKFLOW PLACEHOLDER ----------
workflow_slot = st.empty()
workflow_slot.markdown(workflow_html(st.session_state.stage_status), unsafe_allow_html=True)

progress_slot = st.empty()
status_slot = st.empty()

# ---------- RUN ----------
if run:
    if not topic.strip():
        st.warning("Please enter a topic before starting.")
        st.stop()

    st.session_state.topic = topic
    st.session_state.result = None
    st.session_state.error = None
    st.session_state.stage_status = ["running", "waiting", "waiting", "waiting"]
    workflow_slot.markdown(workflow_html(st.session_state.stage_status), unsafe_allow_html=True)

    progress = progress_slot.progress(0, text="Preparing agents")
    status_slot.info("Running the pipeline. This may take a minute.")

    try:
        progress.progress(10, text="Search agent is gathering sources")
        result = run_research_pipeline(topic)

        st.session_state.stage_status = ["done", "done", "done", "done"]
        st.session_state.result = result
        progress.progress(100, text="Finished")
        status_slot.success("Research completed.")
        workflow_slot.markdown(workflow_html(st.session_state.stage_status), unsafe_allow_html=True)

    except Exception as e:
        st.session_state.stage_status = [
            s if s == "done" else ("fail" if s == "running" else "waiting")
            for s in st.session_state.stage_status
        ]
        st.session_state.error = str(e)
        progress_slot.empty()
        status_slot.error(f"Pipeline failed: {e}")
        workflow_slot.markdown(workflow_html(st.session_state.stage_status), unsafe_allow_html=True)

# ---------- RESULTS ----------
result = st.session_state.result
if result:
    st.markdown('<hr class="thin-rule" />', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Search Results", "Extracted Sources", "Final Report", "Critic Review"]
    )

    with tab1:
        st.markdown('<div class="eyebrow" style="margin-top:1rem;">Stage 01  ·  Sources gathered</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="source-list">{result.get("search_results", "No results.")}</div>',
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown('<div class="eyebrow" style="margin-top:1rem;">Stage 02  ·  Extracted reading material</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="source-list">{result.get("scraped_content", "No content.")}</div>',
            unsafe_allow_html=True,
        )

    with tab3:
        st.markdown('<div class="eyebrow" style="margin-top:1rem;">Stage 03  ·  Research report</div>', unsafe_allow_html=True)
        st.markdown('<div class="reading">', unsafe_allow_html=True)
        st.markdown(result.get("report", "No report."))
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "Download report (.md)",
            data=result.get("report", ""),
            file_name=f"{st.session_state.topic[:40].replace(' ', '_') or 'research'}_report.md",
            mime="text/markdown",
        )

    with tab4:
        st.markdown('<div class="eyebrow" style="margin-top:1rem;">Stage 04  ·  Critic\'s review</div>', unsafe_allow_html=True)
        st.markdown('<div class="reading">', unsafe_allow_html=True)
        st.markdown(result.get("feedback", "No feedback."))
        st.markdown('</div>', unsafe_allow_html=True)

elif not run:
    st.markdown(
        '<div class="caption" style="margin-top:1.2rem;">'
        'Enter a topic, pick a research depth, and press Start Research. '
        'Each stage will update above as the agents work.'
        '</div>',
        unsafe_allow_html=True,
    )
