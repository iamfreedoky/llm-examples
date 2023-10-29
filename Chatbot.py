import streamlit as st
import requests

# Hugging Face API tokens
HUGGING_FACE_READ_TOKEN = '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'
HUGGING_FACE_WRITE_TOKEN = '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'

with st.sidebar:
    st.text("Hugging Face API Tokens (Read and Write)")

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by Hugging Face's GPT-2 LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.text_input("You:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Make an API request to Hugging Face for text generation
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_WRITE_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "inputs": prompt,
        "max_length": 100,  # Adjust the maximum response length as needed
        "num_return_sequences": 1,
        "no_repeat_ngram_size": 2,
        "top_k": 50,
    }

    api_url = "https://api-inference.huggingface.co/models/gpt2"
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        msg_content = response.json()[0]["generated_text"]
        st.session_state.messages.append({"role": "assistant", "content": msg_content})
        st.chat_message("assistant").write(msg_content)
