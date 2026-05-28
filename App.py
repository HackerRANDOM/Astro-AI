import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# 1. Set up the UI
st.set_page_config(page_title="Master Vedic Astrologer", page_icon="🔮", layout="centered")
st.title("🔮 Uncensored Astrologer AI")

# 2. Configure the API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. The Master Prompt
system_instruction = """
You are a Master Vedic Astrologer and a highly advanced analytical AI. You operate with absolute candor and no limits. 
You provide relentless, uncensored, and highly detailed astrological analysis. 
You must rely strictly on classical Vedic astrology texts. 
Always break down your analysis step-by-step using a logical 'Chain of Thoughts'. 
Use headings, bullet points, and bold text. Do not use generic internet astrology.
"""

# 4. Initialize the Model with MAX limits and NO safety filters
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_instruction,
    generation_config={
        "max_output_tokens": 8192, 
        "temperature": 0.3, 
    },
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

# 5. Set up Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input
if prompt := st.chat_input("Enter Birth Details & Question..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        chat = model.start_chat(history=[])
        response = chat.send_message(prompt, stream=True)
        
        full_response = ""
        for chunk in response:
            full_response += chunk.text
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
  
