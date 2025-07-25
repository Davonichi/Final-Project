# --- ENVIRONMENT PATCH FOR STREAMLIT ---
import os
os.environ["STREAMLIT_WATCH_USE_POLLING"] = "true"

# --- MAIN IMPORTS ---
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Code Learning Assistant", layout="wide")

# --- DARK MODE TOGGLE ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.title("🌓 Theme")
st.session_state.dark_mode = st.sidebar.checkbox("Enable Dark Mode", value=st.session_state.dark_mode)

if st.session_state.dark_mode:
    st.markdown("""
        <style>
        body {
            background-color: #0e1117;
            color: #FAFAFA;
        }
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            background-color: #262730;
            color: #FAFAFA;
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("AI Code Tutor")
st.markdown("Helping African learners unlock coding skills with AI ✨")

# --- SIDEBAR NAV ---
st.sidebar.title("Features")
feature = st.sidebar.radio("Choose a feature:", [
    "Code Explainer",
    "Debugging Assistant",
    "Mini Lessons",
    "Quiz Generator",
    "Career Guide"
])

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
    model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype=torch.float32)
    return tokenizer, model

tokenizer, model = load_model()

def chat_with_model(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- FEATURE LOGIC ---
if feature == "Code Explainer":
    st.subheader("Explain Code")
    code = st.text_area("Paste your code here")
    if st.button("Explain") and code:
        with st.spinner("Explaining code..."):
            result = chat_with_model(f"Explain this code in simple terms:\n{code}")
            st.success("Done!")
            st.markdown(result)

elif feature == "Debugging Assistant":
    st.subheader("Debug My Code")
    bug_code = st.text_area("Paste your buggy code")
    if st.button("Find and Fix Bugs") and bug_code:
        with st.spinner("Analyzing code for bugs..."):
            result = chat_with_model(f"Find and fix bugs in this code:\n{bug_code}")
            st.success("Bugfix suggestions ready!")
            st.markdown(result)

elif feature == "Mini Lessons":
    st.subheader("On-Demand Mini Lessons")
    topic = st.text_input("Ask a coding topic (e.g., Python loops, Git basics)")
    if st.button("Teach Me") and topic:
        with st.spinner("Fetching lesson..."):
            result = chat_with_model(f"Teach me about: {topic}")
            st.success("Here's your lesson")
            st.markdown(result)

elif feature == "Quiz Generator":
    st.subheader("Generate a Quiz")
    quiz_topic = st.text_input("Enter a coding topic for a quiz")
    if st.button("Generate Quiz") and quiz_topic:
        with st.spinner("Creating quiz..."):
            result = chat_with_model(f"Create a short 3-question multiple choice quiz on: {quiz_topic}")
            st.success("Quiz ready!")
            st.markdown(result)

elif feature == "Career Guide":
    st.subheader("Ask for Career Advice")
    career_question = st.text_input("Ask anything about your software career path")
    if st.button("Advise Me") and career_question:
        with st.spinner("Getting advice..."):
            result = chat_with_model(f"Give career advice: {career_question}")
            st.success("Here’s some advice:")
            st.markdown(result)

# --- FOOTER ---
st.markdown("---")
st.markdown("Empowering Next Generation of Developers in Africa 🌍 | © 2025 CodeTutor")
