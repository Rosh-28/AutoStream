# 🚀 AutoStream

AutoStream is a **conversational AI agent** designed to qualify leads, answer pricing questions using RAG, and guide users toward subscription intent through a structured, agentic workflow.

---

## 🖥️ How to Run the Project Locally

Follow the steps below to run the **AutoStream Conversational AI Agent** on your local machine.

---

## ✅ Prerequisites

Make sure you have the following installed:

- **Python 3.9+**
- **Git**
- **Gemini 1.5 Flash** or **Ollama** (for local LLM & embeddings)
- A stable terminal (**VS Code recommended**)

---

# 1️⃣ Clone the Repository

    ```bash
    git clone <your-github-repo-url>
    cd AutoStream
    ```

# 2️⃣ Install Dependencies

    ```bash
    pip install -r requirements.txt
    ```

# 3️⃣ Install & Run Ollama Models
    Make sure Ollama is running, then pull the required models:

    ```bash
    ollama pull llama3
    ollama pull nomic-embed-text
    ```

# 4️⃣ Project Structure:

AutoStream/
├── app.py                 # Streamlit UI
├── agent.py               # LangGraph agent logic
├── rag_retrieval.py       # RAG pipeline (Chroma + embeddings)
├── lead.py                # Lead capture tool (JSON storage)
├── data.md                # Pricing & policy knowledge base
├── leads.json             # Captured leads (auto-created)
├── requirements.txt
└── README.md

# 5️⃣ Run the Application:

    ```bash
    streamlit run app.py
    ```
    The app will open automatically in your browser at:
    http://localhost:8501

# 6️⃣ Demo Flow (What to Test)
    Try the following conversation:

1. Causal geetrings - 
    Hi!, Hello!

2. Ask product pricing -
    What are your plans?

3. Show high intent - 
    I want to try the Pro plan for my content.
    I want to subscribe to your platform.

    Provide details when asked
    Name → Email → Platform
    ✅ Lead will be captured and stored in leads.json


## Architecture Explanation

The AutoStream Conversational AI Agent is built using an agentic architecture that combines stateful decision-making, retrieval-augmented generation (RAG), and controlled tool execution.

# Why LangGraph
LangGraph was chosen because it allows modeling the agent as a state machine rather than a simple chatbot. Each user interaction flows through well-defined nodes such as intent processing, knowledge-based answering, and lead capture. This ensures predictable behavior, prevents premature tool execution, and makes the system easy to extend with additional actions (e.g., CRM integration).

# State Management
The agent maintains a persistent state using LangGraph’s shared state object. The state stores:
1. Conversation history
2. Detected user intent
3. Lead details(name, email, platform)

This enables the agent to retain memory across multiple turns, progressively collect user information, and make decisions based on prior context.

# RAG (Retrieval-Augmented Generation)
Product pricing and policy information is stored locally in a Markdown file and embedded using Ollama’s nomic-embed-text model. These embeddings are stored in ChromaDB for efficient semantic retrieval. When a product-related query is detected, relevant context is retrieved and injected into the LLM prompt, ensuring responses are accurate and grounded in the knowledge base.

# LLM & Tool Execution
The primary large language model used in this system is Gemini 1.5 Flash, which is leveraged for intent detection, conversational reasoning, and response generation. The system can seamlessly switch to a local LLM such as Llama 3 via Ollama without any changes to the agent logic. This allows the agent to continue performing intent detection, RAG-based answering, and lead qualification entirely offline.
Tool execution is strictly gated by the agent’s internal state. The lead capture tool (mock_lead_capture) is invoked only after the agent has successfully collected all required user details (name, email, and creator platform), ensuring safe and non-premature backend actions.

# UI Layer
Streamlit is used to provide an interactive chat-based interface. Each user input triggers a single LangGraph execution cycle, ensuring deterministic behavior and preventing infinite loops.

# LangGraph model 
 (graph.png)


 ## Whatsapp Webhook Integration

To integrate this agent with WhatsApp, I would use the WhatsApp Business API and webhooks.

First, a backend server (using Flask or FastAPI) would expose a webhook URL. This webhook is registered with WhatsApp so that whenever a user sends a message, WhatsApp automatically sends that message to our server.

The server extracts the user’s message and phone number and passes the message to the LangGraph agent. The phone number is used as a unique session ID so the agent can remember the conversation across multiple messages.

The agent then processes the message by detecting intent, retrieving information using RAG, or collecting lead details. Once a response is generated, the backend sends the reply back to the user through the WhatsApp Business API.

This setup allows the same agent logic used in the Streamlit demo to work on WhatsApp with minimal changes.
