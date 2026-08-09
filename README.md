# DocSpring 

A Retrieval-Augmented Generation (RAG) chatbot that lets you upload a single PDF and have a conversation with it — powered end-to-end by Azure AI services.

Built as a hands-on Azure AI project during my AIML internship at Emerson, this project explores Azure Blob Storage, Azure Document Intelligence, Azure OpenAI, and Azure AI Search in a single, cost-conscious pipeline (built on an Azure for Students subscription).

## Features

- Upload any PDF and chat with its contents in natural language
- Text extraction via Azure Document Intelligence (works on both text-based and scanned PDFs)
- Chunking and embedding generation via Azure OpenAI
- Vector search and retrieval via Azure AI Search (Free tier)
- Answer generation via Azure OpenAI (GPT-4.1 Nano)
- Single-session scope — each new upload clears the previous document's data

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Storage | Azure Blob Storage |
| Text Extraction | Azure Document Intelligence |
| Embeddings & Chat | Azure OpenAI (GPT-4.1 Nano) |
| Vector Search | Azure AI Search (F0 tier) |

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full pipeline breakdown and data flow.

## Getting Started

See [docs/setup_guide.md](docs/setup_guide.md) for Azure resource provisioning and local setup instructions.

## Project Structure

```
docspring-pdf-chat/
├── backend/          # FastAPI app, routers, and Azure service integrations
├── frontend/         # Streamlit chat UI
├── docs/             # Architecture and setup documentation
├── requirements.txt
└── .env.example
```

## Screenshots

Coming soon — see [docs/screenshots](docs/screenshots).

## License

This project is licensed under the terms of the [MIT License](LICENSE).
