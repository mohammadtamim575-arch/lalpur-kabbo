import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import io

st.set_page_config(page_title="লালপুর কাব্য", layout="wide")

# API Key সেটআপ
genai.configure(api_key="gen-lang-client-0780492464")

st.title("✨ লালপুর কাব্য")
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("আপনার প্রশ্ন বা কবিতা লিখুন..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        full_response = response.text
        st.markdown(full_response)
        
        st.code(full_response, language=None)
        
        if st.button("🔊 শুনতে ক্লিক করুন"):
            tts = gTTS(text=full_response, lang='bn')
            audio_file = io.BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
