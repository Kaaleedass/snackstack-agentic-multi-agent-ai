# 🍔 SnackStack AI — Agentic Multi-Agent Food Ordering Assistant

An AI-powered food ordering assistant built with **Python, LangGraph, Agentic AI, and Retrieval-Augmented Generation (RAG)**. SnackStack uses a multi-agent architecture to understand user requests, retrieve relevant menu information, assist with orders, and provide conversational interactions with optional voice support.

## 🚀 Project Overview

SnackStack AI demonstrates how multiple specialized AI agents can collaborate to handle food ordering tasks through a conversational interface.

Instead of relying on a single AI workflow, the system uses routing and specialized agents to process different types of user requests.

## ✨ Key Features

- 🤖 **Agentic AI:** AI-driven workflows that determine how to handle user requests.
- 🔀 **Multi-Agent Architecture:** Routes requests to specialized agents for menu queries and order assistance.
- 🔎 **RAG-Based Menu Search:** Retrieves relevant product and menu information using semantic search.
- 🧠 **LangGraph Orchestration:** Manages agent workflows, state, and conditional routing.
- 💬 **Conversational Interface:** Interact with the assistant using a chat interface.
- 🎙️ **Voice Interaction:** Supports voice input and spoken responses in supported interfaces.
- 🛠️ **Tool Integration:** Uses tools to retrieve information and support order-related tasks.
- 👤 **Human-in-the-Loop:** Supports human assistance when a request requires clarification or escalation, where implemented.

## 🏗️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| LangGraph | Agent workflow orchestration and state management |
| LangChain | LLM and tool integration |
| Large Language Models (LLMs) | Natural-language understanding and response generation |
| Retrieval-Augmented Generation (RAG) | Context-aware menu and product retrieval |
| Vector Embeddings | Semantic similarity search |
| Flask | Web interface and backend API, where configured |
| HTML, CSS, JavaScript | Chat interface and browser-based voice interaction |
| OpenAI API | Language model, embeddings, and voice-related API integration, where configured |

## 🧩 Architecture

```text
                  User
                   |
                   v
          Chat / Voice Interface
                   |
                   v
             Flask Backend
                   |
                   v
           LangGraph Workflow
                   |
                   v
             Request Router
              /          \
             v            v
       Menu Agent      Order Agent
             |            |
             v            v
       RAG / Search    Order Tools
              \          /
               v        v
           Response Generation
                   |
                   v
            User Response
```

*Note: This is a conceptual overview. The exact workflow depends on the agents and tools implemented in the current codebase.*

## 📁 Project Structure

```text
SnackStack/
├── SnackStack/
│   ├── agents/
│   ├── Tools/
│   ├── Voice/
│   ├── data/
│   ├── config.py
│   ├── graph.py
│   ├── main.py
│   ├── nodes.py
│   ├── rag.py
│   └── state.py
├── templates/
│   └── index.html
├── web.py
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/snackstack-agentic-multi-agent-ai.git
cd snackstack-agentic-multi-agent-ai
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the API keys required by your implementation.

```env
OPENAI_API_KEY=your_openai_api_key
```

Keep API keys private. Never commit your `.env` file or expose secrets in your source code.

### 5. Run the application

**Command-line interface:**

```powershell
python -m SnackStack.main
```

**Web interface:**

```powershell
python web.py
```

Open the local URL displayed in your terminal, if your Flask application prints one.

## 💡 Example Use Cases

- Search for menu items using natural language.
- Ask questions about available food products.
- Request assistance with food orders.
- Route different requests to specialized AI agents.
- Interact with the assistant through chat and supported voice features.

Actual capabilities depend on the tools, data, and integrations enabled in the application.

## 🔐 Security

- Store API keys in environment variables.
- Add `.env`, virtual environments, caches, and local secrets to `.gitignore`.
- Do not upload private customer information or confidential business data.
- Validate tool inputs before executing order-related operations.

## 🎯 Project Goals

This project explores practical applications of:

- Agentic AI and autonomous workflows
- Multi-agent collaboration and orchestration
- LangGraph state management and conditional routing
- Retrieval-Augmented Generation
- Tool calling and conversational AI
- Voice-enabled AI applications

## 👨‍💻 Author

**Kaaleedass Manoharan**

AI Engineering | Python Automation | Agentic AI | Multi-Agent Systems | RAG

## 📄 License

Choose a license before distributing the project. For example, an MIT License can be added by creating a `LICENSE` file with the appropriate license text.

---

⭐ If you find this project interesting, consider starring the repository and following its development.
