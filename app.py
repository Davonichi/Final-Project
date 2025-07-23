import streamlit as st
import requests

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
tab = st.sidebar.radio("Choose a feature", [
    "Code Explainer",
    "Debugging Assistant",
    "Quiz Generator",
    "Career Guidance",
    "Mini Lessons"
])

# Language selector
language = st.selectbox("Select your programming language", languages)

# Deepseek API function
def ask_deepseek(prompt):
    try:
        # Deepseek API endpoint (replace with actual endpoint if different)
        url = "https://api.deepseek.com/v1/chat/completions"
        
        # Your Deepseek API key from Streamlit secrets
        headers = {
            "Authorization": f"Bearer {st.secrets['sk-b8d553064b1843a3b90888d5c74f7e5d']}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",  # or the specific model you want to use
            "messages": [
                {"role": "system", "content": "You are a helpful coding tutor for beginners."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.5,
            "max_tokens": 2000  # Deepseek typically allows more tokens
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Code Explainer
if tab == "Code Explainer":
    st.header("🔍 Explain Your Code")
    code = st.text_area(f"Paste your {language} code below", height=200)
    if st.button("Explain"):
        if code.strip():
            with st.spinner("Generating explanation..."):
                prompt = f"Explain this {language} code to a beginner:\n{code}"
                explanation = ask_deepseek(prompt)
                st.success("AI Explanation:")
                st.markdown(explanation)
        else:
            st.warning("Please paste some code.")

# Debugging Assistant
elif tab == "Debugging Assistant":
    st.header("🔎 Debug Your Code")
    code = st.text_area(f"Paste your buggy {language} code below", height=200)
    if st.button("Fix"):
        if code.strip():
            with st.spinner("Analyzing and fixing..."):
                prompt = f"This {language} code has a bug. Fix it and explain the fix:\n{code}"
                result = ask_deepseek(prompt)
                st.success("AI Fix + Explanation:")
                st.markdown(result)
        else:
            st.warning("Please paste code to debug.")

# Quiz Generator
elif tab == "Quiz Generator":
    st.header("📄 Generate a Quiz")
    topic = st.text_input(f"Enter a topic in {language} (e.g. functions, loops)")
    if st.button("Generate Quiz"):
        if topic.strip():
            with st.spinner("Creating quiz..."):
                prompt = f"Create a 3-question multiple choice quiz with answers on the topic '{topic}' in {language}."
                quiz = ask_deepseek(prompt)
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
            with st.spinner("Generating roadmap..."):
                prompt = f"Give me a step-by-step learning roadmap to become a {role}. Include tools and resources."
                roadmap = ask_deepseek(prompt)
                st.success(f"Learning Path for {role}:")
                st.markdown(roadmap)
        else:
            st.warning("Please enter a role.")

# Mini Lessons
elif tab == "Mini Lessons":
    st.header("📚 Mini Lessons")
    st.caption("Learn quick concepts in Python, HTML, SQL, JavaScript, C++, and more!")

    lesson_language = st.selectbox("Choose a language", languages)
    lesson_topic = st.text_input("What concept or topic do you want to learn about?")
    
    if st.button("Teach Me"):
        if lesson_topic.strip():
            with st.spinner("Preparing lesson..."):
                prompt = f"Give a short, beginner-friendly explanation (in 3-5 sentences) about '{lesson_topic}' in {lesson_language}."
                lesson = ask_deepseek(prompt)
                st.success("🧠 Micro Lesson:")
                st.markdown(lesson)
        else:
            st.warning("Please enter a topic.")
