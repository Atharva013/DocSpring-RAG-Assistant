<div align="center">

# DocSpring — Azure-Powered Multi-PDF RAG Assistant

<p align="center">
  <strong>An Azure-powered RAG assistant for indexing multiple PDFs and answering questions with exact page-level citations.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Azure_AI_Foundry-GPT--4.1--Mini-0078D4.svg?style=flat&logo=microsoftazure" alt="Azure AI Foundry">
  <img src="https://img.shields.io/badge/Azure_AI_Search-HNSW_Vector_Search-0089D6.svg?style=flat&logo=microsoftazure" alt="Azure AI Search">
  <img src="https://img.shields.io/badge/Azure_Doc_Intelligence-S0_Standard_OCR-0078D4.svg?style=flat" alt="Azure Document Intelligence S0 Tier">
  <img src="https://img.shields.io/badge/Azure_Blob_Storage-Multi--PDF_Store-0089D6.svg?style=flat" alt="Azure Blob Storage">
  <img src="https://img.shields.io/badge/FastAPI-Backend_API-009688.svg?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React_19-Material_UI_v9-61DAFB.svg?style=flat&logo=react" alt="React MUI">
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat" alt="License">
</p>

</div>

---

## 🌟 Overview

**DocSpring** is an enterprise-grade, Azure-native Retrieval-Augmented Generation (RAG) platform that enables users to upload **multiple PDF documents per chat session** and conduct grounded, natural language Q&A against their combined contents.

Built end-to-end on **Azure AI Cloud Services** (Azure Blob Storage, Azure Document Intelligence Standard `S0` Tier, Azure AI Foundry, and Azure AI Search), DocSpring extracts text across multi-page documents with page-level accuracy, indexes 1536-dimensional embeddings into an HNSW vector index, and generates answers strictly grounded in your documents with exact **source filename and page number citations**.

---

## ✨ Key Features

- 📑 **Multi-PDF Document Indexing**: Upload and index multiple PDF files per session, querying across your entire document collection simultaneously.
- 🏢 **Azure AI Foundry Model Deployment Hub**: Centralized deployment management in Azure AI Foundry hosting `gpt-4.1-mini` for chat inference and `text-embedding-3-small` (1536 dims) for vector embeddings.
- ⚡ **Azure Document Intelligence S0 Standard OCR**: High-throughput text extraction powered by Azure Document Intelligence Standard `S0` tier, enabling large multi-page PDF processing without free-tier page limits.
- 🔍 **Azure AI Search Vector Index**: High-performance HNSW vector search (`pdf-chat-index`) with strict session filtering (`session_id eq '{id}'`) preventing session cross-talk.
- 🔒 **Secure SAS URL Processing**: PDFs are stored in Azure Blob Storage and read directly by Azure Document Intelligence via short-lived SAS URLs — PDF contents never bloat backend RAM.
- 🎯 **Strict Source & Page Citations**: AI answers are automatically formatted into normalized markdown sections (**Summary**, **Key points**, **Sources**) citing exact filenames and page numbers.
- 🎨 **Modern React 19 + Material UI Frontend**: Responsive dark/light interface with subtle micro-animations, loading skeletons, expandable source citations, and quick suggestion chips.
- 💬 **Multi-Session Isolation**: Supports multiple independent chat sessions with full lifecycle management (create, title, select, delete).
- 📊 **Streamlit Alternative Frontend**: Includes an alternative Streamlit UI (`frontend-streamlit`) for rapid prototyping.

---

## 🛠️ Tech Stack & Azure Architecture

