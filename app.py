import os
import certifi
import streamlit as st

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# ENVIRONMENT
# ============================================================

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# ============================================================
# CHECK API KEYS
# ============================================================

if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY is missing from your .env file.")
    st.stop()

if not TAVILY_API_KEY:
    st.error("❌ TAVILY_API_KEY is missing from your .env file.")
    st.stop()


# ============================================================
# GLOBAL CSS
# ============================================================

st.html("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --pink: #ff00cc;
    --pink-light: #ff4de1;
    --purple: #8a2be2;
    --dark: #050008;
    --dark2: #0b0010;
    --border: rgba(255, 0, 204, 0.35);
    --text: #ffffff;
    --muted: #a9a0ad;
}


/* PAGE */

.stApp {
    background:
        radial-gradient(
            circle at 50% -10%,
            rgba(255, 0, 204, 0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at 0% 50%,
            rgba(138, 43, 226, 0.10),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #030006 0%,
            #09000e 50%,
            #030006 100%
        );

    color: var(--text);
}


/* REMOVE STREAMLIT TOP SPACE */

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px;
}


/* HERO */

.hero {
    text-align: center;
    padding: 40px 20px 25px 20px;
}


.hero-badge {
    display: inline-block;

    padding: 8px 18px;

    border: 1px solid rgba(255, 0, 204, 0.55);

    border-radius: 50px;

    background: rgba(255, 0, 204, 0.06);

    color: #ff5be2;

    font-family: 'Orbitron', sans-serif;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 3px;

    box-shadow:
        0 0 15px rgba(255, 0, 204, 0.15),
        inset 0 0 15px rgba(255, 0, 204, 0.04);
}


.hero-title {
    margin-top: 20px;

    font-family: 'Orbitron', sans-serif;

    font-size: clamp(45px, 8vw, 90px);

    font-weight: 900;

    letter-spacing: 5px;

    line-height: 1;

    color: white;

    text-shadow:
        0 0 10px rgba(255, 255, 255, 0.2),
        0 0 35px rgba(255, 0, 204, 0.25);
}


.hero-title span {
    color: #ff00cc;

    text-shadow:
        0 0 10px #ff00cc,
        0 0 30px rgba(255, 0, 204, 0.7),
        0 0 60px rgba(255, 0, 204, 0.4);
}


.hero-subtitle {
    margin-top: 18px;

    color: #aaa1af;

    font-family: 'Inter', sans-serif;

    font-size: 16px;

    letter-spacing: 2px;
}


/* STATUS CARD */

.status-card {

    margin: 25px auto 35px auto;

    max-width: 600px;

    padding: 18px 24px;

    border: 1px solid rgba(255, 0, 204, 0.28);

    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            rgba(255, 0, 204, 0.08),
            rgba(80, 0, 100, 0.05)
        );

    box-shadow:
        0 0 30px rgba(255, 0, 204, 0.08),
        inset 0 0 20px rgba(255, 0, 204, 0.02);
}


.status-row {

    display: flex;

    align-items: center;

    gap: 15px;

}


.status-dot {

    width: 12px;

    height: 12px;

    border-radius: 50%;

    background: #00ff88;

    box-shadow:
        0 0 8px #00ff88,
        0 0 20px rgba(0, 255, 136, 0.7);

    animation: pulse 1.5s infinite;
}


.status-main {

    color: white;

    font-family: 'Orbitron', sans-serif;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 2px;
}


.status-sub {

    margin-top: 4px;

    color: #8e8492;

    font-size: 12px;

}


/* INPUT AREA */

.input-title {

    margin-bottom: 10px;

    color: #ff5be2;

    font-family: 'Orbitron', sans-serif;

    font-size: 12px;

    letter-spacing: 2px;

}


/* TEXT AREA */

textarea {

    background: rgba(255, 255, 255, 0.025) !important;

    color: white !important;

    border: 1px solid rgba(255, 0, 204, 0.35) !important;

    border-radius: 14px !important;

    font-size: 15px !important;

}


textarea:focus {

    border: 1px solid #ff00cc !important;

    box-shadow:
        0 0 10px rgba(255, 0, 204, 0.3),
        0 0 30px rgba(255, 0, 204, 0.08) !important;

}


/* BUTTON */

.stButton > button {

    width: 100%;

    min-height: 55px;

    margin-top: 12px;

    border: 1px solid #ff00cc !important;

    border-radius: 14px !important;

    background:
        linear-gradient(
            90deg,
            #ff00cc,
            #b000ff
        ) !important;

    color: white !important;

    font-family: 'Orbitron', sans-serif !important;

    font-size: 13px !important;

    font-weight: 800 !important;

    letter-spacing: 2px !important;

    box-shadow:
        0 0 15px rgba(255, 0, 204, 0.35),
        0 0 40px rgba(255, 0, 204, 0.12);

    transition: all 0.25s ease;

}


.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 20px rgba(255, 0, 204, 0.55),
        0 0 60px rgba(255, 0, 204, 0.25);

}


/* THINKING CARD */

.thinking-card {

    margin-top: 30px;

    padding: 25px;

    border-radius: 18px;

    border: 1px solid rgba(255, 0, 204, 0.3);

    background:
        linear-gradient(
            135deg,
            rgba(255, 0, 204, 0.08),
            rgba(120, 0, 150, 0.04)
        );

    text-align: center;

    box-shadow:
        0 0 35px rgba(255, 0, 204, 0.08);
}


.thinking-icon {

    font-size: 38px;

    animation:
        thinkingPulse 1.2s infinite;

}


