# Azure System Architecture

## Overview

DocSpring RAG Assistant is built on a high-performance, cloud-native RAG architecture built on top of **Microsoft Azure AI Services** and **Azure AI Foundry**. The system decouples frontend clients, RESTful API orchestration, blob storage, OCR extraction, multi-PDF vector search, and LLM inference.

---

## High-Level System Architecture Diagram

```mermaid
graph TD
    classDef frontend fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff;
    classDef backend fill:#0284c7,stroke:#0369a1,stroke-width:2px,color:#fff;
    classDef azure fill:#0078d4,stroke:#005a9e,stroke-width:2px,color:#fff;
    classDef store fill:#6366f1,stroke:#4338ca,stroke-width:2px,color:#fff;

    subgraph Clients["1. Frontend Presentation Layer"]
        ReactUI["React 19 + MUI Frontend"]:::frontend
        StreamlitUI["Streamlit Dashboard"]:::frontend
    end

    subgraph Backend["2. FastAPI Orchestration Layer"]
        UploadAPI["PDF Upload Endpoint<br/>/sessions/{id}/upload"]:::backend
        ChatAPI["Chat Question Endpoint<br/>/sessions/{id}/chat"]:::backend
        SessionAPI["Session Management Router<br/>/sessions"]:::backend
    end

    subgraph Ingestion["3. Azure Ingestion & OCR Services"]
        AzureBlob[("Azure Blob Storage<br/>Container: pdf-uploads")]:::store
        AzureDocIntel["Azure Document Intelligence<br/>S0 Standard Tier - prebuilt-read"]:::azure
    end

    subgraph AIPlatform["4. Azure AI Foundry & Vector Search Services"]
        AzureFoundryEmbed["Azure AI Foundry Embeddings<br/>Deployment: text-embedding-3-small"]:::azure
        AzureAISearch[("Azure AI Search Index<br/>HNSW Vector Index: pdf-chat-index")]:::store
        AzureFoundryChat["Azure AI Foundry Chat<br/>Deployment: gpt-4.1-mini"]:::azure
    end

    ReactUI -->|REST / JSON| UploadAPI
    ReactUI -->|REST / JSON| ChatAPI
    ReactUI -->|REST / JSON| SessionAPI
    StreamlitUI -->|REST / JSON| UploadAPI
    StreamlitUI -->|REST / JSON| ChatAPI

    UploadAPI -->|1. Store Raw PDFs| AzureBlob
    UploadAPI -->|2. Read SAS URL| AzureDocIntel
    AzureDocIntel -->|3. Extracted Text & Spans| UploadAPI
    UploadAPI -->|4. Text Chunks| AzureFoundryEmbed
    AzureFoundryEmbed -->|5. 1536-dim Vectors & Metadata| AzureAISearch

    ChatAPI -->|1. Question Text| AzureFoundryEmbed
    AzureFoundryEmbed -->|2. Query Embedding Vector| AzureAISearch
    AzureAISearch -->|3. HNSW Vector Search & Session Filter| ChatAPI
    ChatAPI -->|4. Grounded Context Payload| AzureFoundryChat
    AzureFoundryChat -->|5. Structured Answer| ReactUI
```

---

## Detailed Data Pipelines

### 1. Multi-PDF Upload, Azure OCR & Vector Indexing Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User as User Browser
    participant UI as React / Streamlit Frontend
    participant API as FastAPI Backend (/upload)
    participant Blob as Azure Blob Storage
    participant OCR as Azure Doc Intelligence (S0)
    participant Embed as Azure AI Foundry (text-embedding-3-small)
    participant VectorDB as Azure AI Search (pdf-chat-index)

    User->>UI: Select PDF files & click Upload
    UI->>API: POST /sessions/{sessionId}/upload (Multipart FormData)
    API->>Blob: Upload PDF blob to {sessionId}/{docId}/{filename}
    Blob-->>API: Blob Storage URL Confirmation
    API->>Blob: Generate short-lived Read SAS URL (15 min validity)
    Blob-->>API: Read SAS URL
    API->>OCR: Trigger prebuilt-read S0 model via Read SAS URL
    OCR-->>API: result.content + page.spans character offsets
    API->>API: Split text into chunks (1600 chars, 200 overlap)
    API->>Embed: Generate 1536-dim embeddings for text chunks
    Embed-->>API: List of 1536 float vector arrays
    API->>VectorDB: Index chunks (content, embedding, session_id, doc_id, page_number)
    VectorDB-->>API: Upload Acknowledgement
    API-->>UI: 200 OK Response (Filename, Total Pages, Indexed Chunks)
    UI-->>User: Display Document Summary Card in UI
