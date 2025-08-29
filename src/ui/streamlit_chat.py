import streamlit as st
from typing import Dict, List
from src.core.persona import Persona
from src.core.llm import stream_chat

INTRO_TMPL = "My name is {user_name} and you can ask me any career related questions."

def init_state():
    if "history" not in st.session_state:
        st.session_state.history: List[Dict[str, str]] = []
    if "persona" not in st.session_state:
        st.session_state.persona = Persona()
    if "configured" not in st.session_state:
        st.session_state.configured = False

def sidebar():
    st.sidebar.header("Profile Setup")
    uploaded = st.sidebar.file_uploader(
        "Upload your resume (PDF only)*",
        type=["pdf"],
        accept_multiple_files=False,
    )
    name = st.sidebar.text_input("Your full name *", value=st.session_state.persona.name or "")
    extra = st.sidebar.text_area(
        "Additional information",
        value=st.session_state.persona.extra_info or "",
        placeholder="e.g., Contact details, portfolio link, hobbies, notable achievements..."
    )
    apply = st.sidebar.button("Apply / Update Profile", use_container_width=True)

    if apply:
        pdf_bytes = uploaded.read() if uploaded is not None else None
        st.session_state.persona = Persona(name=name.strip(), resume_bytes=pdf_bytes, extra_info=extra)
        st.session_state.configured = bool(name.strip())
        # Reset chat with first assistant message
        st.session_state.history = []
        if st.session_state.configured:
            first = INTRO_TMPL.format(user_name=name.strip())
            st.session_state.history.append({"role": "assistant", "content": first})
        else:
            st.session_state.history.append({
                "role": "assistant",
                "content": "Please enter your name in the sidebar to begin."
            })

def header():
    st.markdown(
        """
        # 🤖 Resume Agent
        Configure the profile in the sidebar, then chat below.
        """.strip()
    )
    st.divider()

def draw_chat():
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_input():
    disabled = not st.session_state.configured
    prompt = st.chat_input(
        "Ask about career, skills, projects, or background…",
        disabled=disabled
    )
    if not prompt:
        return

    # Show user's message immediately this run
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add to history
    st.session_state.history.append({"role": "user", "content": prompt})

    # Build system prompt
    persona = st.session_state.persona
    system_prompt = persona.system_prompt()

    # Stream assistant reply inline (don’t add to history yet)
    with st.chat_message("assistant"):
        stream = stream_chat(system_prompt, st.session_state.history[:-1], prompt)
        full = st.write_stream(stream) or ""   # safety: ensure string

    # Append final assistant reply to history (so it shows next rerun)
    if full.strip():
        st.session_state.history.append({"role": "assistant", "content": full})
    else:
        st.session_state.history.append({
            "role": "assistant",
            "content": "_(Encountered an issue streaming a reply. Please try again.)_"
        })


def render_page():
    st.set_page_config(page_title="Generic Career Agent", page_icon="🤖", layout="centered")
    init_state()
    sidebar()
    header()
    draw_chat()

    if not st.session_state.configured:
        st.info("Set your **name** (and optionally upload a PDF resume) in the sidebar, then click **Apply / Update Profile**.")
    handle_input()