.thinking-title {

    margin-top: 10px;

    color: white;

    font-family: 'Orbitron', sans-serif;

    font-size: 14px;

    letter-spacing: 2px;

}


.thinking-text {

    margin-top: 8px;

    color: #aaa1af;

    font-size: 13px;

}


/* LOADING BAR */

.loading-bar {

    width: 100%;

    height: 4px;

    margin-top: 18px;

    overflow: hidden;

    border-radius: 20px;

    background: rgba(255,255,255,0.08);

}


.loading-progress {

    width: 40%;

    height: 100%;

    border-radius: 20px;

    background: linear-gradient(
        90deg,
        transparent,
        #ff00cc,
        #ff7bea,
        transparent
    );

    animation: loading 1.4s infinite;

}


/* RESULT */

.result-card {

    margin-top: 35px;

    padding: 30px;

    border-radius: 18px;

    border: 1px solid rgba(255, 0, 204, 0.35);

    background:
        linear-gradient(
            135deg,
            rgba(255, 0, 204, 0.06),
            rgba(255,255,255,0.015)
        );

    box-shadow:
        0 0 35px rgba(255, 0, 204, 0.08);
}


.result-header {

    margin-bottom: 20px;

    color: #ff5be2;

    font-family: 'Orbitron', sans-serif;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 2px;

}


/* FOOTER */

.footer {

    margin-top: 70px;

    padding-top: 20px;

    border-top: 1px solid rgba(255,255,255,0.06);

    text-align: center;

    color: #5f5762;

    font-size: 11px;

    letter-spacing: 1px;
}


/* ANIMATIONS */

@keyframes pulse {

    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }

    50% {
        transform: scale(1.35);
        opacity: 0.65;
    }

}


@keyframes thinkingPulse {

    0%, 100% {
        transform: scale(1);
        filter: drop-shadow(
            0 0 5px rgba(255, 0, 204, 0.4)
        );
    }

    50% {
        transform: scale(1.15);
        filter: drop-shadow(
            0 0 20px rgba(255, 0, 204, 0.8)
        );
    }

}


@keyframes loading {

    0% {
        transform: translateX(-120%);
    }

    100% {
        transform: translateX(300%);
    }

}

</style>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-badge">
        AUTONOMOUS AI RESEARCH AGENT
    </div>

    <div class="hero-title">
        NEXUS <span>AI</span>
    </div>

    <div class="hero-subtitle">
        Search • Reason • Research • Answer
    </div>

</div>
""")


# ============================================================
# STATUS
# ============================================================

st.html("""
<div class="status-card">

    <div class="status-row">

        <div class="status-dot"></div>

        <div>

            <div class="status-main">
                NEURAL CORE ONLINE
            </div>

            <div class="status-sub">
                GPT-3.5 + Tavily Research Engine
            </div>

        </div>

    </div>

</div>
""")


# ============================================================
# CREATE AGENT
# ============================================================

@st.cache_resource
def create_agent():

    search_tool = TavilySearchResults(
        max_results=2,
        tavily_api_key=TAVILY_API_KEY
    )

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=OPENAI_API_KEY
    )

    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(
        llm=llm,
        tools=[search_tool],
        prompt=prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[search_tool],
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    return agent_executor


# ============================================================
# INPUT
# ============================================================

st.html("""
<div class="input-title">
    // ENTER YOUR RESEARCH COMMAND
</div>
""")


user_question = st.text_area(
    "Research command",
    placeholder=(
        "Example:\n"
        "What is the latest iPhone 18 Pro Max price in Sri Lanka?"
    ),
    height=140,
    label_visibility="collapsed"
)


# ============================================================
# BUTTON
# ============================================================

run_agent = st.button(
    "⚡ ACTIVATE AI AGENT",
    use_container_width=True
)


# ============================================================
# RUN AGENT
# ============================================================

if run_agent:

    if not user_question.strip():

        st.warning("⚠️ Please enter a research question first.")

    else:

        # ----------------------------------------------------
        # THINKING UI
        # ----------------------------------------------------

        thinking_placeholder = st.empty()

        thinking_placeholder.html("""
        <div class="thinking-card">

            <div class="thinking-icon">
                🧠
            </div>

            <div class="thinking-title">
                AI AGENT ACTIVATED
            </div>

            <div class="thinking-text">
                Searching the web and analyzing information...
            </div>

            <div class="loading-bar">
                <div class="loading-progress"></div>
            </div>

        </div>
        """)

        try:

            # ------------------------------------------------
            # EXECUTE AGENT
            # ------------------------------------------------

            response = create_agent().invoke(
                {
                    "input": user_question
                }
            )

            # ------------------------------------------------
            # REMOVE THINKING UI
            # ------------------------------------------------

            thinking_placeholder.empty()

            # ------------------------------------------------
            # GET RESULT
            # ------------------------------------------------

            answer = response.get(
                "output",
                "No answer was returned."
            )

            # ------------------------------------------------
            # RESULT HEADER
            # ------------------------------------------------

            st.html("""
            <div class="result-card">

                <div class="result-header">
                    ⚡ NEXUS AI RESPONSE
                </div>

            </div>
            """)

            # ------------------------------------------------
            # DISPLAY ANSWER
            # ------------------------------------------------

            st.markdown(answer)

        except Exception as e:

            thinking_placeholder.empty()

            st.error(
                f"❌ Agent error:\n\n{str(e)}"
            )


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    NEXUS AI • AUTONOMOUS RESEARCH ENGINE
    <br>
    GPT + TAVILY • BUILT FOR AI AGENT EXPERIMENTATION

</div>
""")
