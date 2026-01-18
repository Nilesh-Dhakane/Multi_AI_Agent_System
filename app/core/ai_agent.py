from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langchain_community.tools.tavily_search.tool import TavilySearchResults
#from langgraph.prebuilt import create_react_agent     is deprecated
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger("ai_agent.py")


def get_response_from_ai_agent(model_name,messages,system_prompt,allow_search=False):

    llm = ChatGroq(model=model_name,temperature=0.2)
    tools = [TavilySearchResults(max_results=2) if allow_search else []]
    
    messages.append({"role":"system","content":system_prompt})
    if allow_search is False:
        response = llm.invoke(messages)
        return response.content
    else:
        agent = create_agent( 
                                tools=tools,
                                model= llm,
                                )
    
        state = {"messages": messages}
        response = agent.invoke(state)
        result = response.get("messages")
        ai_messages = [ message for message in result if isinstance(message, AIMessage)]
        return ai_messages[-1].content