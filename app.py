import streamlit as st
import requests
import time

# Use CodeGen 350M Mono from Hugging Face (faster)
API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"
HF_TOKEN = st.secrets["HF_TOKEN"]  # Stored in Streamlit Secrets

def query_model(prompt):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5
        }
    }

    for attempt in range(3):  # Retry up to 3 times
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            time.sleep(5)

    return {"error": "Model is still warming up. Please try again after 60 seconds."}

# Streamlit App UI
st.set_page_config(page_title="Code Assistant", page_icon="🤖")
st.title("🤖 Hugging Face Code Assistant (CodeGen 350M)")

task = st.selectbox("Choose a task", ["Explain code", "Complete code"])
code_input = st.text_area("Paste your Python code here", height=200)

if st.button("Submit"):
    if not code_input.strip():
        st.warning("⚠️ Please paste some code.")
    else:
        with st.spinner("Calling CodeGen..."):
            prompt = f"# Python code explanation:\n{code_input}" if task == "Explain code" else code_input
            result = query_model(prompt)

            if "error" in result:
                st.error(result["error"])
            else:
                output = result[0].get("generated_text", "No output received.")
                st.success("✅ AI Response:")
                st.code(output, language="python")
