import streamlit as st
import openai

# Set your API key (stored securely in secrets)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# UI
st.set_page_config(page_title="Code Assistant", page_icon="🤖")
st.title("🤖 OpenAI-Powered Code Assistant")

task = st.selectbox("Choose a task", ["Explain code", "Complete code"])
code_input = st.text_area("Paste your Python code below 👇", height=200)

if st.button("Submit"):
    if not code_input.strip():
        st.warning("⚠️ Please paste some code.")
    else:
        with st.spinner("Asking OpenAI..."):
            # Prompt construction
            if task == "Explain code":
                prompt = f"Explain what the following Python code does:\n{code_input}"
            else:
                prompt = f"Continue this Python code:\n{code_input}"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for code learning."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=300
                )
                result = response['choices'][0]['message']['content']
                st.success("✅ AI Response:")
                st.code(result, language="python")

            except openai.error.OpenAIError as e:
                st.error(f"❌ OpenAI API error: {e}")
