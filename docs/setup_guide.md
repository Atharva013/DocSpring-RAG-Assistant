# Complete Azure Setup & Deployment Guide

This guide provides step-by-step instructions for provisioning Azure AI services and Azure AI Foundry resources, configuring environment variables, installing Python & Node.js dependencies, and running both the backend and frontend applications.

---

## 📋 System Prerequisites

- **Python**: 3.10 or higher ([python.org](https://www.python.org/))
- **Node.js**: 18.0 or higher with `npm` ([nodejs.org](https://nodejs.org/))
- **Azure Subscription**: Active Azure account (Azure for Students, Free Trial, or Pay-As-You-Go)
- **Azure CLI**: Installed and authenticated (`az login`)

---

## 1. Provision Azure Resources

You will need to create the following 4 primary resource components in the Azure Portal and Azure AI Foundry:

### A. Azure Blob Storage
1. Create a **Storage Account** in your resource group.
2. Under **Data storage**, create a Container named `pdf-uploads` (Access level: *Private*).
3. Copy your **Storage Account Connection String** from **Access keys**.

### B. Azure Document Intelligence (Standard S0 Tier)
1. Create an **Azure AI Document Intelligence** resource.
2. Select the **Standard S0 Tier** for high-throughput OCR text extraction without free-tier page processing limits.
3. Copy the **Endpoint URL** and **API Key 1** from **Keys and Endpoint**.

### C. Azure AI Foundry (Model Deployments)
1. Open the [Azure AI Foundry Portal](https://ai.azure.com/) (Azure AI Studio).
2. Create or connect your Azure OpenAI workspace.
3. Deploy the **Chat Model**:
   - Model: `gpt-4.1-mini` (or `gpt-4o-mini`)
   - Deployment Name: `gpt-4.1-mini`
4. Deploy the **Embedding Model**:
   - Model: `text-embedding-3-small`
   - Deployment Name: `text-embedding-3-small`
5. Copy your workspace **Endpoint URL**, **API Key**, and API Version (e.g. `2024-08-01-preview`).

### D. Azure AI Search
1. Create an **Azure AI Search** resource (F0 Free tier or Basic/Standard).
2. Copy the **Url Endpoint** and **Primary Admin Key** from **Keys**.

---

## 2. Configure Environment Variables

Create a `.env` file in the project root directory by copying `.env.example`:

```bash
cp .env.example .env
```

Open `.env` in your editor and enter your Azure resource values:

```env
# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
AZURE_STORAGE_CONTAINER_NAME=pdf-uploads

# Azure Document Intelligence (Standard S0 Tier)
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://<your-doc-intel-name>.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_azure_doc_intel_key

# Azure AI Foundry / Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-foundry-resource-name>.openai.azure.com/
AZURE_OPENAI_KEY=your_azure_foundry_key
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4.1-mini
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<your-search-resource-name>.search.windows.net
AZURE_SEARCH_KEY=your_azure_search_admin_key
AZURE_SEARCH_INDEX_NAME=pdf-chat-index

# Backend URL
BACKEND_API_URL=http://localhost:8000
```

> [!CAUTION]
> **Security Reminder**: Never commit your `.env` file to source control. The `.gitignore` file is pre-configured to ignore `.env`.

---

## 3. Install Backend Dependencies

From the project root directory:

```bash
# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4. Run the Backend FastAPI Server

With the virtual environment activated, start the backend server:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- **Backend REST API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Interactive Docs**: `http://localhost:8000/redoc`

*(Upon backend startup, `ensure_index_exists()` automatically initializes the `pdf-chat-index` in Azure AI Search if it doesn't already exist).*

---

## 5. Run the Primary React MUI Frontend

Open a new terminal window:

```bash
# Navigate to frontend-react directory
cd DocSpring-RAG-Assistant/frontend-react

# Install Node modules
npm install

# Start Vite dev server
npm run dev
```

- **React Dashboard URL**: `http://localhost:5173`

---

## 6. (Optional) Run Streamlit Frontend

If you wish to run the alternative Streamlit dashboard:

```bash
# From project root with virtual environment activated
streamlit run frontend-streamlit/app.py
```

- **Streamlit App URL**: `http://localhost:8501`

---

## 🛠️ Verification & Troubleshooting

### Verification Checklist
1. Open `http://localhost:5173`.
2. Click **New Chat** to initialize a new session.
3. Drag & drop one or more PDF files into the upload dropzone. Check that files upload to **Azure Blob Storage**, extract text via **Azure Document Intelligence (S0)**, and index 1536-dim embeddings via **Azure AI Foundry** into **Azure AI Search**.
4. Submit a question in the chat bar. Verify that `gpt-4.1-mini` via **Azure AI Foundry** returns an answer rendered with bold markdown section headings (**Summary**, **Key points**, **Sources**) and page-level citations across your uploaded PDFs.

### Common Troubleshooting

#### 1. `ResourceNotFoundError` on Azure Blob Storage
- **Cause**: The storage container name specified in `.env` does not exist or account connection string is invalid.
- **Fix**: Verify `AZURE_STORAGE_CONTAINER_NAME=pdf-uploads` and ensure container permission is valid.

#### 2. `azure.core.exceptions.HttpResponseError: Invalid Request` on Document Intelligence
- **Cause**: The SAS URL expired or endpoint is incorrect.
- **Fix**: Check `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT` and `AZURE_DOCUMENT_INTELLIGENCE_KEY` in `.env`. Ensure your Document Intelligence resource is active.

#### 3. `azure.core.exceptions.HttpResponseError` on Azure AI Search / Foundry
- **Cause**: Vector dimensions mismatch or deployment name typo.
- **Fix**: Ensure your Azure AI Foundry embedding deployment is named `text-embedding-3-small` (1536 dims) and chat deployment is named `gpt-4.1-mini`.