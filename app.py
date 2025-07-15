import streamlit as st
import openai

# Set up OpenAI API key securely
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit page config
st.set_page_config(page_title="AI Code Learning Assistant", page_icon="💡")
st.title("💡 AI Code Learning Assistant")
st.caption("Powered by OpenAI | Built for SDG 4: Quality Education")

# Sidebar navigation
tab = st.sidebar.radio("Choose a feature", ["Code Explainer", "Debugging Assistant", "Quiz Generator", "Career Guidance"])

# Unified function to ask OpenAI
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
        return f"⚠️ Error: {e}"

# Tab 1: Code Explainer
if tab == "Code Explainer":
    st.header("🔍 Explain Your Code")
    code = st.text_area("Paste your Python code below", height=200)
    if st.button("Explain"):
        if code.strip():
            prompt = f"Explain what this Python code does:\n{code}"
            explanation = ask_openai(prompt)
            st.success("AI Explanation:")
            st.code(explanation, language="markdown")
        else:
            st.warning("Please enter some code.")

# Tab 2: Debugging Assistant
elif tab == "Debugging Assistant":
    st.header("🐞 Debug Your Code")
    code = st.text_area("Paste your buggy Python code below", height=200)
    if st.button("Fix"):
        if code.strip():
            prompt = f"This Python code has a bug. Fix it and explain the fix:\n{code}"
            result = ask_openai(prompt)
            st.success("AI Fix + Explanation:")
            st.code(result, language="python")
        else:
            st.warning("Please paste code to debug.")

# Tab 3: Quiz Generator
elif tab == "Quiz Generator":
    st.header("📄 Generate a Coding Quiz")
    topic = st.text_input("Enter a coding topic (e.g. 'Python lists')")
    if st.button("Generate Quiz"):
        if topic.strip():
            prompt = f"Create a short quiz (3 questions with answers) for a beginner learning {topic}."
            quiz = ask_openai(prompt)
            st.success("Quiz:")
            st.markdown(quiz)
        else:
            st.warning("Please enter a topic.")

# Tab 4: Career Guidance
elif tab == "Career Guidance":
    st.header("🎓 Career Learning Paths")
    role = st.text_input("What role are you interested in? (e.g. Mobile Developer, Web Developer)")
    if st.button("Get Path"):
        if role.strip():
            prompt = f"Give me a step-by-step learning roadmap to become a {role}. Include tools and online resources."
            roadmap = ask_openai(prompt)
            st.success(f"Learning Path for {role}:")
            st.markdown(roadmap)
        else:
            st.warning("Please enter a role.")
