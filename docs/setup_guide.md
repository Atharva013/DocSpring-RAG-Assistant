# Setup Guide

## Prerequisites

- Python 3.10+
- An Azure subscription (Azure for Students works)
- Azure CLI installed and authenticated (`az login`)

## 1. Provision Azure Resources

1. **Azure Blob Storage** — create a Storage Account and a container for PDF uploads.
2. **Azure AI Search** — create a Search service on the Free (F0) tier.
3. **Azure OpenAI** — deploy a chat model (GPT-4.1 Nano) and an embeddings model.
4. **Azure Document Intelligence** — create a Document Intelligence resource.
5. **Azure AI Foundry** — optional, used for monitoring deployments.

Note down the endpoint and key for each resource — you'll need them in the next step.

## 2. Configure Environment Variables

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Fill in `.env` with your Azure resource endpoints and keys. **Never commit `.env`** — only `.env.example` (with placeholder values) is tracked in git.

## 3. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## 5. Run the Frontend

In a separate terminal:

```bash
cd frontend
streamlit run app.py
```

## 6. Try It Out

1. Open the Streamlit UI in your browser.
2. Upload a PDF.
3. Wait for upload → extraction → indexing to complete (status shown in the UI).
4. Ask questions about the document in the chat box.

## Notes

- Only one PDF is supported per session. Uploading a new PDF clears the previous document's data from both Blob Storage and the Azure AI Search index.
- Monitor your Azure OpenAI and Document Intelligence usage in the Azure Portal to stay within student credit limits.