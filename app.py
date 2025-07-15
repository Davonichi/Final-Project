import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load your .env file
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"] 

# Set up Streamlit
st.set_page_config(page_title="AI Code Assistant", page_icon="🤖")
st.title("👨‍💻 AI Code Learning Assistant")

user_input = st.text_area("💬 Ask a question or paste code:", height=200)
task_type = st.selectbox("What do you want to do?", ["Explain code", "Fix bug", "Ask a question"])

if st.button("Get Help"):
    with st.spinner("Thinking..."):
        # Build prompt
        if task_type == "Explain code":
            prompt = f"Explain this Python code in simple terms:\n{user_input}"
        elif task_type == "Fix bug":
            prompt = f"Find and fix the bug in this Python code:\n{user_input}"
        else:
            prompt = f"Answer this Python programming question:\n{user_input}"

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=600
            )
            answer = response.choices[0].message.content
            st.success("✅ Here's the AI's response:")
            st.code(answer, language="python" if "```python" in answer else "text")
        except Exception as e:
            st.error(f"❌ Error: {e}")