| Layer | Azure Service / Technology | Description |
| :--- | :--- | :--- |
| **Object Storage** | [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/) | Stores uploaded PDF files under session-scoped blob paths. |
| **Document OCR** | [Azure Document Intelligence](https://azure.microsoft.com/services/ai-services/document-intelligence/) | **Standard `S0` Tier** running `prebuilt-read` layout model for large multi-page PDFs. |
| **AI Model Management** | [Azure AI Foundry](https://ai.azure.com/) (Azure AI Studio) | Central portal managing model deployments (`gpt-4.1-mini` & `text-embedding-3-small`). |
| **Embeddings** | Azure OpenAI via Azure AI Foundry | Generates 1536-dimensional vector embeddings (`text-embedding-3-small`). |
| **Vector Search** | [Azure AI Search](https://azure.microsoft.com/services/search/) | HNSW vector index (`pdf-chat-index`) with OData session filter security. |
| **Chat LLM** | Azure OpenAI via Azure AI Foundry | Generates grounded responses (`gpt-4.1-mini`). |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+) | Async REST API orchestration with Pydantic settings. |
| **Primary Frontend** | [React 19](https://react.dev/) + [Material UI (MUI v9)](https://mui.com/) | Built with Vite for rapid execution and modern UI aesthetics. |
| **Secondary Frontend** | [Streamlit](https://streamlit.io/) | Lightweight Python chat interface. |

---

## 🏗️ System Architecture & Data Flow

```
[ User PDF Uploads (Multiple PDFs) ]
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ FastAPI Backend (/sessions/{id}/upload)                         │
│ ├── 1. Upload PDFs to Azure Blob Storage                         │
│ ├── 2. Generate short-lived Read SAS URL                         │
│ ├── 3. Extract text & page spans via Azure Doc Intelligence (S0) │
│ ├── 4. Split text into overlapping chunks (1600 chars)           │
│ └── 5. Embeddings via Azure AI Foundry (text-embedding-3-small)  │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│ Azure AI Search (Index: pdf-chat-index)                         │
│ (HNSW Vector Index storing chunk text, embeddings, & metadata)   │
└──────────────────────────────────────────────────────────────────┘
```

```
[ User Question ]
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│ FastAPI Backend (/sessions/{id}/chat)                           │
│ ├── 1. Query embedding via Azure AI Foundry (text-embedding-small)│
│ ├── 2. Azure AI Search KNN Query ($filter=session_id eq '{id}') │
│ ├── 3. Send top matching context to Azure AI Foundry gpt-4.1-mini│
│ └── 4. Normalize response headers (**Summary**, **Key points**)   │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
[ React 19 MUI Dashboard / Streamlit Interface ]
```

For complete technical specifications and sequence diagrams, see **[docs/architecture.md](docs/architecture.md)**.

---

## 📁 Repository Structure

```
DocSpring-RAG-Assistant/
├── backend/                  # FastAPI Backend API & Azure Services
│   ├── main.py               # FastAPI entry point & CORS configuration
│   ├── config.py             # Pydantic Azure credentials settings loader
│   ├── routers/              # REST Endpoints (sessions, upload, chat, health)
│   └── services/             # Azure Service Modules:
│       ├── blob_service.py         # Azure Blob Storage & SAS generation
│       ├── extraction_service.py   # Azure Document Intelligence S0 OCR
│       ├── embedding_service.py    # Azure AI Foundry Embedding generation
│       ├── search_service.py       # Azure AI Search HNSW Index & KNN query
│       ├── chunking_service.py     # Recursive text splitter
│       └── chat_service.py         # Azure AI Foundry Chat completion (gpt-4.1-mini)
│
├── frontend-react/           # Production React 19 + Material UI App
│   ├── src/
│   │   ├── api/              # Axios HTTP client connecting to FastAPI
│   │   ├── components/       # MUI Components (Sidebar, Hero, MessageList, etc.)
│   │   ├── theme/            # Material UI custom theme tokens & palette
│   │   ├── App.jsx           # Application state & session coordinator
│   │   └── main.jsx          # React DOM mounting & ThemeProvider
│   ├── package.json          # Node dependencies & npm scripts
│   └── vite.config.js        # Vite bundler configuration
│
├── frontend-streamlit/       # Streamlit alternative interface
│   └── app.py                # Streamlit app script
│
├── docs/                     # Documentation & visual assets
│   ├── architecture.md       # Full technical architecture document
│   ├── setup_guide.md        # Step-by-step Azure setup guide
│   └── assets/screenshots/   # Application screenshots directory
│
├── requirements.txt          # Python backend dependencies
└── .env.example              # Environment variables template
```

---

## 📸 Screenshots

Click the links below to view high-resolution screenshots of the DocSpring interface:

- 🖼️ [DocSpring Multi-PDF Dashboard & Session Navigation](docs/assets/screenshots/docspring_multi_pdf_dashboard.png) — Features the dark sidebar session list, active session stats, multi-PDF document summary panel, drag-and-drop file uploader, and interactive chat stream.
- 🖼️ [Grounded AI Response & Citation Drawer](docs/assets/screenshots/docspring_single_pdf_chat.png) — Demonstrates AI response normalized into bold markdown headings (**Summary**, **Key points**) along with page-level source citations (`Page 1 Chunk 1`, `Page 2 Chunk 2`).

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher (for React frontend)
- **Azure Account**: Azure Subscription with Azure Blob Storage, Azure Document Intelligence (S0 Tier), Azure AI Foundry (hosting `gpt-4.1-mini` & `text-embedding-3-small`), and Azure AI Search resources.

---

### 1. Environment Configuration

Copy the `.env.example` template to `.env` in the root folder:

```bash
cp .env.example .env
```

Fill in your Azure resource credentials in `.env`:

```env
# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER_NAME=pdf-uploads

# Azure Document Intelligence (Standard S0 Tier)
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://<your-doc-intel>.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key_here

# Azure AI Foundry / Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-foundry-resource>.openai.azure.com/
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4.1-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_KEY=your_key_here
AZURE_SEARCH_INDEX_NAME=pdf-chat-index
```

---

### 2. Backend Setup

```bash
# Clone the repository
git clone https://github.com/Atharva013/DocSpring-RAG-Assistant.git
cd DocSpring-RAG-Assistant

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI backend server
uvicorn backend.main:app --reload --port 8000
```
> The API will run at `http://localhost:8000`. Access interactive API documentation at `http://localhost:8000/docs`.

---

### 3. Frontend Setup (React Material UI)

In a separate terminal window:

```bash
# Navigate to frontend directory
cd frontend-react

# Install Node modules
npm install

# Launch Vite development server
npm run dev
```
> Access the React application at `http://localhost:5173`.

---

### 4. Alternative Frontend (Streamlit)

To launch the Streamlit dashboard:

```bash
# From project root with virtual environment activated
streamlit run frontend-streamlit/app.py
```

For complete step-by-step Azure resource provisioning, see **[docs/setup_guide.md](docs/setup_guide.md)**.

---

## ✨ API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/sessions` | List all active chat sessions |
| `POST` | `/sessions` | Create a new chat session |
| `GET` | `/sessions/{id}` | Get session details, messages & list of indexed documents |
| `DELETE` | `/sessions/{id}` | Delete session, purge Azure Blobs & clear Azure Search index documents |
| `PATCH` | `/sessions/{id}/title` | Rename session title |
| `POST` | `/sessions/{id}/upload` | Upload PDF to Azure Blob Storage, run Azure Doc Intelligence (S0) & index in Azure AI Search |
| `POST` | `/sessions/{id}/chat` | Ask a question against multi-PDF session chunks via `gpt-4.1-mini` |
| `GET` | `/health/info` | Health check & active Azure AI Foundry deployment model names |

---

## 📄 License

This project is licensed under the terms of the **[MIT License](LICENSE)**.
