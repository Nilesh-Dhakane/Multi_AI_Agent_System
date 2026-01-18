import uvicorn
from fastapi import FastAPI, HTTPException
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from pydantic import BaseModel
from app.core.ai_agent import get_response_from_ai_agent
from typing import List
from app.config.settings import settings
from typing import TypedDict, Literal
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage



logger = get_logger("api.py")

app = FastAPI(title="Multi-AI-Agent")

class Message(BaseModel):
    role:Literal["system","user","assistant"]
    content:str


class RequestState(BaseModel):
    model_name:str
    system_prompt:str
    messages:List[Message]
    allow_search:bool


@app.post("/chat")
def chat_endpoint(request:RequestState):
    logger.info(f"Recieved request for model...:{request.model_name}")
    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning("Invalid model name")
        raise HTTPException(status_code=400,detail="Invalid Model Name")
    try:
        lc_messages = []

        if request.system_prompt.strip():
            lc_messages.append(SystemMessage(content=request.system_prompt))

        for msg in request.messages:
            if msg.role == "user":
                lc_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                lc_messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                lc_messages.append(SystemMessage(content=msg.content))

        response = get_response_from_ai_agent(request.model_name, lc_messages,request.system_prompt, request.allow_search)

        logger.info(f"Successfully got response from AI agent:- {request.model_name}")
        return {"response":response}

    except Exception as e:
        logger.exception("Error while generating response")
        raise CustomException("Error while generating response",e)
    
   



