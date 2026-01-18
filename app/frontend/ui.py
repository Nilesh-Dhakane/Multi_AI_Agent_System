import streamlit as st
import requests
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger("ui.py")


st.set_page_config(page_title="Multi-AI-Agent",layout="centered")
st.title("Multi AI Agent USing Groq and Tavily")
system_prompt = st.text_area("Define your AI Agent:=", height=70)
model_name = st.selectbox("Select you AI Model:",settings.ALLOWED_MODEL_NAMES)
allow_search = st.checkbox("Select fo Web Search using Tavily:-")
user_query = st.text_area("Enter you Query",height=150)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
        "model_name" : model_name,
        "system_prompt" : system_prompt,
        "messages" : [{"role":"user","content":user_query}],
        "allow_search" : allow_search
    }

    try: 
        logger.info("Sending request to backend")
        response = requests.post(url=API_URL,json=payload)
        if response.status_code == 200:
            agent_response = response.json().get("response","")
            logger.info("successfully recieved response from backend.")
            #st.subheader(agent_response)
            st.markdown(agent_response.replace("\n","<br>"),unsafe_allow_html=True)
        else:
            logger.exception("backend error")
            st.error("Error with backend")
    except Exception as e:
        logger.exception("Error occured while sending request to backend")
        raise CustomException("Error while sending request to backend",e)



