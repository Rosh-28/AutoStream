# from google import genai
# from google.genai import types
from langchain_community.llms import Ollama
from typing import TypedDict, List
from langgraph.graph import StateGraph
from langchain.schema import HumanMessage, AIMessage 
from rag_retrieval import load_rag
from lead import mock_lead_capture
import os, json
# from dotenv import load_dotenv
# load_dotenv()

INTENT_PROMPT = """
You are an AI sales agent for AutoStream.

You must:
1. Detect intent: casual, product, or high_intent
2. If product then answer ONLY using the knowledge base
3. If high_intent (when user shows intent like subscribe, signup, try, etc) then ask for missing lead info (NAME, EMAIL, PLATFORM - platform is where they create content, e.g., YouTube, Instagram)
4. If casual then reply normally like hello, how are you, etc.

Return STRICT JSON:
{
  "intent": "...",
  "response": "..."
}
"""

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
llm = Ollama(model="llama3")

# Define the agent state
class AgentState(TypedDict):
    chat_history: List
    intent: str
    email: str
    name: str
    platform: str

retriever = load_rag()

# Define graph nodes
def classify_node(state: AgentState) -> AgentState:
    return state

def answer_node(state: AgentState) -> AgentState:
    question = state["chat_history"][-1].content
    documents = retriever.get_relevant_documents(question)
    context = "\n".join([d.page_content for d in documents])

    prompt = f"""
    {INTENT_PROMPT}

    Knowledge Base:
    {context}

    User message:
    {question}

    Current state:
    Name: {state['name']}
    Email: {state['email']}
    Platform: {state['platform']}
    """

    # Use gemini API
    # response = client.models.generate_content(
    #     model="models/gemini-1.5-flash",
    #     contents=prompt,
    #     config=types.GenerateContentConfig(temperature=0)
    # )
    response_text = llm.invoke(prompt)

    try:
        data = json.loads(response_text)
        state["intent"] = data["intent"]
        state["chat_history"].append(AIMessage(content=data["response"]))
    except Exception as e:
        state["chat_history"].append(AIMessage(content="Sorry, I had trouble understanding."))

    return state

def lead_node(state: AgentState) -> AgentState:
    if not state.get("name"):
        state["chat_history"].append(AIMessage(content="Can I have your name?"))
        return state
    if not state.get("email"):
        state["chat_history"].append(AIMessage(content="Can I have your email?"))
        return state
    if not state.get("platform"):
        state["chat_history"].append(AIMessage(content="Which platform do you create content on?"))
        return state
    
    mock_lead_capture(state["name"], state["email"], state["platform"])
    state["chat_history"].append(AIMessage(content="Thank you! Your interest has been noted."))
    return state

def router(state: AgentState) -> str:
    if state["intent"] == "high_intent":
        return "lead_capture"
    return "product_answer"

def casual_node(state):
    return state

graph = StateGraph(AgentState)

graph.add_node("classify_intent", classify_node)
graph.add_node("product_answer", answer_node)
graph.add_node("lead_capture", lead_node)
graph.set_entry_point("classify_intent")
graph.add_conditional_edges("classify_intent", router,
                            {
                                "product_answer":"product_answer",
                                "lead_capture":"lead_capture",
                            },)

# graph.add_edge("product_answer", "classify_intent")
# graph.add_edge("lead_capture", "classify_intent")

app = graph.compile()

# from IPython.display import display, Image
# png_bytes = app.get_graph().draw_mermaid_png()

# with open("graph.png", "wb") as f:
#     f.write(png_bytes)

def run_agent(user_input, session_state) -> str:
    if "agent_state" not in session_state or session_state.agent_state is None:
        session_state.agent_state = AgentState(chat_history=[], intent="", email="", name="", platform="")

    last_ai = session_state.agent_state["chat_history"][-1].content if session_state.agent_state["chat_history"] else ""

    if "name" in last_ai.lower():
        session_state.agent_state["name"] = user_input
    elif "email" in last_ai.lower():
        session_state.agent_state["email"] = user_input
    elif "platform" in last_ai.lower():
        session_state.agent_state["platform"] = user_input
    else:
        session_state.agent_state["chat_history"].append(HumanMessage(content=user_input))

    session_state.agent_state = app.invoke(session_state.agent_state)
    if session_state.agent_state and session_state.agent_state["chat_history"]:
        return session_state.agent_state["chat_history"][-1].content
    return ""