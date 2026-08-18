# Azure System Architecture

## Overview

DocSpring RAG Assistant is built on a high-performance, cloud-native RAG architecture built on top of **Microsoft Azure AI Services** and **Azure AI Foundry**. The system decouples frontend clients, RESTful API orchestration, blob storage, OCR extraction, multi-PDF vector search, and LLM inference.

---

## High-Level System Architecture Diagram

```mermaid
graph TD
    User([User Browser]) -->|HTTP / JSON| FrontendReact[React 19 + MUI Frontend]
    User -->|HTTP / HTML| FrontendStreamlit[Streamlit Dashboard]
    
    subgraph FastAPI Backend App
        API[FastAPI Router Engine]
        SessionRouter[Routers: /sessions]
        UploadRouter[Routers: /upload]
        ChatRouter[Routers: /chat]
        
        BlobSvc[Blob Service]
        DocIntelSvc[Extraction Service]
        ChunkingSvc[Chunking Service]
        EmbeddingSvc[Embedding Service]
        SearchSvc[Search Service]
        ChatSvc[Chat Service]
    end
    
    subgraph Azure Cloud Platform
        AzureBlob[(Azure Blob Storage\nContainer: pdf-uploads)]
        AzureDocIntel[Azure Document Intelligence\nS0 Standard Tier - prebuilt-read]
        AzureAISearch[(Azure AI Search\nIndex: pdf-chat-index)]
        
        subgraph Azure AI Foundry Hub
            AzureFoundryEmbed[Deployment: text-embedding-3-small\n1536-dimensional vectors]
            AzureFoundryChat[Deployment: gpt-4.1-mini\nGrounded Chat Completion]
        end
    end
    
    FrontendReact --> API
    FrontendStreamlit --> API
    API --> SessionRouter
    API --> UploadRouter
    API --> ChatRouter
    
    UploadRouter --> BlobSvc
    BlobSvc -->|1. Upload Multi-PDF Blobs| AzureBlob
    BlobSvc -->|2. Generate Read SAS URLs| DocIntelSvc
    DocIntelSvc -->|3. Extract Multi-Page Spans| AzureDocIntel
    DocIntelSvc --> ChunkingSvc
    ChunkingSvc --> EmbeddingSvc
    EmbeddingSvc -->|4. Generate 1536-dim Vectors| AzureFoundryEmbed
    EmbeddingSvc --> SearchSvc
    SearchSvc -->|5. Index Chunks & Metadata| AzureAISearch
    
    ChatRouter --> EmbeddingSvc
    ChatRouter --> SearchSvc
    SearchSvc -->|6. KNN Vector Query + Session Filter| AzureAISearch
    ChatRouter --> ChatSvc
    ChatSvc -->|7. Grounded Multi-Doc Completion| AzureFoundryChat
```

---

## Detailed Data Pipelines

### 1. Multi-PDF Upload, Azure OCR & Vector Indexing Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Client as Frontend (React / Streamlit)
    participant FastAPI as FastAPI (/sessions/{id}/upload)
    participant BlobSvc as Azure Blob Storage
    participant DocIntel as Azure Document Intelligence (S0)
    participant Chunker as Chunking Service
    participant Embedder as Azure AI Foundry (text-embedding-3-small)
    participant AISearch as Azure AI Search (pdf-chat-index)

    User->>Client: Select PDF files & click Upload
    Client->>FastAPI: POST /sessions/{sessionId}/upload (Multipart FormData)
    FastAPI->>BlobSvc: Upload PDF blob under path {sessionId}/{docId}/{filename}
    BlobSvc-->>FastAPI: Blob Storage URL
    FastAPI->>BlobSvc: Generate short-lived Read SAS URL (15 min expiry)
    BlobSvc-->>FastAPI: Read SAS URL
    FastAPI->>DocIntel: Trigger prebuilt-read S0 model using Read SAS URL
    DocIntel-->>FastAPI: result.content + page.spans offset metadata
    FastAPI->>Chunker: Split page text (Chunk size: 1600, Overlap: 200)
    Chunker-->>FastAPI: Text chunks tagged with 1-indexed page numbers
    FastAPI->>Embedder: Generate 1536-dimensional vector embeddings
    Embedder-->>FastAPI: List of 1536 float arrays
    FastAPI->>AISearch: Upload documents (content, embedding, session_id, document_id, page_number)
    AISearch-->>FastAPI: Index confirmation
    FastAPI-->>Client: 200 OK (Filename, Pages, Chunks indexed)
    Client-->>User: Render document summary card in UI
```

---

### 2. Conversational RAG Query & Multi-PDF Answer Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Client as Frontend (React / Streamlit)
    participant FastAPI as FastAPI (/sessions/{id}/chat)
    participant Embedder as Azure AI Foundry (text-embedding-3-small)
    participant AISearch as Azure AI Search (pdf-chat-index)
    participant ChatSvc as Chat Service (Formatting Engine)
    participant FoundryChat as Azure AI Foundry (gpt-4.1-mini)

    User->>Client: Type question & submit
    Client->>FastAPI: POST /sessions/{sessionId}/chat { question }
    FastAPI->>Embedder: Generate query vector embedding (1536 dims)
    Embedder-->>FastAPI: Query vector array
    FastAPI->>AISearch: VectorizedQuery (k=8, filter: session_id eq '{sessionId}')
    AISearch-->>FastAPI: Top matching chunks across multi-PDFs + Source filenames + Page numbers
    FastAPI->>ChatSvc: Build context prompt template with retrieved chunks
    ChatSvc->>FoundryChat: Send system prompt & grounded context payload (gpt-4.1-mini)
    FoundryChat-->>ChatSvc: Generated raw response
    ChatSvc->>ChatSvc: Normalize headings (**Summary**, **Key points**, **Sources**)
    ChatSvc-->>FastAPI: Clean formatted markdown answer
    FastAPI-->>Client: JSON response { answer, sources_detail }
    Client-->>User: Render markdown message bubble with expandable citations
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