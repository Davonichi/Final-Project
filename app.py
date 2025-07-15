import streamlit as st
import requests

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/bigcode/santacoder"
HF_TOKEN = st.secrets["HF_TOKEN"]  # Secure token from Streamlit secrets

def query(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.5
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "❌ Model returned invalid response. Please wait and try again."}

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
            else:
                generated = result[0].get("generated_text", "No response received.")
                st.success("✅ AI Response:")
                st.code(generated, language="python")
