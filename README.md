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

## Overview

**DocSpring** is an enterprise-grade, Azure-native Retrieval-Augmented Generation (RAG) platform that enables users to upload multiple PDF documents per chat session and conduct grounded, natural language Q&A against their combined contents.

Built end-to-end on Azure AI Cloud Services (Azure Blob Storage, Azure Document Intelligence Standard S0 Tier, Azure AI Foundry, and Azure AI Search), DocSpring extracts text across multi-page documents with page-level accuracy, indexes 1536-dimensional embeddings into an HNSW vector index, and generates answers strictly grounded in the source documents with exact source filename and page number citations.

---

## Key Features

- **Multi-PDF Document Indexing** — Upload and index multiple PDF files per session, querying across the entire document collection simultaneously.
- **Azure AI Foundry Model Deployment Hub** — Centralized deployment management in Azure AI Foundry hosting `gpt-4.1-mini` for chat inference and `text-embedding-3-small` (1536 dimensions) for vector embeddings.
- **Azure Document Intelligence S0 Standard OCR** — High-throughput text extraction powered by Azure Document Intelligence Standard S0 tier, enabling large multi-page PDF processing without free-tier page limits.
- **Azure AI Search Vector Index** — High-performance HNSW vector search (`pdf-chat-index`) with strict session filtering (`session_id eq '{id}'`) preventing session cross-talk.
- **Secure SAS URL Processing** — PDFs are stored in Azure Blob Storage and read directly by Azure Document Intelligence via short-lived SAS URLs, so PDF contents never bloat backend RAM.
- **Strict Source & Page Citations** — AI answers are automatically formatted into normalized markdown sections (Summary, Key Points, Sources) citing exact filenames and page numbers.
- **Modern React 19 + Material UI Frontend** — Responsive dark/light interface with subtle micro-animations, loading skeletons, expandable source citations, and quick suggestion chips.
- **Multi-Session Isolation** — Supports multiple independent chat sessions with full lifecycle management (create, title, select, delete).
- **Streamlit Alternative Frontend** — Includes an alternative Streamlit UI (`frontend-streamlit`) for rapid prototyping.

---

## Tech Stack & Azure Architecture

