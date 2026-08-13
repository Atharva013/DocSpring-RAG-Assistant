"""
DocSpring Streamlit frontend.

Modern multi-session PDF chat UI backed by the FastAPI RAG backend.
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
REQUEST_TIMEOUT = 120


st.set_page_config(
    page_title="DocSpring AI",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #070A12;
            --panel: rgba(14, 20, 35, 0.76);
            --panel-strong: rgba(21, 30, 52, 0.92);
            --stroke: rgba(148, 163, 184, 0.22);
            --text: #E5EEF9;
            --muted: #8EA4C8;
            --accent: #60A5FA;
            --accent-2: #A78BFA;
            --green: #34D399;
            --pink: #F472B6;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            color: var(--text);
            background:
                radial-gradient(circle at top left, rgba(96, 165, 250, 0.22), transparent 34rem),
                radial-gradient(circle at top right, rgba(167, 139, 250, 0.18), transparent 32rem),
                linear-gradient(135deg, #060812 0%, #0B1020 45%, #111827 100%);
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(15, 23, 42, 0.94), rgba(2, 6, 23, 0.94));
            border-right: 1px solid var(--stroke);
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        .block-container {
            padding-top: 2.2rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 1.45rem 1.55rem;
            border: 1px solid var(--stroke);
            border-radius: 28px;
            background:
                linear-gradient(135deg, rgba(96, 165, 250, 0.16), rgba(167, 139, 250, 0.12)),
                rgba(15, 23, 42, 0.72);
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.32);
        }

        .hero::after {
            content: "";
            position: absolute;
            right: -5rem;
            top: -6rem;
            width: 16rem;
            height: 16rem;
            border-radius: 999px;
            background: rgba(96, 165, 250, 0.20);
            filter: blur(8px);
        }

        .eyebrow {
            color: var(--green);
            text-transform: uppercase;
            letter-spacing: .16em;
            font-size: .76rem;
            font-weight: 800;
            margin-bottom: .35rem;
        }

        .hero h1 {
            font-size: clamp(2.1rem, 4vw, 4.2rem);
            line-height: .96;
            letter-spacing: -.06em;
            margin: 0;
        }

        .hero p {
            max-width: 740px;
            margin: .8rem 0 0;
            color: var(--muted);
            font-size: 1rem;
        }

        .glass-card {
            border: 1px solid var(--stroke);
            background: var(--panel);
            border-radius: 24px;
            padding: 1rem 1.1rem;
            box-shadow: 0 18px 54px rgba(0, 0, 0, 0.24);
            backdrop-filter: blur(18px);
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .75rem;
            margin: 1rem 0;
        }

        .metric-card {
            border: 1px solid var(--stroke);
            border-radius: 20px;
            padding: .9rem 1rem;
            background: rgba(15, 23, 42, .66);
        }

        .metric-card span {
            display: block;
            color: var(--muted);
            font-size: .78rem;
            font-weight: 600;
        }

        .metric-card strong {
            display: block;
            margin-top: .2rem;
            font-size: 1.35rem;
        }

        .doc-chip, .source-chip {
            display: inline-flex;
            align-items: center;
            gap: .35rem;
            margin: .22rem .28rem .22rem 0;
            padding: .38rem .62rem;
            border-radius: 999px;
            border: 1px solid rgba(96, 165, 250, .28);
            background: rgba(96, 165, 250, .10);
            color: #DCEBFF;
            font-size: .82rem;
            font-weight: 600;
        }

        .source-chip {
            border-color: rgba(52, 211, 153, .28);
            background: rgba(52, 211, 153, .10);
        }

        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: var(--muted);
            border: 1px dashed rgba(148, 163, 184, .28);
            border-radius: 28px;
            background: rgba(15, 23, 42, .38);
        }

        .empty-state h3 {
            color: var(--text);
            margin-bottom: .35rem;
        }

        .session-pill {
            padding: .68rem .82rem;
            border-radius: 18px;
            border: 1px solid var(--stroke);
            background: rgba(15, 23, 42, .54);
            margin-bottom: .55rem;
        }

        .session-pill small {
            color: var(--muted);
        }

        div[data-testid="stChatMessage"] {
            border-radius: 22px;
            background: rgba(15, 23, 42, 0.48);
            border: 1px solid rgba(148, 163, 184, 0.12);
        }

        .stButton > button {
            border-radius: 999px;
            border: 1px solid rgba(96, 165, 250, .36);
            background: linear-gradient(135deg, rgba(96, 165, 250, .18), rgba(167, 139, 250, .16));
            color: var(--text);
            font-weight: 700;
        }

        .stButton > button:hover {
            border-color: rgba(96, 165, 250, .72);
            color: white;
        }

        [data-testid="stFileUploader"] {
            border: 1px dashed rgba(96, 165, 250, .32);
            border-radius: 24px;
            padding: .7rem;
            background: rgba(15, 23, 42, .46);
        }

        @media (max-width: 780px) {
            .metric-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def api_request(
    method: str,
    path: str,
    *,
    json: dict[str, Any] | None = None,
    files: dict[str, Any] | None = None,
    timeout: int = REQUEST_TIMEOUT,
) -> Any:
    url = f"{BACKEND_API_URL}{path}"
    try:
        response = requests.request(
            method,
            url,
            json=json,
            files=files,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not reach backend at {BACKEND_API_URL}. Is FastAPI running?"
        ) from exc

    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(detail)

    if not response.content:
        return None
    return response.json()


def format_datetime(value: str | None) -> str:
    if not value:
        return "—"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%d %b, %I:%M %p")
    except ValueError:
        return value


def short_id(value: str | None) -> str:
    return value[:8] if value else "--------"


def get_sessions() -> list[dict[str, Any]]:
    return api_request("GET", "/sessions")


def create_session() -> dict[str, Any]:
    return api_request("POST", "/sessions")


def get_session_detail(session_id: str) -> dict[str, Any]:
    return api_request("GET", f"/sessions/{session_id}")


def upload_pdf(session_id: str, uploaded_file: Any) -> dict[str, Any]:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }
    return api_request("POST", f"/sessions/{session_id}/upload", files=files, timeout=240)


def ask_question(session_id: str, question: str) -> dict[str, Any]:
    return api_request(
        "POST",
        f"/sessions/{session_id}/chat",
        json={"question": question},
        timeout=180,
    )


def ensure_state() -> None:
    defaults = {
        "current_session_id": None,
        "sessions": [],
        "session_detail": None,
        "last_error": None,
        "uploading": False,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def refresh_sessions() -> None:
    st.session_state.sessions = get_sessions()


def load_session(session_id: str) -> None:
    st.session_state.current_session_id = session_id
    st.session_state.session_detail = get_session_detail(session_id)


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### 🧊 DocSpring")
        st.caption("Persistent multi-PDF RAG on Azure")

        if st.button("＋ New research chat", use_container_width=True):
            try:
                session = create_session()
                refresh_sessions()
                load_session(session["session_id"])
                st.rerun()
            except RuntimeError as exc:
                st.error(str(exc))

        st.divider()

        try:
            refresh_sessions()
        except RuntimeError as exc:
            st.error(str(exc))
            return

        st.markdown("#### Sessions")
        if not st.session_state.sessions:
            st.caption("No sessions yet. Create one and start uploading PDFs.")
            return

        for session in st.session_state.sessions:
            session_id = session["session_id"]
            title = session.get("title") or "New chat"
            is_active = session_id == st.session_state.current_session_id
            label_prefix = "● " if is_active else ""
            label = f"{label_prefix}{title[:34]}"
            help_text = (
                f"{session.get('document_count', 0)} PDFs • "
                f"Updated {format_datetime(session.get('updated_at'))} • "
                f"ID {short_id(session_id)}"
            )
            if st.button(label, key=f"session-{session_id}", help=help_text, use_container_width=True):
                load_session(session_id)
                st.rerun()


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Azure RAG Lab • Emerson AIML Internship</div>
            <h1>Chat with PDFs,<br/>without losing the thread.</h1>
            <p>
                Upload multiple documents into a persistent session, ask questions across them,
                and get grounded answers with source-aware retrieval.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_overview(detail: dict[str, Any]) -> None:
    session = detail["session"]
    documents = detail["documents"]
    messages = detail["messages"]

    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card"><span>Session</span><strong>{short_id(session["session_id"])}</strong></div>
            <div class="metric-card"><span>PDFs indexed</span><strong>{len(documents)}</strong></div>
            <div class="metric-card"><span>Messages</span><strong>{len(messages)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if documents:
        chips = "".join(
            f'<span class="doc-chip">📄 {doc["filename"]} · {doc["chunks_indexed"]} chunks</span>'
            for doc in documents
        )
        st.markdown(f'<div class="glass-card">{chips}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="empty-state">
                <h3>No PDFs in this session yet</h3>
                <p>Upload one or more PDFs below. Once indexed, this session becomes queryable.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_upload_panel(session_id: str) -> None:
    with st.container(border=False):
        st.markdown("#### Add PDFs to this session")
        uploaded_files = st.file_uploader(
            "Drop PDFs here",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if uploaded_files and st.button("Index uploaded PDFs", use_container_width=True):
            progress = st.progress(0, text="Preparing upload...")
            successes = []
            try:
                for index, uploaded_file in enumerate(uploaded_files, start=1):
                    progress.progress(
                        (index - 1) / len(uploaded_files),
                        text=f"Indexing {uploaded_file.name}...",
                    )
                    result = upload_pdf(session_id, uploaded_file)
                    successes.append(result)

                progress.progress(1.0, text="PDF indexing complete.")
                st.success(
                    "Indexed "
                    + ", ".join(
                        f"{item['filename']} ({item['chunks_indexed']} chunks)"
                        for item in successes
                    )
                )
                load_session(session_id)
                st.rerun()
            except RuntimeError as exc:
                st.error(f"Upload failed: {exc}")


def render_messages(detail: dict[str, Any]) -> None:
    messages = detail["messages"]
    if not messages:
        st.markdown(
            """
            <div class="empty-state">
                <h3>Ask your first question</h3>
                <p>Try: “Summarize these PDFs”, “Compare the documents”, or “What are the key action items?”</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for message in messages:
        role = message["role"]
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(message["message"])


