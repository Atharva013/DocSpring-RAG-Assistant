# DocSpring — React + Material UI Frontend

<p align="center">
  <strong>Modern, Responsive Web Interface for Multi-PDF RAG Intelligence</strong>
</p>

This directory contains the primary frontend application for DocSpring, built using **React 19**, **Material UI (MUI v9)**, and **Vite**.

---

## 🎨 Material UI (MUI) Design Architecture

The UI adheres to modern web design standards, featuring custom HSL color palettes, subtle elevation cards, soft gradients, and interactive micro-animations.

### Theme & Global Tokens (`src/theme/theme.js`)
- **Primary Color**: Emerald Green (`#16a34a` main, `#4ade80` light, `#15803d` dark)
- **Secondary Color**: Vivid Orange (`#f97316` main)
- **Background**: Soft Slate Gray (`#f8fafc` default, `#ffffff` paper cards, `#0f172a` dark sidebar)
- **Typography**: Inter / Roboto typography scale with defined weights (`700`, `600`, `500`)
- **Border Radius**: Unified `12px` card radius and `10px` button radius.

---

## 🧩 Component Breakdown (`src/components/`)

| Component File | Responsibilities & MUI Components Used |
| :--- | :--- |
| **`Sidebar.jsx`** | Session drawer navigation list, branding header, "New Chat" action button, and session deletion controls. <br> *(MUI: `Drawer`, `List`, `ListItemButton`, `ListItemIcon`, `ListItemText`, `IconButton`)* |
| **`HeroHeader.jsx`** | Active session summary widget displaying title, update timestamp, total indexed chunk counter, and model badges (`mistral`, `bge-small`). <br> *(MUI: `Paper`, `Typography`, `Chip`, `Stack`, `Button`)* |
| **`DocumentsPanel.jsx`** | Displays currently indexed PDF files per session, showing page count, file size, and chunk metrics. <br> *(MUI: `Paper`, `Typography`, `Chip`, `Stack`)* |
| **`UploadPanel.jsx`** | Expandable dropzone container allowing users to upload PDF documents with progress feedback. <br> *(MUI: `Accordion`, `AccordionSummary`, `AccordionDetails`, `LinearProgress`, `Button`)* |
| **`MessageList.jsx`** | Chat stream view with empty-state suggestion chips, Markdown message formatting (`react-markdown`), source citation expanders, copy button, and skeleton loading indicator. <br> *(MUI: `Box`, `Paper`, `Avatar`, `Typography`, `Chip`, `Tooltip`, `Accordion`)* |
| **`ChatInput.jsx`** | Floating input bar anchored at the bottom of the viewport with send button and keyboard submit handlers. <br> *(MUI: `Paper`, `InputBase`, `IconButton`, `CircularProgress`)* |
| **`DeleteDialog.jsx`** | Accessible confirmation modal dialog triggered before deleting a session. <br> *(MUI: `Dialog`, `DialogTitle`, `DialogContent`, `DialogActions`, `Button`)* |

---

## 📡 API Integration (`src/api/`)

- **`client.js`**: Central Axios client pre-configured with `baseURL: 'http://localhost:8000'` and timeout handlers.
- **`sessions.js`**: Encapsulates session management requests (`getSessions`, `createSession`, `getSessionDetail`, `deleteSession`, `renameSession`).
- **`chat.js`**: Submits question payloads to `/sessions/{id}/chat` and fetches system health details.
- **`upload.js`**: Handles multi-part `FormData` PDF uploads to `/sessions/{id}/upload`.

---

## 🚀 Available Scripts

In the `frontend-react` directory, you can run:

### `npm run dev`
Runs the app in development mode using Vite.  
Open [http://localhost:5173](http://localhost:5173) to view it in your browser. The page reloads automatically when you save changes.

### `npm run build`
Bundles the app into static production files in the `dist` folder. Optimizes CSS, JavaScript, and asset assets for deployment.

### `npm run preview`
Locally previews the production build created in the `dist` directory.

### `npm run lint`
Runs ESLint across all `.js` and `.jsx` source files to verify syntax and hook rules.

---

## ⚙️ Environment Configuration

By default, the React app communicates with the FastAPI backend at `http://localhost:8000`. To target a custom backend host, update `src/api/client.js` or set an environment variable `VITE_API_BASE_URL`.
