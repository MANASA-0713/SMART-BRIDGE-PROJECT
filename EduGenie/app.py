import streamlit as st
import requests
from pathlib import Path

# 1. Page Configuration
st.set_page_config(
    page_title="EduGenie | AI Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BACKEND_URL = "http://127.0.0.1:8000"

# 2. Load external stylesheet
def load_css(path: str):
    css_path = Path(path)
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

load_css("static/style.css")

# 3. Session state Initialization
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "generated_quiz" not in st.session_state:
    st.session_state.generated_quiz = None

# Page navigation callback handler
def switch_to_page(page_name):
    st.session_state.current_page = page_name

FEATURES = [
    {"icon": "💬", "title": "Q&A System", "page": "Q&A System", "key": "card_qa",
     "desc": "Get immediate, accurate answers to your academic questions."},
    {"icon": "📝", "title": "Quiz Generator", "page": "Quiz Generator", "key": "card_quiz",
     "desc": "Test your knowledge with auto-generated multiple-choice quizzes."},
    {"icon": "💡", "title": "Concept Explainer", "page": "Concept Explainer", "key": "card_explain",
     "desc": "Simplified, student-friendly explanations on demand."},
    {"icon": "🗺️", "title": "Learning Path", "page": "Learning Path", "key": "card_path",
     "desc": "Build a structured, step-by-step roadmap for any subject."},
    {"icon": "⏳", "title": "Text Summarizer", "page": "Summarizer", "key": "card_summary",
     "desc": "Extract the core ideas from lengthy readings instantly."},
]

# 4. Shared UI components
def render_topbar():
    st.markdown("""
    <div class="topbar">
        <div class="topbar-brand"> EduGenie <span class="badge">AI</span></div>
    </div>
    """, unsafe_allow_html=True)

def render_page_header(eyebrow: str, title: str, desc: str):
    col_head, col_back = st.columns([8, 2])
    with col_head:
        st.markdown(f"""
        <div class="page-eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-desc">{desc}</div>
        """, unsafe_allow_html=True)
    with col_back:
        st.write("")
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        st.button(
            "⬅️ Dashboard", 
            key="global_home_btn", 
            on_click=switch_to_page, 
            args=("Dashboard",)
        )
        st.markdown('</div>', unsafe_allow_html=True)

def result_card(content: str):
    st.markdown(f'<div class="result-card">{content}</div>', unsafe_allow_html=True)

def render_feature_card(feature: dict):
    """Renders a styled card with a standard Streamlit button positioned 
    directly underneath, styled cleanly to avoid breaking layouts."""
    
    # 1. Render the beautiful visual card
    st.markdown(f'''
    <div class="feature-card">
        <div class="fc-head">
            <span class="fc-icon">{feature["icon"]}</span>
            <span class="fc-title">{feature["title"]}</span>
        </div>
        <p class="fc-desc">{feature["desc"]}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # 2. Render an explicit action button wrapper
    st.markdown('<div class="card-action-btn">', unsafe_allow_html=True)
    clicked = st.button(f"Open {feature['title']}", key=f'{feature["key"]}_btn')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 3. Handle page routing
    if clicked:
        st.session_state.current_page = feature["page"]
        st.rerun()

render_topbar()

# 5. Main Router / Page Engine
if st.session_state.current_page == "Dashboard":
    st.markdown('<div class="hero-title">Welcome back 👋</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Your AI-powered study companion — ask questions, '
        'get explanations, summarize readings, and build a learning roadmap.</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="section-title">Available Modules</div>', unsafe_allow_html=True)
    
    row1 = st.columns(2, gap="medium")
    row2 = st.columns(2, gap="medium")
    row3 = st.columns(2, gap="medium")
    
    with row1[0]: render_feature_card(FEATURES[0]) # Q&A System
    with row1[1]: render_feature_card(FEATURES[1]) # Quiz Generator
    with row2[0]: render_feature_card(FEATURES[2]) # Concept Explainer
    with row2[1]: render_feature_card(FEATURES[3]) # Learning Path
    with row3[0]: render_feature_card(FEATURES[4]) # Text Summarizer
    
    st.markdown(
        '<div class="app-footer">EduGenie · Powered by Gemini 2.5 Flash &amp; LaMini-Flan-T5</div>',
        unsafe_allow_html=True
    )

# ---------------- Q&A System ----------------
elif st.session_state.current_page == "Q&A System":
    render_page_header("Module", "Q&A Academic System", "Powered by Gemini 2.5 Flash")
    question = st.text_input("Your question", placeholder="Ask anything academic...", label_visibility="collapsed")
    
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    ask_clicked = st.button("Ask Gemini")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if ask_clicked:
        if question.strip():
            with st.spinner("Gemini is thinking..."):
                try:
                    response = requests.get(f"{BACKEND_URL}/qa", params={"question": question})
                    if response.status_code == 200:
                        result_card(response.json().get("answer"))
                    else:
                        st.error("Backend error.")
                except Exception as e:
                    st.error(f"Error connecting: {e}")
        else:
            st.warning("Please type a question first.")

# ---------------- Concept Explainer ----------------
elif st.session_state.current_page == "Concept Explainer":
    render_page_header("Module", "Concept Explainer", "Running locally via LaMini-Flan-T5")
    topic = st.text_input("Topic", placeholder="e.g., Photosynthesis", label_visibility="collapsed")
    
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    explain_clicked = st.button("Explain Topic")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if explain_clicked:
        if topic.strip():
            with st.spinner("LaMini is processing..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/explain", json={"topic": topic})
                    if response.status_code == 200:
                        result_card(response.json().get("explanation"))
                    else:
                        st.error("Error communicating with backend.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a topic.")

# ---------------- Summarizer ----------------
elif st.session_state.current_page == "Summarizer":
    render_page_header("Module", "Text Summarizer", "Condense long readings into key points")
    text = st.text_area("Reading material", height=220, label_visibility="collapsed", placeholder="Paste your reading material here...")
    
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    summarize_clicked = st.button("Summarize Text")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if summarize_clicked:
        if text.strip():
            with st.spinner("Summarizing..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/summarize", json={"text": text})
                    if response.status_code == 200:
                        result_card(response.json().get("summary"))
                    else:
                        st.error("Backend error.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter some text.")

# ---------------- Quiz Generator ----------------
elif st.session_state.current_page == "Quiz Generator":
    render_page_header("Module", "Interactive Quiz Generator", "Auto-generated multiple-choice questions")
    
    quiz_text = st.text_area("Study context", height=200, label_visibility="collapsed",
                             placeholder="Paste study context to generate a quiz...")
    
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    quiz_clicked = st.button("Generate Quiz")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 1. Trigger the API request when button is clicked and save it to memory
    if quiz_clicked:
        if quiz_text.strip():
            with st.spinner("Creating your quiz..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/quiz", json={"text": quiz_text})
                    if response.status_code == 200:
                        st.session_state.generated_quiz = response.json().get("quiz")
                    else:
                        st.error("Backend error.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please paste some study context first.")
            
            # 2. Render the quiz outside of the button trigger using session memory
    if st.session_state.generated_quiz is not None:
        quiz_data = st.session_state.generated_quiz
        if isinstance(quiz_data, list):
            st.write("")
            for idx, q in enumerate(quiz_data):
                with st.container(border=True):
                    st.markdown(f"**Q{idx+1}. {q.get('question')}**")
                    options = q.get("options", [])
                    
                    # Setting index=None keeps the options unselected until the user clicks one
                    user_choice = st.radio(
                        f"Select your answer for Q{idx+1}:", 
                        options,
                        key=f"quiz_radio_{idx}", 
                        label_visibility="collapsed",
                        index=None
                    )
                    
                    # --- Real-Time Feedback Logic ---
                    if user_choice is not None:
                        correct_answer = q.get("answer")
                        
                        if user_choice == correct_answer:
                            st.success("🎉 **Correct! Brilliant!**")
                        else:
                            st.error("❌ **Incorrect! Try another option.**")
                            
                    # Optional: We can still keep the reveal drawer if they get stuck!
                    with st.expander("Stuck? Reveal Answer"):
                        st.write(f"The correct answer is: **{q.get('answer')}**")
        else:
            st.error("Could not parse quiz response.")

# ---------------- Learning Path ----------------
elif st.session_state.current_page == "Learning Path":
    render_page_header("Module", "Personalized Learning Path", "Structured roadmap for any subject")
    lp_topic = st.text_input("Subject", placeholder="What subject do you want a timeline for?", label_visibility="collapsed")
    
    st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
    path_clicked = st.button("Build Roadmap")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if path_clicked:
        if lp_topic.strip():
            with st.spinner("Crafting your roadmap..."):
                try:
                    response = requests.get(f"{BACKEND_URL}/learn/recommendations", params={"topic": lp_topic})
                    if response.status_code == 200:
                        result_card(response.json().get("recommendation"))
                    else:
                        st.error("Backend error.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter a subject.")