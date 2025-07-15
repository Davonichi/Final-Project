import streamlit as st
import requests

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/bigcode/santacoder"
HF_TOKEN = st.secrets["HF_TOKEN"]  # Secure token from Streamlit secrets

import streamlit as st
import requests
import time

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/bigcode/santacoder"
HF_TOKEN = st.secrets["HF_TOKEN"]

def query(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.5}
    }
    
    # Try up to 3 times with delays
    for attempt in range(3):
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            time.sleep(5)  # wait before retrying
    return {"error": "Model is still loading or unavailable — please wait a bit and try again."}


# Streamlit UI
st.set_page_config(page_title="Code Assistant", page_icon="🤖")
st.title("🤖 Hugging Face Code Assistant (Santacoder)")

task = st.selectbox("Choose a task:", ["Explain code", "Complete code"])
code_input = st.text_area("Paste your Python code below 👇", height=200)

if st.button("Submit"):
    if not code_input.strip():
        st.warning("⚠️ Please paste some code first.")
    else:
        with st.spinner("Asking Santacoder..."):
            if task == "Explain code":
                prompt = f"# Python code explanation:\n{code_input}"
            else:
                prompt = code_input  # continue code

            result = query(prompt)

            if "error" in result:
                st.error(result["error"])
            if "error" in result:
                st.error(result["error"])
            else:
                generated = result[0].get("generated_text", "No output received.")
                st.code(generated, language="python")