def render_chat_box(session_id: str) -> None:
    question = st.chat_input("Ask across every PDF in this session...")
    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking through your PDFs...")
        try:
            response = ask_question(session_id, question)
            placeholder.markdown(response["answer"])
            if response.get("sources"):
                chips = "".join(
                    f'<span class="source-chip">↳ {source}</span>'
                    for source in response["sources"]
                )
                st.markdown(chips, unsafe_allow_html=True)
            st.caption(f"Retrieved chunks: {response.get('retrieved_chunks', 0)}")
            load_session(session_id)
        except RuntimeError as exc:
            placeholder.error(str(exc))


def render_active_session() -> None:
    session_id = st.session_state.current_session_id

    if session_id is None:
        render_hero()
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="empty-state">
                <h3>Start with a new research chat</h3>
                <p>Use the sidebar button to create a persistent session, then upload PDFs into it.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    try:
        detail = get_session_detail(session_id)
        st.session_state.session_detail = detail
    except RuntimeError as exc:
        st.error(str(exc))
        return

    session = detail["session"]
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">Active session • {format_datetime(session.get("updated_at"))}</div>
            <h1>{session.get("title", "New chat")}</h1>
            <p>Session ID: {session_id}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_session_overview(detail)

    with st.expander("Upload more PDFs", expanded=not detail["documents"]):
        render_upload_panel(session_id)

    st.markdown("### Conversation")
    render_messages(detail)
    render_chat_box(session_id)


def main() -> None:
    inject_styles()
    ensure_state()
    render_sidebar()
    render_active_session()


if __name__ == "__main__":
    main()
