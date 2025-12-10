import streamlit as st
import requests
import json

st.title("🎓 Tutor Inteligente de Algoritmos")

prompt = st.chat_input("Pregunta sobre algoritmos...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    # Llamada a tu API local de Ollama
    res = requests.post('http://localhost:11434/api/generate', 
        json={"model": "tutor_v0", "prompt": prompt, "stream": False})
    
    response_text = json.loads(res.text)['response']
    
    with st.chat_message("assistant"):
        st.write(response_text)