| Layer                 | Azure Service / Technology                                                  | Description                                                              |
|------------------------|-------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| Object Storage         | [Azure Blob Storage](https://azure.microsoft.com/services/storage/blobs/)     | Stores uploaded PDF files under session-scoped blob paths.                 |
| Document OCR           | [Azure Document Intelligence](https://azure.microsoft.com/services/ai-services/document-intelligence/) | Standard S0 Tier running the `prebuilt-read` layout model for large multi-page PDFs. |
| AI Model Management     | [Azure AI Foundry](https://ai.azure.com/) (Azure AI Studio)                   | Central portal managing model deployments (`gpt-4.1-mini` and `text-embedding-3-small`). |
| Embeddings              | Azure OpenAI via Azure AI Foundry                                             | Generates 1536-dimensional vector embeddings (`text-embedding-3-small`).   |
| Vector Search           | [Azure AI Search](https://azure.microsoft.com/services/search/)               | HNSW vector index (`pdf-chat-index`) with OData session-filter security.   |
| Chat LLM                | Azure OpenAI via Azure AI Foundry                                             | Generates grounded responses (`gpt-4.1-mini`).                             |
| Backend API             | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)                       | Async REST API orchestration with Pydantic settings.                       |
| Primary Frontend        | [React 19](https://react.dev/) + [Material UI (MUI v9)](https://mui.com/)     | Built with Vite for rapid execution and a modern UI aesthetic.             |
| Secondary Frontend      | [Streamlit](https://streamlit.io/)                                            | Lightweight Python chat interface.                                         |

---

## System Architecture & Data Flow

**Document ingestion pipeline**

```
                        User PDF Uploads (Multiple PDFs)
                                     │
                                     ▼
┌───────────────────────────────────────────────────────────────────┐
│  FastAPI Backend  —  POST /sessions/{id}/upload                    │
│                                                                      │
│  1. Upload PDFs to Azure Blob Storage                               │
│  2. Generate short-lived read SAS URL                               │
│  3. Extract text and page spans via Azure Document Intelligence (S0)│
│  4. Split text into overlapping chunks (1600 characters)            │
│  5. Generate embeddings via Azure AI Foundry (text-embedding-3-small)│
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────┐
│  Azure AI Search  —  Index: pdf-chat-index                          │
│  HNSW vector index storing chunk text, embeddings, and metadata     │
└───────────────────────────────────────────────────────────────────┘
```

**Query and response pipeline**

```
                              User Question
                                     │
                                     ▼
┌───────────────────────────────────────────────────────────────────┐
│  FastAPI Backend  —  POST /sessions/{id}/chat                       │
│                                                                      │
│  1. Generate query embedding via Azure AI Foundry (text-embedding)  │
│  2. Query Azure AI Search KNN ($filter = session_id eq '{id}')      │
│  3. Send top matching context to Azure AI Foundry (gpt-4.1-mini)    │
│  4. Normalize response into headers (Summary, Key Points, Sources)  │
└──────────────────────────────────┬───────────────────────────────────┘
                                   │
                                   ▼
                    React 19 MUI Dashboard / Streamlit Interface
```

For complete technical specifications and sequence diagrams, see [docs/architecture.md](docs/architecture.md).

---

## Repository Structure

```
DocSpring-RAG-Assistant/
├── backend/                    FastAPI backend API and Azure service modules
│   ├── main.py                 FastAPI entry point and CORS configuration
│   ├── config.py                Pydantic Azure credentials settings loader
│   ├── routers/                 REST endpoints (sessions, upload, chat, health)
│   └── services/                Azure service modules
│       ├── blob_service.py            Azure Blob Storage and SAS generation
│       ├── extraction_service.py      Azure Document Intelligence S0 OCR
│       ├── embedding_service.py       Azure AI Foundry embedding generation
│       ├── search_service.py          Azure AI Search HNSW index and KNN query
│       ├── chunking_service.py        Recursive text splitter
│       └── chat_service.py            Azure AI Foundry chat completion (gpt-4.1-mini)
│
├── frontend-react/             Production React 19 + Material UI application
│   ├── src/
│   │   ├── api/                  Axios HTTP client connecting to FastAPI
│   │   ├── components/           MUI components (Sidebar, Hero, MessageList, etc.)
│   │   ├── theme/                Material UI custom theme tokens and palette
│   │   ├── App.jsx               Application state and session coordinator
│   │   └── main.jsx              React DOM mounting and ThemeProvider
│   ├── package.json             Node dependencies and npm scripts
│   └── vite.config.js           Vite bundler configuration
│
├── frontend-streamlit/         Streamlit alternative interface
│   └── app.py                   Streamlit app script
│
├── docs/                        Documentation and visual assets
│   ├── architecture.md          Full technical architecture document
│   ├── setup_guide.md           Step-by-step Azure setup guide
│   └── assets/screenshots/      Application screenshots directory
│
├── requirements.txt             Python backend dependencies
└── .env.example                 Environment variables template
```

---

## Screenshots

- [DocSpring Multi-PDF Dashboard & Session Navigation](docs/assets/screenshots/docspring_multi_pdf_dashboard.png) — Dark sidebar session list, active session stats, multi-PDF document summary panel, drag-and-drop file uploader, and interactive chat stream.
- [Grounded AI Response & Citation Drawer](docs/assets/screenshots/docspring_single_pdf_chat.png) — AI response normalized into markdown headings (Summary, Key Points) with page-level source citations (`Page 1, Chunk 1`, `Page 2, Chunk 2`).

---

## Quick Start Guide

### Prerequisites

- **Python** — 3.10 or higher
- **Node.js** — 18.0 or higher (for the React frontend)
- **Azure Account** — an Azure subscription with Azure Blob Storage, Azure Document Intelligence (S0 tier), Azure AI Foundry (hosting `gpt-4.1-mini` and `text-embedding-3-small`), and Azure AI Search resources provisioned.

---

### 1. Environment Configuration

Copy the `.env.example` template to `.env` in the root folder:

```bash
cp .env.example .env
```

Fill in the Azure resource credentials in `.env`:

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

# Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI backend server
uvicorn backend.main:app --reload --port 8000
```

The API runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.

---

### 3. Frontend Setup (React + Material UI)

In a separate terminal window:

```bash
# Navigate to the frontend directory
cd frontend-react

# Install Node modules
npm install

# Launch the Vite development server
npm run dev
```

The React application is available at `http://localhost:5173`.

---

### 4. Alternative Frontend (Streamlit)

To launch the Streamlit dashboard:

```bash
# From the project root, with the virtual environment activated
streamlit run frontend-streamlit/app.py
```

For complete step-by-step Azure resource provisioning, see [docs/setup_guide.md](docs/setup_guide.md).

---

## API Endpoints Summary

| Method   | Endpoint                     | Description                                                                 |
|----------|-------------------------------|-------------------------------------------------------------------------------|
| `GET`    | `/sessions`                   | List all active chat sessions.                                                |
| `POST`   | `/sessions`                   | Create a new chat session.                                                    |
| `GET`    | `/sessions/{id}`              | Get session details, messages, and the list of indexed documents.             |
| `DELETE` | `/sessions/{id}`              | Delete a session, purge its Azure Blobs, and clear its Azure Search index entries. |
| `PATCH`  | `/sessions/{id}/title`        | Rename a session title.                                                       |
| `POST`   | `/sessions/{id}/upload`       | Upload a PDF to Azure Blob Storage, run Azure Document Intelligence (S0), and index it in Azure AI Search. |
| `POST`   | `/sessions/{id}/chat`         | Ask a question against multi-PDF session chunks via `gpt-4.1-mini`.           |
| `GET`    | `/health/info`                | Health check and active Azure AI Foundry deployment model names.              |

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).
