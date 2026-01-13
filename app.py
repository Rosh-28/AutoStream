import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AutoStream AI Agent", layout="centered")
st.title("🎬 AutoStream AI Agent")

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []

if "agent_state" not in st.session_state:
    st.session_state.agent_state = None

# Chat input
user_input = st.chat_input("Ask about AutoStream...")

if user_input:
    st.session_state.chat.append(("user", user_input))

    # Run LangGraph agent
    response = run_agent(user_input, st.session_state)

    st.session_state.chat.append(("agent", response))

# Render chat
for role, msg in st.session_state.chat:
    st.chat_message(role).write(msg)
