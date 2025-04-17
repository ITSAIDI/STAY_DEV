from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
import json
from langchain_core.messages import ToolMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import GoogleSerperAPIWrapper

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

############################### Define the tools ( Tavily and Serper)

os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_API_KEY')
Tavily = TavilySearchResults(max_results=3)
Serper = GoogleSerperAPIWrapper(k=3,gl='fr',hl='fr',serper_api_key=os.getenv('SERPER_API_KEY'))
tools = [Tavily]

def Get_AIMessage(state:State):
    messages = state.get("messages", []) 
    if messages:
        message = messages[-1]
    return message

def searchFunction(state:State):
    message = Get_AIMessage(state)
    Tavily_call = message.tool_calls[0]
    tool_arguments = Tavily_call["args"]
    
    print("\n ⚙️ Web search is Executing...")
    
    Tavily_result = Tavily.invoke(tool_arguments)
    Serper_result = Serper.run(tool_arguments['query'])
    
    Tavily_Message =  ToolMessage(content=json.dumps(Tavily_result),name=Tavily_call["name"],tool_call_id=Tavily_call["id"])
    Serper_Message =  ToolMessage(content=Serper_result,name=Tavily_call["name"],tool_call_id=Tavily_call["id"])
    
    return {"messages": [Tavily_Message,Serper_Message]}

############################### Define the llm

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",api_key=os.getenv('GEMINI_API_KEY'))
llm_with_tools = llm.bind_tools(tools)

def Llm_Function(state: State):
    print("\n💡 LLM is Thinking !")
    
    prompt = state["messages"]
    response = llm_with_tools.invoke(prompt)
    return {"messages": response}

############################### Build the graph

graph_builder.add_node("LLM", Llm_Function)
graph_builder.add_node("Tavily", searchFunction)


def Ask_for_Tavily(tool_calls:list):
    for tool_call in tool_calls:
        if tool_call['name'] == "tavily_search_results_json":
            return True
    return False

def Condition_Function(state: State):
    """
    Use in the conditional_edge to route to the ToolsNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    messages = state.get("messages", [])
    
    if isinstance(state, list):
        ai_message = state[-1]
        
    elif messages : # check that messages is not an empty list
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0: # Check if the LLM ask for a tool
        
        if Ask_for_Tavily(ai_message.tool_calls):
            return "Ask for Tavily"
    return "Ask for END"


graph_builder.add_conditional_edges("LLM",Condition_Function,{"Ask for Tavily": "Tavily", "Ask for END": "__end__"},)
graph_builder.add_edge("Tavily", "LLM")
graph_builder.add_edge(START, "LLM")
WebSerchAgent = graph_builder.compile()

def visualize():
    with open("graph.png", "wb") as f:
        f.write(WebSerchAgent.get_graph().draw_mermaid_png())

import re

def clean_json_string(s):
    # Supprime les blocs markdown ```json ... ```
    s = s.strip()
    s = re.sub(r"^```json\s*", "", s)
    s = re.sub(r"\s*```$", "", s)
    return s


def main(context):
    system_prompt = """
        Voici la biographie d'une chaîne YouTube, accompagnée de quelques descriptions et titres de vidéos. Votre tâche est d’extraire le pays d’origine de la chaîne (par exemple : France, USA, etc.).

        - Votre réponse doit être au format dictionnaire python avec deux clés : "pays" et "justification". 
        - Si le pays ne peut pas être déterminé avec certitude, insérez "inconnu" dans le champ "pays" et laissez "justification" vide.
        - Vous avez accès à un moteur de recherche. Utilisez-le si vous avez besoin de rechercher des informations supplémentaires sur Internet.
    """
   
    result = WebSerchAgent.invoke({"messages": [("user", context), ("user", system_prompt)]})
    
    json_str = result.get("messages")[-1].content
    cleaned = clean_json_string(json_str)
    data = json.loads(cleaned)
    print(data["pays"]) 
    print(data["justification"]) 

        




