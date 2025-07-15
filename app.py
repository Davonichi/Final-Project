import streamlit as st
import requests

# API setup
API_URL = "https://api-inference.huggingface.co/models/Salesforce/codegen-350M-mono"
HF_TOKEN = st.secrets["HF_TOKEN"]

def query(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "❌ Invalid JSON response. The model might still be loading or unavailable."}

# UI
st.set_page_config(page_title="Code Assistant (HF)", page_icon="🤖")
st.title("🤖 Hugging Face Code Assistant")
task = st.radio("Choose task", ["Explain code", "Complete code"])
code = st.text_area("Paste your Python code here", height=200)

if st.button("Submit"):
    with st.spinner("Talking to Hugging Face..."):
        prompt = f"'''Explain the following Python code'''\n{code}" if task == "Explain code" else code

        result = query({
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200}
        })

        if "error" in result:
            st.error(result["error"])
        else:
            output = result[0].get("generated_text", "No response generated.")
            st.success("✅ Response:")
            st.code(output, language="python")