```

---

### 2. Conversational RAG Query & Multi-PDF Answer Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User as User Browser
    participant UI as React / Streamlit Frontend
    participant API as FastAPI Backend (/chat)
    participant Embed as Azure AI Foundry (text-embedding-3-small)
    participant VectorDB as Azure AI Search (pdf-chat-index)
    participant ChatLLM as Azure AI Foundry (gpt-4.1-mini)

    User->>UI: Submit question in chat bar
    UI->>API: POST /sessions/{sessionId}/chat { question }
    API->>Embed: Generate query vector embedding (1536 dims)
    Embed-->>API: Query vector array
    API->>VectorDB: HNSW Vector Search (k=8, filter: session_id eq '{sessionId}')
    VectorDB-->>API: Top matching chunks across multi-PDFs + Page numbers
    API->>API: Build system prompt template with retrieved context
    API->>ChatLLM: Send grounded completion request
    ChatLLM-->>API: Raw LLM response string
    API->>API: Normalize section headers (**Summary**, **Key points**, **Sources**)
    API-->>UI: Return JSON { answer, sources_detail }
    UI-->>User: Render markdown message bubble with page citations
```

---

## Session Isolation & Security Model

To prevent cross-session document leakage in multi-tenant or multi-session environments:

1. **Azure Blob Storage Pathing**: PDF files are stored using structured blob paths:  
   `{session_id}/{document_id}/{filename}`
2. **Azure AI Search OData Filtering**: Every indexed chunk document contains a `session_id` filterable field. Similarity queries execute with strict OData security filters:  
   `$filter=session_id eq '{session_id}'`
3. **Session Teardown**: When a session is deleted (`DELETE /sessions/{sessionId}`), the backend executes:
   - `delete_session_blobs()`: Deletes all session PDF blobs from Azure Storage.
   - `delete_session_chunks()`: Purges all matching documents from the Azure AI Search index.

---

## Azure Service Component Responsibilities

| Backend File | Azure Integration & Responsibility |
| :--- | :--- |
| `backend/config.py` | Loads credentials for Azure Blob Storage, Document Intelligence (S0), Azure AI Foundry, and Azure AI Search from `.env`. |
| `backend/services/blob_service.py` | Uploads PDF files to Azure Blob Storage and generates read-only SAS URLs for Azure Document Intelligence. |
| `backend/services/extraction_service.py` | Calls Azure Document Intelligence (`prebuilt-read` S0 Tier) via SAS URL to extract full-text layout and page-level character offsets (`spans`). |
| `backend/services/chunking_service.py` | Performs recursive text chunking with configurable overlap (`1600` chars / `200` overlap). |
| `backend/services/embedding_service.py` | Calls Azure AI Foundry embedding deployment (`text-embedding-3-small`, 1536 dimensions). |
| `backend/services/search_service.py` | Manages Azure AI Search index schema (`pdf-chat-index`), HNSW vector profile, document indexing, and session-scoped multi-PDF vector queries. |
| `backend/services/chat_service.py` | Sends grounded context prompts to Azure AI Foundry Chat deployment (`gpt-4.1-mini`) and normalizes answer section formatting. |

---

## Cost & Resource Optimization

1. **Direct SAS URL Extraction**: The PDF file streams directly from Azure Blob Storage to Azure Document Intelligence via SAS URL. The file is never held in backend RAM.
2. **Standard S0 Tier OCR Scaling**: Uses Azure Document Intelligence Standard `S0` Tier for fast multi-page and multi-PDF extraction without page rate-limiting errors.
3. **Azure AI Foundry Management**: Centralized deployment hub for model monitoring, cost control, and managing `gpt-4.1-mini` and `text-embedding-3-small`.
4. **Batch Indexing**: Document chunks and embeddings are uploaded to Azure AI Search in batch sizes of `100` documents to minimize HTTP overhead.
5. **Optimized Embedding Dimensions**: Uses `text-embedding-3-small` (1536 dimensions) for lower vector search index storage footprint while maintaining high retrieval precision.