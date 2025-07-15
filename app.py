import streamlit as st
import requests
import os

# Use Hugging Face token stored in Streamlit Secrets
API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
HF_TOKEN = st.secrets["HF_TOKEN"]

def query(payload):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.title("💻 Hugging Face Code Assistant (StarCoder)")
task = st.selectbox("Task", ["Explain code", "Complete code"])
code = st.text_area("Paste your code here")

if st.button("Submit"):
    with st.spinner("Calling StarCoder..."):
        if task == "Explain code":
            prompt = f"\"\"\"\nExplain what the following Python code does:\n{code}\n\"\"\"\n"
        else:
            prompt = code  # Just let the model continue it

        result = query({
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200}
        })

        if "error" in result:
            st.error(f"❌ API Error: {result['error']}")
        else:
            output = result[0]["generated_text"]
            st.success("✅ Response:")
            st.code(output, language="python")
