# PersonalGPT Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                             │
│              ┌──────────────────────────┐                    │
│              │   Next.js Frontend       │                    │
│              │  (Chat UI, Components)   │                    │
│              └────────────┬─────────────┘                    │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Auth &     │  │   Session    │  │   Route     │       │
│  │  Middleware  │  │  Management  │  │  Handlers   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐  ┌──▼─────────┐ ┌▼──────────┐
│  LangChain   │  │ PostgreSQL  │ │  Redis    │
│  Orchestration│  │  (Primary   │ │  (Cache)  │
│              │  │   DB)       │ └───────────┘
└───────┬──────┘  └──────┬──────┘
        │                │
    ┌───▼────┐      ┌────▼────┐
    │ Chroma  │      │ pgvector│
    │(Vector) │      │(Vector) │
    └─────────┘      └─────────┘
        │
    ┌───▼──────────────┐
    │  LLM Providers   │
    │ (OpenAI, Claude) │
    └──────────────────┘
```

## Component Details

### 1. Frontend (Next.js)
- **Chat Interface**: React components for conversation UI
- **Session State**: Client-side and server-side state management
- **API Client**: Axios/Fetch for backend communication
- **Auth**: JWT token storage and refresh logic

### 2. Backend (FastAPI)
- **API Routes**: RESTful endpoints for chat, history, settings
- **Middleware**: Auth validation, CORS, logging
- **Session Manager**: Track active conversations
- **Request Handler**: Process user queries and route to LLM

### 3. AI Orchestration (LangChain)
- **Prompt Management**: Template and dynamic prompt construction
- **Memory Management**: Conversation history and context
- **Tool Integration**: Connect to search, calculators, APIs
- **Agent Loops**: Agentic reasoning workflows

### 4. Data Layers

#### PostgreSQL (Primary)
- User accounts & preferences
- Conversation metadata
- Session logs
- Structured business logic

#### Chroma (Vector Store)
- Embeddings of past conversations
- Document embeddings for RAG
- Semantic search index

#### Redis (Cache)
- Session data (short-lived)
- Cached embeddings
- Rate limiting
- Real-time chat state

## Data Flow

1. **User Query** → Frontend captures input
2. **API Request** → Backend receives with JWT token
3. **Context Retrieval** → Query vector DB for relevant history
4. **LLM Invocation** → LangChain builds prompt with context
5. **LLM Response** → Stream response back to frontend
6. **Storage** → Save to PostgreSQL + embeddings to vector DB
7. **UI Update** → Frontend displays response with history

## Authentication Flow

1. User logs in with credentials
2. Backend validates and returns JWT token
3. Frontend stores token (localStorage/secure cookie)
4. All API requests include token in Authorization header
5. Backend validates token on each request
6. Token refresh logic for expired tokens
