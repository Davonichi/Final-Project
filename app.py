import streamlit as st
import openai

# Set your API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page config
st.set_page_config(page_title="AI Code Learning Assistant", page_icon="💡")
st.title("💡 AI Code Learning Assistant")

# 🔹 Word wrap fix for long code blocks
st.markdown("""
<style>
  pre code {
    white-space: pre-wrap;
    word-break: break-word;
    overflow-x: auto;
  }
</style>
""", unsafe_allow_html=True)

st.caption("Supports Python, JavaScript, Java, HTML, C++, SQL, and more")

# Supported languages
languages = [
    "Python", "JavaScript", "Java", "C++", "HTML", "CSS", "SQL", "PHP", "Dart", "R"
]

# Sidebar tabs
tab = st.sidebar.radio("Choose a feature", ["Code Explainer", "Debugging Assistant", "Quiz Generator", "Career Guidance"])

# Language selector
language = st.selectbox("Select your programming language", languages)

# Unified AI query function
def ask_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful coding tutor for beginners."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ OpenAI API Error: {e}"

# Code Explainer
if tab == "Code Explainer":
    st.header("🔍 Explain Your Code")
    code = st.text_area(f"Paste your {language} code below", height=200)
    if st.button("Explain"):
        if code.strip():
            prompt = f"Explain this {language} code to a beginner:\n{code}"
            explanation = ask_openai(prompt)
            st.success("AI Explanation:")
            st.code(explanation)
        else:
            st.warning("Please paste some code.")

# Debugging Assistant
elif tab == "Debugging Assistant":
    st.header("🔎 Debug Your Code")
    code = st.text_area(f"Paste your buggy {language} code below", height=200)
    if st.button("Fix"):
        if code.strip():
            prompt = f"This {language} code has a bug. Fix it and explain the fix:\n{code}"
            result = ask_openai(prompt)
            st.success("AI Fix + Explanation:")
            st.code(result)
        else:
            st.warning("Please paste code to debug.")

# Quiz Generator
elif tab == "Quiz Generator":
    st.header("📄 Generate a Quiz")
    topic = st.text_input(f"Enter a topic in {language} (e.g. functions, loops)")
    if st.button("Generate Quiz"):
        if topic.strip():
            prompt = f"Create a 3-question multiple choice quiz with answers on the topic '{topic}' in {language}."
            quiz = ask_openai(prompt)
            st.success("Quiz:")
            st.markdown(quiz)
        else:
            st.warning("Please enter a topic.")

# Career Guidance
elif tab == "Career Guidance":
    st.header("🎓 Career Learning Paths")
    role = st.text_input("What coding career are you interested in? (e.g. Web Developer, Data Scientist)")
    if st.button("Get Learning Path"):
        if role.strip():
            prompt = f"Give me a step-by-step learning roadmap to become a {role}. Include tools and resources."
            roadmap = ask_openai(prompt)
            st.success(f"Learning Path for {role}:")
            st.markdown(roadmap)
        else:
            st.warning("Please enter a role.")
