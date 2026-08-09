# Architecture

## Overview

DocSpring PDF Chat follows a linear RAG pipeline. The Streamlit frontend handles PDF upload and chat interaction; the FastAPI backend orchestrates every processing step, all of which run on Azure.

## Data Flow — Upload and Indexing

```
User (Streamlit)
   |  uploads PDF
   v
FastAPI /upload
   |  stores raw file
   v
Azure Blob Storage
   |  triggers extraction
   v
Azure Document Intelligence
   |  extracted text
   v
Chunking (backend service)
   |  chunks
   v
Azure OpenAI (embeddings)
   |  chunks + embeddings
   v
Azure AI Search (index)
```

## Data Flow — Chat

```
User (Streamlit)
   |  asks a question
   v
FastAPI /chat
   |  embed query
   v
Azure AI Search (vector search)
   |  top matching chunks
   v
Azure OpenAI (chat completion)
   |  generated answer
   v
Streamlit (displayed to user)
```

## Component Responsibilities

| Component | Responsibility |
|---|---|
| `routers/upload.py` | Accepts the PDF, delegates storage and extraction |
| `routers/chat.py` | Accepts a question, delegates retrieval and generation |
| `services/blob_service.py` | Uploads/fetches files from Azure Blob Storage |
| `services/extraction_service.py` | Calls Azure Document Intelligence to extract text |
| `services/chunking_service.py` | Splits extracted text into overlapping chunks |
| `services/embedding_service.py` | Generates embeddings via Azure OpenAI |
| `services/search_service.py` | Creates/clears/queries the Azure AI Search index |
| `services/chat_service.py` | Sends retrieved context and question to Azure OpenAI for the final answer |

## Session Handling

The system is scoped to one PDF per session. When a new PDF is uploaded, the previous file is removed from Blob Storage and its entries are cleared from the Azure AI Search index before the new document is processed. This keeps the Free (F0) tier index within its limits and avoids unbounded storage growth.

## Cost Considerations

Since this runs on an Azure for Students subscription, every design decision favors low cost:

- Azure AI Search on the Free (F0) tier — no cost
- Azure OpenAI deployed on the cheapest available chat model (GPT-4.1 Nano)
- Document Intelligence used sparingly — one extraction per session
- No persistence across sessions, so no ongoing storage growth