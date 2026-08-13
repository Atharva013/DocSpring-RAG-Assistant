"""
DocSpring Streamlit frontend.

Simple, fast, centered UI for persistent multi-PDF RAG chat.
"""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
import streamlit as st
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000").rstrip("/")
FAST_TIMEOUT = 45
DETAIL_TIMEOUT = 90
UPLOAD_TIMEOUT = 600
CHAT_TIMEOUT = 300


st.set_page_config(
    page_title="DocSpring",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="expanded",
)


def styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] { font-family: Inter, sans-serif; }

        .stApp {
            background: #f6f8fc;
            color: #111827;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        .block-container {
            max-width: 900px;
            padding-top: 1.4rem;
        }

        .top-card {
            background: linear-gradient(135deg, #111827, #1d4ed8);
            border-radius: 24px;
            padding: 26px 28px;
            color: white;
            box-shadow: 0 18px 50px rgba(37, 99, 235, .20);
            margin-bottom: 18px;
        }

        .top-card h1 {
            margin: 0;
            font-size: 2.2rem;
            letter-spacing: -0.04em;
        }

        .top-card p {
            color: #dbeafe;
            margin: 8px 0 0 0;
            font-size: 1rem;
        }

        .info-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin: 12px 0 18px 0;
        }

        .info-box {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 16px;
            padding: 12px 14px;
        }

        .info-box span {
            color: #6b7280;
            font-size: .78rem;
            font-weight: 700;
        }

        .info-box b {
            display: block;
            margin-top: 3px;
            color: #111827;
            font-size: 1.15rem;
        }

        .doc-list {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 14px 16px;
            margin-bottom: 16px;
        }

        .doc-chip, .source-chip {
            display: inline-block;
            padding: 6px 10px;
            margin: 4px 5px 4px 0;
            border-radius: 999px;
            font-size: .84rem;
            font-weight: 700;
        }

        .doc-chip {
            color: #1e40af;
            background: #dbeafe;
            border: 1px solid #bfdbfe;
        }

        .source-chip {
            color: #065f46;
            background: #d1fae5;
            border: 1px solid #a7f3d0;
        }

        .empty {
            background: white;
            border: 1px dashed #cbd5e1;
            color: #64748b;
            border-radius: 18px;
            padding: 28px;
            text-align: center;
            margin: 12px 0;
        }

        .small-muted {
            color: #64748b;
            font-size: .86rem;
        }

        div[data-testid="stChatMessage"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 4px;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 700;
        }

        @media (max-width: 720px) {
            .info-row { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def request_api(
    method: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
    timeout: int = FAST_TIMEOUT,
) -> Any:
    try:
        response = requests.request(
            method,
            f"{BACKEND_API_URL}{path}",
            json=json,
            files=files,
            timeout=timeout,
        )
    except requests.ReadTimeout as exc:
        raise RuntimeError(
            "Backend is still processing or Azure took too long. Try again in a moment."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Backend is not reachable at {BACKEND_API_URL}. Start FastAPI first."
        ) from exc

    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(str(detail))

    return response.json() if response.content else None


def fmt_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%d %b %I:%M %p")
    except ValueError:
        return value


def short(value: str, length: int = 8) -> str:
    return value[:length]


@st.cache_data(ttl=8, show_spinner=False)
def cached_sessions() -> list[dict[str, Any]]:
    return request_api("GET", "/sessions", timeout=FAST_TIMEOUT)


def clear_cache() -> None:
    cached_sessions.clear()


def create_session() -> dict[str, Any]:
    clear_cache()
    return request_api("POST", "/sessions", timeout=FAST_TIMEOUT)


def get_detail(session_id: str) -> dict[str, Any]:
    return request_api("GET", f"/sessions/{session_id}", timeout=DETAIL_TIMEOUT)


def upload(session_id: str, file: Any) -> dict[str, Any]:
    return request_api(
        "POST",
        f"/sessions/{session_id}/upload",
        files={"file": (file.name, file.getvalue(), "application/pdf")},
        timeout=UPLOAD_TIMEOUT,
    )


def chat(session_id: str, question: str) -> dict[str, Any]:
    return request_api(
        "POST",
        f"/sessions/{session_id}/chat",
        json={"question": question},
        timeout=CHAT_TIMEOUT,
    )


def init_state() -> None:
    st.session_state.setdefault("session_id", None)
    st.session_state.setdefault("detail", None)


def load_session(session_id: str) -> None:
    st.session_state.session_id = session_id
    st.session_state.detail = get_detail(session_id)


def sidebar() -> None:
    with st.sidebar:
        st.title("📘 DocSpring")
        st.caption("Multi-PDF RAG Chat")

        if st.button("New chat", type="primary", use_container_width=True):
            with st.spinner("Creating chat..."):
                session = create_session()
                load_session(session["session_id"])
                st.rerun()

        st.divider()
        st.subheader("Chats")

        try:
            sessions = cached_sessions()
        except RuntimeError as exc:
            st.error(str(exc))
            return

        if not sessions:
            st.caption("No chats yet.")
            return

        for item in sessions:
            label = item.get("title") or "New chat"
            caption = f"{item.get('document_count', 0)} PDFs · {fmt_date(item.get('updated_at'))}"
            active = item["session_id"] == st.session_state.session_id

            if st.button(
                ("● " if active else "") + label[:32],
                key=item["session_id"],
                help=caption,
                use_container_width=True,
            ):
                with st.spinner("Opening chat..."):
                    load_session(item["session_id"])
                    st.rerun()


def landing() -> None:
    st.markdown(
        """
        <div class="top-card">
            <h1>Ask questions across your PDFs</h1>
            <p>Create a chat, upload documents, then ask in the box below. Your sessions stay saved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="empty">
            <b>Start here</b><br/>
            Click <b>New chat</b> in the sidebar, upload PDFs, and begin asking questions.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header(detail: dict[str, Any]) -> None:
    session = detail["session"]
    docs = detail["documents"]
    messages = detail["messages"]
    title = session.get("title") or "New chat"

    st.markdown(
        f"""
        <div class="top-card">
            <h1>{title}</h1>
            <p>Session {short(session["session_id"])} · updated {fmt_date(session.get("updated_at"))}</p>
        </div>
        <div class="info-row">
            <div class="info-box"><span>PDFs</span><b>{len(docs)}</b></div>
            <div class="info-box"><span>Messages</span><b>{len(messages)}</b></div>
            <div class="info-box"><span>Backend</span><b>{BACKEND_API_URL.replace("http://", "")}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_docs(detail: dict[str, Any]) -> None:
    docs = detail["documents"]
    if not docs:
        st.markdown(
            '<div class="empty">No PDFs indexed yet. Upload documents below.</div>',
            unsafe_allow_html=True,
        )
        return

    chips = "".join(
        f'<span class="doc-chip">📄 {doc["filename"]} · {doc["chunks_indexed"]} chunks</span>'
        for doc in docs
    )
    st.markdown(f'<div class="doc-list"><b>Indexed PDFs</b><br/>{chips}</div>', unsafe_allow_html=True)


def upload_area(session_id: str) -> None:
    with st.expander("Upload PDFs", expanded=True):
        files = st.file_uploader(
            "Choose one or more PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            help="Large or scanned PDFs may take 1–3 minutes because Azure Document Intelligence extracts them first.",
        )

        if files and st.button("Upload and index", type="primary", use_container_width=True):
            progress = st.progress(0)
            results: list[str] = []
            for index, file in enumerate(files, start=1):
                progress.progress((index - 1) / len(files), text=f"Indexing {file.name}...")
                try:
                    result = upload(session_id, file)
                    results.append(f"{result['filename']} ({result['chunks_indexed']} chunks)")
                except RuntimeError as exc:
                    st.error(f"{file.name}: {exc}")
            progress.progress(1.0, text="Done")
            if results:
                st.success("Indexed: " + ", ".join(results))
                clear_cache()
                load_session(session_id)
                st.rerun()


def render_messages(detail: dict[str, Any]) -> None:
    messages = detail["messages"]
    if not messages:
        st.markdown(
            '<div class="empty">Ask something like: “Summarize the uploaded PDFs” or “Compare the key points.”</div>',
            unsafe_allow_html=True,
        )
        return

    for msg in messages:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["message"])


def chat_box(session_id: str) -> None:
    question = st.chat_input("Ask a question about the uploaded PDFs")
    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        holder = st.empty()
        holder.markdown("Searching your PDFs and drafting an answer...")
        try:
            result = chat(session_id, question)
            holder.markdown(result["answer"])
            if result.get("sources"):
                chips = "".join(
                    f'<span class="source-chip">{source}</span>'
                    for source in result["sources"]
                )
                st.markdown(chips, unsafe_allow_html=True)
            st.caption(f"Retrieved chunks: {result.get('retrieved_chunks', 0)}")
            clear_cache()
            load_session(session_id)
        except RuntimeError as exc:
            holder.error(str(exc))


def active_chat() -> None:
    session_id = st.session_state.session_id
    if not session_id:
        landing()
        return

    try:
        detail = get_detail(session_id)
        st.session_state.detail = detail
    except RuntimeError as exc:
        st.error(str(exc))
        return

    render_header(detail)
    render_docs(detail)
    upload_area(session_id)
    st.divider()
    st.subheader("Chat")
    render_messages(detail)
    chat_box(session_id)


def main() -> None:
    styles()
    init_state()
    sidebar()
    active_chat()


if __name__ == "__main__":
    main()
