"""
DocSpring Streamlit frontend - Premium UI Edition
Fresh mint-green + warm-orange + white showcase theme.
"""

from __future__ import annotations

import html
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests
import streamlit as st
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000").rstrip("/")
FAST_TIMEOUT    = 45
DETAIL_TIMEOUT  = 90
UPLOAD_TIMEOUT  = 600
CHAT_TIMEOUT    = 300
DELETE_TIMEOUT  = 240
INDIA_TZ        = ZoneInfo("Asia/Kolkata")


st.set_page_config(
    page_title="DocSpring AI",
    page_icon="📄",          # neutral document icon, not AI-generated feel
    layout="wide",
    initial_sidebar_state="expanded",
)


# ═══════════════════════════════════════════════════════════════════════════════
#  CSS  –  Mint-Green + Warm-Orange + White Theme
# ═══════════════════════════════════════════════════════════════════════════════
def css() -> None:
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

        <style>
        /* ── TOKENS ──────────────────────────────────────────────── */
        :root {
            /* Core palette */
            --green-50:   #f0fdf4;
            --green-100:  #dcfce7;
            --green-200:  #bbf7d0;
            --green-400:  #4ade80;
            --green-500:  #22c55e;
            --green-600:  #16a34a;
            --green-700:  #15803d;
            --orange-50:  #fff7ed;
            --orange-100: #ffedd5;
            --orange-400: #fb923c;
            --orange-500: #f97316;
            --orange-600: #ea580c;

            /* Semantic */
            --bg:          #f8fffe;
            --bg-card:     #ffffff;
            --bg-sidebar:  #ffffff;
            --text-dark:   #0f2318;
            --text-body:   #1d3a28;
            --text-muted:  #52796f;
            --text-light:  #84a98c;
            --border:      #d1fae5;
            --border-md:   #a7f3d0;
            --accent:      #16a34a;
            --accent-lt:   #4ade80;
            --accent-glow: rgba(22,163,74,0.15);
            --orange:      #f97316;
            --orange-lt:   #fb923c;
            --orange-glow: rgba(249,115,22,0.12);
            --shadow-sm:   0 1px 3px rgba(15,35,24,0.06), 0 1px 2px rgba(15,35,24,0.04);
            --shadow-md:   0 4px 16px rgba(15,35,24,0.08), 0 2px 6px rgba(15,35,24,0.05);
            --shadow-lg:   0 10px 40px rgba(15,35,24,0.10), 0 4px 12px rgba(15,35,24,0.06);
            --shadow-xl:   0 20px 60px rgba(15,35,24,0.12), 0 8px 20px rgba(15,35,24,0.07);
            --r-sm:  10px;
            --r-md:  16px;
            --r-lg:  22px;
            --r-xl:  28px;
        }

        /* ── GLOBAL ──────────────────────────────────────────────── */
        *, *::before, *::after { box-sizing: border-box; }

        /* Hide default Streamlit header banner (containing Deploy button) */
        header[data-testid="stHeader"],
        [data-testid="stHeader"] {
            display: none !important;
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
        }

        /* Thin mint scrollbar */
        ::-webkit-scrollbar { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track { background: var(--green-50); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--green-500), var(--orange-500));
            border-radius: 99px;
        }

        /* ── APP BACKGROUND ──────────────────────────────────────── */
        .stApp {
            background: linear-gradient(145deg, #f8fffe 0%, #f0fdf4 40%, #fff7ed 80%, #f8fffe 100%);
            background-attachment: fixed;
        }

        .block-container {
            max-width: 1600px;
            padding: 0.5rem 1.2rem 3rem;
        }

        /* Kill Streamlit's default dark overrides */
        .stMarkdown, .stText, p, li, label, span {
            color: var(--text-body);
        }

        .stCaptionContainer p {
            color: var(--text-muted) !important;
            font-size: 0.76rem !important;
        }

        .stAlert p { color: #1a1a1a !important; }

        /* ── LAYOUT SHELL ────────────────────────────────────────── */
        .app-shell {
            max-width: 1360px;   /* wider content area */
            margin: 0 auto;
        }

        /* ── SIDEBAR ─────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid var(--border-md) !important;
            box-shadow: 2px 0 20px rgba(22,163,74,0.07) !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text-dark) !important;
        }

        /* Sidebar session list buttons — light blue text */
        [data-testid="stSidebar"] .stButton > button {
            min-height: 38px !important;
            font-size: 0.83rem !important;
            border-radius: var(--r-sm) !important;
            font-weight: 600 !important;
            color: #2563eb !important;
        }
        [data-testid="stSidebar"] .stButton > button * {
            color: #2563eb !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            color: #1d4ed8 !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover * {
            color: #1d4ed8 !important;
        }

        /* ── SIDEBAR BRAND ───────────────────────────────────────── */
        .sb-brand {
            text-align: center;
            padding: 20px 8px 16px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 14px;
        }

        .sb-logo {
            width: 52px;
            height: 52px;
            border-radius: 16px;
            background: linear-gradient(135deg, #16a34a 0%, #22c55e 50%, #f97316 100%);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            box-shadow: 0 8px 24px rgba(22,163,74,0.35), 0 2px 8px rgba(22,163,74,0.2);
            font-size: 1.4rem;
            animation: logoPulse 4s ease-in-out infinite;
        }

        @keyframes logoPulse {
            0%,100% { box-shadow: 0 8px 24px rgba(22,163,74,.35), 0 2px 8px rgba(22,163,74,.2); }
            50%      { box-shadow: 0 10px 32px rgba(22,163,74,.5), 0 4px 14px rgba(22,163,74,.3); }
        }

        .sb-title {
            margin: 0;
            font-size: 1.45rem;
            font-weight: 900;
            letter-spacing: -0.04em;
            background: linear-gradient(135deg, #16a34a 0%, #059669 50%, #f97316 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .sb-sub {
            font-size: 0.7rem !important;
            color: var(--text-light) !important;
            font-weight: 500 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            margin-top: 2px !important;
        }

        /* ── SESSION ITEMS ───────────────────────────────────────── */
        .session-meta {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.67rem;
            color: var(--text-light) !important;
            margin: -4px 0 8px 2px;
            padding-left: 2px;
        }

        .session-meta i { opacity: 0.6; font-size: 0.6rem; }

        .active-dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 6px var(--accent);
            display: inline-block;
            flex-shrink: 0;
            animation: dotBlink 1.8s ease infinite;
        }

        .idle-dot {
            width: 6px; height: 6px;
            border-radius: 50%;
            background: #d1fae5;
            border: 1px solid #a7f3d0;
            display: inline-block;
            flex-shrink: 0;
        }

        @keyframes dotBlink {
            0%,100% { opacity: 1; }
            50%      { opacity: 0.35; }
        }

        /* ── HERO CARD ───────────────────────────────────────────── */
        .hero-card {
            background: linear-gradient(135deg,
                rgba(22,163,74,0.08)  0%,
                rgba(255,255,255,0.9) 40%,
                rgba(249,115,22,0.06) 100%);
            border: 1px solid var(--border-md);
            border-radius: var(--r-xl);
            padding: 28px 32px;
            margin-bottom: 18px;
            position: relative;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
            animation: slideDown 0.5s cubic-bezier(0.34,1.56,0.64,1);
        }

        @keyframes slideDown {
            from { opacity:0; transform: translateY(-18px); }
            to   { opacity:1; transform: translateY(0); }
        }

        /* Animated top accent line */
        .hero-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #16a34a, #4ade80, #f97316, #16a34a);
            background-size: 300% 100%;
            animation: lineFlow 3s linear infinite;
        }

        @keyframes lineFlow {
            0%   { background-position: 0% 0%; }
            100% { background-position: 300% 0%; }
        }

        .hero-card h1 {
            margin: 0 0 6px;
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: -0.05em;
            color: var(--text-dark) !important;
        }

        .hero-card h1 span.grad {
            background: linear-gradient(135deg, #16a34a 0%, #059669 50%, #f97316 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero-card p {
            color: var(--text-muted) !important;
            font-size: 0.97rem;
            margin: 0;
            line-height: 1.65;
        }

        /* ── STATUS BADGE ────────────────────────────────────────── */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: var(--green-50);
            border: 1px solid var(--green-200);
            border-radius: 99px;
            padding: 7px 15px;
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--green-700);
            white-space: nowrap;
        }

        .status-badge .live-dot {
            width: 7px; height: 7px;
            border-radius: 50%;
            background: var(--green-500);
            animation: livePulse 1.6s ease infinite;
        }

        @keyframes livePulse {
            0%,100% { opacity:1; box-shadow: 0 0 0 0 rgba(34,197,94,.5); }
            50%      { opacity:0.7; box-shadow: 0 0 0 5px rgba(34,197,94,0); }
        }

        /* ── METRIC CARDS ────────────────────────────────────────── */
        /* All three cards are forced to identical height via grid + align-stretch */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-bottom: 18px;
            align-items: stretch;   /* ← key: cards stretch to tallest sibling */
        }

        .metric-card {
            background: #ffffff;
            border-radius: var(--r-lg);
            padding: 20px 20px 18px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow-md);
            display: flex;
            flex-direction: column;
            gap: 4px;
            position: relative;
            overflow: hidden;
            transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1),
                        box-shadow 0.25s ease;
            animation: cardUp 0.5s ease both;
        }

        .metric-card:nth-child(1) { animation-delay: 0.07s; }
        .metric-card:nth-child(2) { animation-delay: 0.14s; }
        .metric-card:nth-child(3) { animation-delay: 0.21s; }

        @keyframes cardUp {
            from { opacity:0; transform: translateY(16px); }
            to   { opacity:1; transform: translateY(0); }
        }

        /* Left accent stripe */
        .metric-card::before {
            content:'';
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 4px;
            border-radius: 4px 0 0 4px;
        }

        .metric-card.mc-green::before  { background: var(--green-500); }
        .metric-card.mc-orange::before { background: var(--orange-500); }
        .metric-card.mc-teal::before   { background: #0d9488; }

        .metric-card:hover {
            transform: translateY(-5px);
        }

        .metric-card.mc-green:hover  { box-shadow: var(--shadow-lg), 0 0 0 1px var(--green-200); }
        .metric-card.mc-orange:hover { box-shadow: var(--shadow-lg), 0 0 0 1px #fed7aa; }
        .metric-card.mc-teal:hover   { box-shadow: var(--shadow-lg), 0 0 0 1px #99f6e4; }

        .mc-icon-wrap {
            width: 36px; height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.95rem;
            margin-bottom: 8px;
            flex-shrink: 0;
        }

        .mc-green  .mc-icon-wrap { background: var(--green-50);  color: var(--green-600); border: 1px solid var(--green-200); }
        .mc-orange .mc-icon-wrap { background: var(--orange-50); color: var(--orange-600); border: 1px solid #fed7aa; }
        .mc-teal   .mc-icon-wrap { background: #f0fdfa; color: #0d9488; border: 1px solid #99f6e4; }

        .mc-label {
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-light) !important;
        }

        .mc-value {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1;
            color: var(--text-dark) !important;
            margin-top: 2px;
        }

        .mc-green  .mc-value { color: var(--green-700) !important; }
        .mc-orange .mc-value { color: var(--orange-600) !important; }
        .mc-teal   .mc-value { color: #0d9488 !important; }

        /* ── GLASS / INFO CARD ───────────────────────────────────── */
        .info-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--r-lg);
            box-shadow: var(--shadow-md);
            padding: 20px 22px;
            margin-bottom: 14px;
            transition: box-shadow 0.25s ease;
        }

        .info-card:hover { box-shadow: var(--shadow-lg); }

        .info-card-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
        }

        .card-icon-wrap {
            width: 32px; height: 32px;
            border-radius: 9px;
            background: var(--green-50);
            border: 1px solid var(--green-200);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            color: var(--green-600);
            flex-shrink: 0;
        }

        .card-icon-wrap.orange {
            background: var(--orange-50);
            border-color: #fed7aa;
            color: var(--orange-600);
        }

        .info-card-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--text-dark) !important;
            margin: 0;
        }

        /* ── BUTTONS ─────────────────────────────────────────────── */
        .stButton > button {
            border-radius: var(--r-md) !important;
            font-weight: 700 !important;
            min-height: 44px !important;
            font-size: 0.88rem !important;
            letter-spacing: 0.015em !important;
            transition: all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
        }

        /* Primary = gradient green → orange */
        .stButton > button[kind="primary"],
        .stButton > button[data-testid^="stBaseButton-primary"] {
            background: linear-gradient(135deg, #16a34a 0%, #22c55e 50%, #f97316 100%) !important;
            background-size: 200% 100% !important;
            color: #fff !important;
            border: none !important;
            box-shadow: 0 4px 18px rgba(22,163,74,.35), inset 0 1px 0 rgba(255,255,255,.15) !important;
            animation: btnFlow 5s ease infinite !important;
        }

        @keyframes btnFlow {
            0%,100% { background-position: 0% 50%; }
            50%      { background-position: 100% 50%; }
        }

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid^="stBaseButton-primary"]:hover {
            box-shadow: 0 8px 28px rgba(22,163,74,.45) !important;
        }

        /* Secondary */
        .stButton > button[kind="secondary"],
        .stButton > button[data-testid^="stBaseButton-secondary"] {
            background: #fff !important;
            border: 1px solid var(--border-md) !important;
            color: var(--text-body) !important;
        }

        .stButton > button[kind="secondary"]:hover,
        .stButton > button[data-testid^="stBaseButton-secondary"]:hover {
            border-color: var(--accent) !important;
            color: var(--accent) !important;
            box-shadow: 0 4px 14px rgba(22,163,74,.12) !important;
        }

        /* Sidebar buttons smaller */
        [data-testid="stSidebar"] .stButton > button {
            min-height: 36px !important;
            font-size: 0.81rem !important;
            border-radius: var(--r-sm) !important;
        }

        /* ── INPUT FIELDS ────────────────────────────────────────── */
        .stTextInput input,
        .stTextArea textarea {
            background: #fff !important;
            color: var(--text-dark) !important;
            border: 1px solid var(--border-md) !important;
            border-radius: var(--r-md) !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(22,163,74,.12) !important;
        }

        /* ── CHAT INPUT ──────────────────────────────────────────── */
        /* Redundant block removed - styled cleanly below */

        /* ── CHAT MESSAGES ───────────────────────────────────────── */
        div[data-testid="stChatMessage"] {
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-lg) !important;
            box-shadow: var(--shadow-sm) !important;
            animation: msgSlide 0.35s cubic-bezier(0.34,1.56,0.64,1) !important;
            margin-bottom: 10px !important;
            transition: box-shadow 0.2s ease !important;
        }

        div[data-testid="stChatMessage"]:hover {
            box-shadow: var(--shadow-md) !important;
        }

        @keyframes msgSlide {
            from { opacity:0; transform: translateY(10px); }
            to   { opacity:1; transform: translateY(0); }
        }

        div[data-testid="stChatMessage"] p,
        div[data-testid="stChatMessage"] li,
        div[data-testid="stChatMessage"] h1,
        div[data-testid="stChatMessage"] h2,
        div[data-testid="stChatMessage"] h3 {
            color: var(--text-dark) !important;
        }

        /* ── FILE UPLOADER ───────────────────────────────────────── */
        [data-testid="stFileUploader"] {
            background: linear-gradient(135deg, rgba(240,253,244,0.5) 0%, rgba(255,255,255,0.95) 100%) !important;
            border: 1.5px dashed #86efac !important;
            border-radius: var(--r-lg) !important;
            padding: 12px 16px !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: #22c55e !important;
            background: rgba(220,252,231,0.5) !important;
            box-shadow: 0 0 0 4px rgba(34,197,94,0.08) !important;
        }

        /* Override Streamlit's internal dark background for uploader dropzone and texts */
        [data-testid="stFileUploaderDropzone"],
        [data-testid="stFileUploader"] section {
            background: transparent !important;
            color: #14532d !important;
        }

        [data-testid="stFileUploader"] * {
            color: #14532d !important;
        }

        [data-testid="stFileUploader"] button {
            background-color: #ffffff !important;
            border: 1px solid #86efac !important;
            color: #15803d !important;
            font-weight: 600 !important;
            border-radius: var(--r-md) !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stFileUploader"] button:hover {
            background-color: #dcfce7 !important;
            border-color: #22c55e !important;
            color: #166534 !important;
        }

        /* ── EXPANDER ────────────────────────────────────────────── */
        [data-testid="stExpander"] {
            background: #ffffff !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--r-lg) !important;
            box-shadow: var(--shadow-sm) !important;
            overflow: hidden !important;
        }

        .streamlit-expanderHeader {
            background: var(--green-50) !important;
            font-weight: 600 !important;
            color: var(--text-dark) !important;
            transition: background 0.2s ease !important;
        }

        .streamlit-expanderHeader:hover {
            background: var(--green-100) !important;
        }

        /* ── PROGRESS BAR ────────────────────────────────────────── */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #16a34a, #4ade80, #f97316) !important;
            background-size: 200% 100% !important;
            animation: progAnim 2s linear infinite !important;
            border-radius: 99px !important;
        }

        @keyframes progAnim {
            0%   { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* ── DIVIDER ─────────────────────────────────────────────── */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--border-md), transparent) !important;
            margin: 12px 0 !important;
        }

        /* ── SOURCE CHIPS ────────────────────────────────────────── */
        .source-chip {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border-radius: 99px;
            padding: 5px 12px;
            margin: 4px 5px 4px 0;
            font-size: 0.77rem;
            font-weight: 600;
            background: var(--green-50);
            border: 1px solid var(--green-200);
            color: var(--green-700);
            transition: all 0.2s ease;
            animation: chipPop 0.3s cubic-bezier(0.34,1.56,0.64,1) both;
        }

        .source-chip i { font-size: 0.68rem; }

        .source-chip:hover {
            background: var(--green-100);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(22,163,74,.15);
        }

        @keyframes spin {
            from { transform: rotate(0deg); }
            to   { transform: rotate(360deg); }
        }

        @keyframes chipPop {
            from { opacity:0; transform: scale(0.8); }
            to   { opacity:1; transform: scale(1); }
        }

        /* ── DOC CHIPS ───────────────────────────────────────────── */
        .doc-chip {
            display: inline-flex;
            align-items: center;
            gap: 9px;
            border-radius: 12px;
            padding: 9px 14px;
            margin: 5px 6px 5px 0;
            font-size: 0.82rem;
            font-weight: 600;
            background: #fff;
            border: 1px solid var(--border-md);
            color: var(--text-body);
            transition: all 0.22s ease;
            box-shadow: var(--shadow-sm);
        }

        .doc-chip-icon {
            width: 28px; height: 28px;
            border-radius: 8px;
            background: #fff5f5;
            border: 1px solid #fecaca;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            color: #dc2626;
            flex-shrink: 0;
        }

        .doc-chip-chunks {
            font-size: 0.7rem;
            color: var(--text-light);
            font-weight: 500;
            background: var(--green-50);
            border: 1px solid var(--green-200);
            border-radius: 99px;
            padding: 1px 8px;
        }

        .doc-chip:hover {
            border-color: var(--accent);
            box-shadow: 0 4px 14px rgba(22,163,74,.12);
            transform: translateY(-2px);
        }

        /* ── EMPTY STATE ─────────────────────────────────────────── */
        .empty-state {
            background: linear-gradient(135deg, rgba(240,253,244,0.4) 0%, #ffffff 50%, rgba(255,247,237,0.4) 100%) !important;
            border: 1px solid var(--border-md) !important;
            border-radius: var(--r-lg) !important;
            padding: 44px 28px !important;
            text-align: center !important;
            box-shadow: var(--shadow-md) !important;
            animation: fadeIn 0.4s ease both !important;
            position: relative !important;
            overflow: hidden !important;
        }

        .empty-state::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #16a34a, #4ade80, #f97316, #16a34a);
            background-size: 300% 100%;
            animation: lineFlow 4s linear infinite;
        }

        @keyframes fadeIn { from{opacity:0} to{opacity:1} }

        .empty-state-icon {
            width: 60px; height: 60px;
            border-radius: 18px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            animation: iconFloat 3s ease-in-out infinite;
        }

        @keyframes iconFloat {
            0%,100% { transform: translateY(0); }
            50%      { transform: translateY(-8px); }
        }

        .empty-state-icon.green {
            background: var(--green-50);
            border: 1px solid var(--green-200);
            color: var(--green-600);
        }

        .empty-state-icon.orange {
            background: var(--orange-50);
            border: 1px solid #fed7aa;
            color: var(--orange-600);
        }

        .empty-state b {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-dark) !important;
            display: block;
            margin-bottom: 7px;
        }

        .empty-state p {
            color: var(--text-muted) !important;
            font-size: 0.88rem;
            margin: 0;
            line-height: 1.6;
        }

        /* ── FEATURE CARDS ───────────────────────────────────────── */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 20px;
        }

        .feature-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: var(--r-lg);
            padding: 22px 18px;
            text-align: center;
            box-shadow: var(--shadow-sm);
            transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
            animation: cardUp 0.6s ease both;
        }

        .feature-card:nth-child(1) { animation-delay: 0.1s; }
        .feature-card:nth-child(2) { animation-delay: 0.2s; }
        .feature-card:nth-child(3) { animation-delay: 0.3s; }

        .feature-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-xl);
            border-color: var(--border-md);
        }

        .fc-icon {
            width: 48px; height: 48px;
            border-radius: 14px;
            margin: 0 auto 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
        }

        .fc-icon.green  { background: var(--green-50);  border: 1px solid var(--green-200);  color: var(--green-600); }
        .fc-icon.orange { background: var(--orange-50); border: 1px solid #fed7aa; color: var(--orange-600); }
        .fc-icon.teal   { background: #f0fdfa; border: 1px solid #99f6e4; color: #0d9488; }

        .fc-title {
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--text-dark) !important;
            margin-bottom: 5px;
        }

        .fc-desc {
            font-size: 0.76rem;
            color: var(--text-muted) !important;
            line-height: 1.55;
        }

        /* ── CONVERSATION SECTION HEADER ─────────────────────────── */
        .conv-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0 8px;
            margin-top: 4px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 12px;
        }

        .conv-header-icon {
            width: 30px; height: 30px;
            border-radius: 9px;
            background: var(--green-50);
            border: 1px solid var(--green-200);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            color: var(--green-600);
        }

        .conv-header span {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--text-dark) !important;
        }

        /* ── UPLOAD HINT ─────────────────────────────────────────── */
        .upload-hint {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 10px;
            padding: 9px 14px;
            border-radius: var(--r-md);
            background: #f0fdf4;
            border: 1px solid #d1fae5;
            font-size: 0.78rem;
            color: #166534;
        }

        /* ── DANGER DELETE BUTTON ─────────────────────────────────── */
        /* Streamlit renders button text as aria-label — target it precisely */
        button[aria-label="🗑 Delete"],
        button[aria-label="\1F5D1 Delete"] {
            background-color: #fee2e2 !important;
            background: #fee2e2 !important;
            color: #b91c1c !important;
            border: 2px solid #fca5a5 !important;
            border-radius: 10px !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            min-height: 36px !important;
            transition: all 0.2s ease !important;
        }
        button[aria-label="🗑 Delete"] p,
        button[aria-label="🗑 Delete"] span,
        button[aria-label="🗑 Delete"] * {
            color: #b91c1c !important;
            font-weight: 700 !important;
        }
        button[aria-label="🗑 Delete"]:hover {
            background-color: #fca5a5 !important;
            background: #fca5a5 !important;
            border-color: #ef4444 !important;
            color: #7f1d1d !important;
            box-shadow: 0 4px 14px rgba(220,38,38,0.25) !important;
            transform: translateY(-1px) !important;
        }
        button[aria-label="🗑 Delete"]:hover * {
            color: #7f1d1d !important;
        }

        /* Remove dark background on ANY column block in the header area */
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div:first-child {
            background: transparent !important;
        }

        /* ══════════════════════════════════════════════════════════
           CHAT INPUT — clean pill, green send button, fixed bottom
           ══════════════════════════════════════════════════════════ */

        /* Wipe decorations off the sticky-bottom wrapper */
        div[data-testid="stBottom"],
        div[data-testid="stBottom"] > div,
        div[data-testid="stBottom"] > div > div,
        div[data-testid="stBottom"] > div > div > div {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
            padding: 0 !important;
        }

        /* ══════════════════════════════════════════════════════════
           CHAT INPUT WIDGET — CLEAN SINGLE GREEN SEND BUTTON
           ══════════════════════════════════════════════════════════ */

        div[data-testid="stBottom"] {
            background: linear-gradient(180deg, rgba(248,255,254,0) 0%, #f8fffe 40%) !important;
            padding: 12px 20px 16px !important;
        }

        /* Outer pill container */
        div[data-testid="stChatInput"] {
            max-width: 1160px !important;
            margin: 0 auto !important;
            background: #ffffff !important;
            border: 2px solid #16a34a !important;
            border-radius: 60px !important;
            box-shadow: 0 6px 24px rgba(22, 163, 74, 0.14) !important;
            min-height: 54px !important;
            padding: 4px 6px 4px 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        div[data-testid="stChatInput"]:focus-within {
            border-color: #15803d !important;
            box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.18), 0 8px 28px rgba(22, 163, 74, 0.18) !important;
        }

        /* Reset inner BaseWeb wrapper containers */
        div[data-testid="stChatInput"] > div,
        div[data-testid="stChatInput"] [data-baseweb="textarea"],
        div[data-testid="stChatInput"] [data-baseweb="base-input"] {
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            flex: 1 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* Ensure submit button wrapper is ALWAYS visible */
        [data-testid="stChatInputSubmitButton"],
        div[data-testid="stChatInputSubmitButton"],
        button[data-testid="stChatInputSubmitButton"] {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            align-items: center !important;
            justify-content: center !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Textarea input styling */
        div[data-testid="stChatInput"] textarea {
            color: #0f2318 !important;
            font-weight: 500 !important;
            font-size: 0.98rem !important;
            opacity: 1 !important;
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            min-height: 40px !important;
            padding: 8px 10px 8px 0 !important;
            line-height: 1.4 !important;
            caret-color: #16a34a !important;
            flex: 1 !important;
        }

        div[data-testid="stChatInput"] textarea::placeholder {
            color: #52796f !important;
            opacity: 0.9 !important;
        }

        /* ── SINGLE GREEN SEND BUTTON (FAR RIGHT EDGE) ────────────── */
        div[data-testid="stChatInput"] button,
        [data-testid="stChatInputSubmitButton"] button,
        button[data-testid="stChatInputSubmitButton"] {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            visibility: visible !important;
            opacity: 1 !important;
            background: #16a34a !important;
            background-color: #16a34a !important;
            background-image: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            color: #ffffff !important;
            fill: #ffffff !important;
            border: none !important;
            border-radius: 50% !important;
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            min-height: 36px !important;
            max-width: 36px !important;
            max-height: 36px !important;
            margin: 0 4px 0 auto !important;
            padding: 0 !important;
            flex-shrink: 0 !important;
            box-shadow: 0 4px 14px rgba(22, 163, 74, 0.4) !important;
            transition: all 0.18s ease !important;
            cursor: pointer !important;
            position: relative !important;
        }

        /* Visible Arrow Icon (in case SVG is missing/hidden by Streamlit) */
        div[data-testid="stChatInput"] button::before,
        button[data-testid="stChatInputSubmitButton"]::before {
            content: "➔" !important;
            font-size: 1.1rem !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            line-height: 1 !important;
            display: inline-block !important;
            visibility: visible !important;
        }

        /* If SVG exists inside button, hide the text arrow fallback */
        div[data-testid="stChatInput"] button:has(svg)::before,
        button[data-testid="stChatInputSubmitButton"]:has(svg)::before {
            display: none !important;
        }

        /* Button hover */
        div[data-testid="stChatInput"] button:hover,
        button[data-testid="stChatInputSubmitButton"]:hover {
            background: #22c55e !important;
            background-color: #22c55e !important;
            background-image: linear-gradient(135deg, #4ade80 0%, #22c55e 100%) !important;
            transform: scale(1.08) !important;
            box-shadow: 0 6px 20px rgba(22, 163, 74, 0.5) !important;
        }

        /* Disabled state override */
        div[data-testid="stChatInput"] button:disabled,
        div[data-testid="stChatInput"] button[disabled],
        button[data-testid="stChatInputSubmitButton"]:disabled {
            display: inline-flex !important;
            visibility: visible !important;
            opacity: 0.85 !important;
            background: #16a34a !important;
            background-color: #16a34a !important;
            background-image: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
            color: #ffffff !important;
            fill: #ffffff !important;
            border: none !important;
            cursor: pointer !important;
        }

        /* Send icon inside button */
        div[data-testid="stChatInput"] button svg,
        div[data-testid="stChatInput"] button svg path,
        div[data-testid="stChatInput"] button svg g,
        button[data-testid="stChatInputSubmitButton"] svg {
            width: 18px !important;
            height: 18px !important;
            fill: #ffffff !important;
            stroke: #ffffff !important;
            color: #ffffff !important;
            visibility: visible !important;
            opacity: 1 !important;
            display: block !important;
        }

        /* Bottom padding so main content clears fixed bottom bar */
        .block-container {
            padding-bottom: 110px !important;
        }

        /* ── DANGER CARD ─────────────────────────────────────────── */
        .danger-card {
            background: #fff5f5;
            border: 1.5px solid #fecaca;
            border-radius: var(--r-xl);
            padding: 28px 32px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }

        .danger-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #ef4444, #f97316);
        }

        .danger-card h1 {
            font-size: 1.7rem;
            font-weight: 800;
            color: #991b1b !important;
            margin: 0 0 10px;
        }

        .danger-card p { color: #7f1d1d !important; line-height: 1.6; }

        /* ── TOAST ───────────────────────────────────────────────── */
        [data-testid="stToast"] {
            background: #fff !important;
            border: 1px solid var(--border-md) !important;
            border-radius: var(--r-md) !important;
            color: var(--text-dark) !important;
            box-shadow: var(--shadow-lg) !important;
        }

        /* ── SPINNER ─────────────────────────────────────────────── */
        .stSpinner > div {
            border-top-color: var(--green-500) !important;
        }

        /* ── TIME BADGE ──────────────────────────────────────────── */
        .time-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--orange-50);
            border: 1px solid #fed7aa;
            border-radius: 99px;
            padding: 5px 12px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--orange-600);
        }

        /* ── RESPONSIVE ──────────────────────────────────────────── */
        @media (max-width: 768px) {
            .metric-grid  { grid-template-columns: 1fr; }
            .feature-grid { grid-template-columns: 1fr; }
            .hero-card h1 { font-size: 1.6rem; }
            .block-container { padding-left: 0.75rem; padding-right: 0.75rem; }
            .app-shell { max-width: 100%; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def api(
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
            "The backend is still waiting on Azure. Large PDFs can take a few minutes; please retry after it finishes."
        ) from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Backend not reachable at {BACKEND_API_URL}. Start FastAPI first.") from exc

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
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=ZoneInfo("UTC"))
        local = parsed.astimezone(INDIA_TZ)
        # e.g. "Mon, 14 Aug · 12:45 PM"
        return local.strftime("%a, %d %b · %I:%M %p")
    except ValueError:
        return value


def now_str() -> str:
    """Current local time string — called fresh every render so it stays current."""
    return datetime.now(INDIA_TZ).strftime("%I:%M %p · %d %b %Y")


def sid(value: str) -> str:
    return value[:8]


def safe(text: str) -> str:
    return html.escape(text or "")


def total_chunks(documents: list[dict[str, Any]]) -> int:
    return sum(int(doc.get("chunks_indexed") or 0) for doc in documents)


def greeting() -> str:
    hour = datetime.now(INDIA_TZ).hour
    if hour < 12:
        return "Good morning"
    if hour < 17:
        return "Good afternoon"
    return "Good evening"


def greeting_icon_html() -> str:
    """Emoji-based greeting icon — works without any CDN."""
    hour = datetime.now(INDIA_TZ).hour
    if hour < 12:
        return '🌅'
    if hour < 17:
        return '☀️'
    return '🌙'


@st.cache_data(ttl=6, show_spinner=False)
def get_sessions_cached() -> list[dict[str, Any]]:
    return api("GET", "/sessions", timeout=FAST_TIMEOUT)


def clear_sessions_cache() -> None:
    get_sessions_cached.clear()


def get_detail(session_id: str) -> dict[str, Any]:
    return api("GET", f"/sessions/{session_id}", timeout=DETAIL_TIMEOUT)


def create_chat() -> dict[str, Any]:
    clear_sessions_cache()
    return api("POST", "/sessions", timeout=FAST_TIMEOUT)


def delete_chat(session_id: str) -> dict[str, Any]:
    clear_sessions_cache()
    return api("DELETE", f"/sessions/{session_id}", timeout=DELETE_TIMEOUT)


def upload_pdf(session_id: str, file: Any) -> dict[str, Any]:
    return api(
        "POST",
        f"/sessions/{session_id}/upload",
        files={"file": (file.name, file.getvalue(), "application/pdf")},
        timeout=UPLOAD_TIMEOUT,
    )


def ask(session_id: str, question: str) -> dict[str, Any]:
    return api(
        "POST",
        f"/sessions/{session_id}/chat",
        json={"question": question},
        timeout=CHAT_TIMEOUT,
    )


def rename_session(session_id: str, title: str) -> None:
    """Patches the session title in the backend."""
    api(
        "PATCH",
        f"/sessions/{session_id}/title",
        json={"title": title},
        timeout=FAST_TIMEOUT,
    )


@st.cache_data(ttl=300, show_spinner=False)
def get_model_info() -> dict:
    """Fetches model deployment names from the backend (cached 5 min)."""
    try:
        return api("GET", "/health/info", timeout=FAST_TIMEOUT)
    except Exception:
        return {"chat_model": "—", "embedding_model": "—", "search_index": "—"}


def init() -> None:
    st.session_state.setdefault("session_id", None)
    st.session_state.setdefault("detail", None)
    st.session_state.setdefault("confirm_delete", False)
    st.session_state.setdefault("delete_target", None)
    st.session_state.setdefault("delete_target_title", None)
    st.session_state.setdefault("theme", "light")


def load_chat(session_id: str) -> None:
    st.session_state.session_id = session_id
    st.session_state.detail = get_detail(session_id)
    st.session_state.confirm_delete = False


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def sidebar() -> None:
    with st.sidebar:
        # Brand — leaf SVG logo
        st.markdown(
            """
            <div class="sb-brand">
                <div class="sb-logo">
                  <!-- Leaf + spring icon for DocSpring -->
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 22C12 22 4 16 4 9a8 8 0 0 1 16 0c0 7-8 13-8 13z"
                          fill="#ffffff" fill-opacity="0.9"/>
                    <path d="M12 22 L12 9" stroke="#16a34a" stroke-width="1.5"
                          stroke-linecap="round" stroke-dasharray="2 2"/>
                    <circle cx="12" cy="9" r="2.5" fill="#f97316" fill-opacity="0.9"/>
                    <path d="M8 7 Q10 4 12 6 Q14 4 16 7"
                          stroke="#ffffff" stroke-width="1.2" fill="none" stroke-linecap="round"/>
                  </svg>
                </div>
                <h1 class="sb-title">DocSpring</h1>
                <p class="sb-sub">Azure RAG &nbsp;·&nbsp; Multi-PDF Chat</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            ":material/add_comment:  New Chat",
            type="primary",
            use_container_width=True,
            key="new-chat-btn",
        ):
            with st.spinner("Creating chat..."):
                session = create_chat()
                load_chat(session["session_id"])
                st.rerun()

        st.divider()

        # Section label
        st.markdown(
            """<div style="display:flex;align-items:center;gap:7px;margin-bottom:10px;">
                   <svg width="13" height="13" viewBox="0 0 24 24" fill="none"
                        stroke="#16a34a" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                     <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                   </svg>
                   <span style="font-size:0.72rem;font-weight:700;color:#84a98c;
                                text-transform:uppercase;letter-spacing:.08em;">Saved Chats</span>
               </div>""",
            unsafe_allow_html=True,
        )

        try:
            sessions = get_sessions_cached()
        except RuntimeError as exc:
            st.error(str(exc))
            return

        if not sessions:
            st.markdown(
                """<div style="text-align:center;padding:20px 8px;color:#84a98c;font-size:.81rem;
                              background:#f0fdf4;border-radius:12px;border:1px dashed #bbf7d0;">
                       <svg width="26" height="26" viewBox="0 0 24 24" fill="none"
                            stroke="#84a98c" stroke-width="1.5" stroke-linecap="round"
                            style="display:block;margin:0 auto 8px;opacity:.6;">
                         <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                       </svg>
                       No chats yet.<br/>Start a new one above!
                   </div>""",
                unsafe_allow_html=True,
            )
            return

        for session in sessions:
            session_id = session["session_id"]
            active = session_id == st.session_state.session_id
            title  = session.get("title") or "New chat"
            count  = session.get("document_count", 0)
            label  = f"{'▶  ' if active else ''}{title[:26]}"

            if st.button(label, key=f"open-{session_id}", use_container_width=True):
                with st.spinner("Opening..."):
                    load_chat(session_id)
                    st.rerun()

            doc_svg = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
            dot_html = '<span class="active-dot"></span>' if active else '<span class="idle-dot"></span>'
            st.markdown(
                f'<div class="session-meta">'
                f'{dot_html}'
                f'{doc_svg}'
                f'&nbsp;{count} PDF{"s" if count != 1 else ""}'
                f'&nbsp;·&nbsp;{fmt_date(session.get("updated_at"))}'
                f'</div>',
                unsafe_allow_html=True,
            )

        # Footer
        st.divider()
        cloud_svg = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:3px;"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>'
        clock_svg = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:3px;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
        st.markdown(
            f"""<div style="text-align:center;padding:4px 0;font-size:.67rem;color:#84a98c;">
                   {cloud_svg} Powered by Azure AI Services
                   <br/>
                   <span class="time-badge" style="margin-top:6px;display:inline-flex;align-items:center;gap:4px;">
                     {clock_svg} {now_str()}
                   </span>
               </div>""",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════════════════════
#  LANDING
# ═══════════════════════════════════════════════════════════════════════════════
def landing() -> None:
    g_icon = greeting_icon_html()
    g_text = greeting()

    st.markdown('<div class="app-shell">', unsafe_allow_html=True)
    upload_svg = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'
    search_svg = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
    gpt_svg    = '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#0d9488" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c-4-4-6-8-6-12a6 6 0 0 1 12 0c0 4-2 8-6 12z"/><circle cx="12" cy="10" r="2" fill="#0d9488"/></svg>'

    st.markdown(
        f"""
        <div class="hero-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;
                      gap:16px;flex-wrap:wrap;">
            <div style="flex:1;min-width:0;">
              <h1><span class="grad">DocSpring AI</span></h1>
              <p>
                Upload PDFs, keep them in sessions, and ask grounded questions
                across all documents — powered end-to-end by Azure AI.
              </p>
            </div>
            <div style="padding-top:6px;">
              <div class="status-badge">
                <span class="live-dot"></span>
                Ready for PDFs
              </div>
            </div>
          </div>
        </div>

        <div class="empty-state">
          <div class="empty-state-icon green" style="font-size:2rem;padding:14px;">
            {g_icon}
          </div>
          <b>{g_text} — welcome to DocSpring!</b>
          <p>Create a new chat from the sidebar, upload your PDFs, and start asking questions.</p>
        </div>

        <div class="feature-grid">
          <div class="feature-card">
            <div class="fc-icon green">{upload_svg}</div>
            <div class="fc-title">Multi-PDF Upload</div>
            <div class="fc-desc">Upload multiple PDFs per session. All documents indexed together for cross-document queries.</div>
          </div>
          <div class="feature-card">
            <div class="fc-icon orange">{search_svg}</div>
            <div class="fc-title">Vector Search</div>
            <div class="fc-desc">Azure AI Search retrieves the most relevant chunks using semantic vector embeddings.</div>
          </div>
          <div class="feature-card">
            <div class="fc-icon teal">{gpt_svg}</div>
            <div class="fc-title">GPT-Powered Answers</div>
            <div class="fc-desc">GPT-4.1 Nano generates grounded, cited answers using only your document content.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  DELETE CONFIRMATION
# ═══════════════════════════════════════════════════════════════════════════════
def delete_confirmation() -> bool:
    if not st.session_state.get("confirm_delete") or not st.session_state.get("delete_target"):
        return False

    target_id    = st.session_state.delete_target
    target_title = st.session_state.get("delete_target_title") or "this chat"

    st.markdown('<div class="app-shell">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="danger-card">
          <h1>⚠️ Delete this chat?</h1>
          <p>
            This will permanently remove <b>{safe(target_title)}</b> from Azure Tables,
            Blob Storage, and Azure AI Search. All indexed chunks and messages will be lost.
          </p>
          <p style="font-weight:700;margin-top:8px;color:#991b1b !important;">
            🚫 This action cannot be undone from the app.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            ":material/delete_forever:  Yes, delete permanently",
            key=f"confirm-delete-{target_id}",
            type="primary",
            use_container_width=True,
        ):
            try:
                with st.spinner("Deleting chat from Azure..."):
                    result = delete_chat(target_id)
                st.toast(
                    f"Deleted {result['deleted_documents']} docs, "
                    f"{result['deleted_messages']} messages, "
                    f"{result['deleted_blobs']} blobs, "
                    f"{result['deleted_search_chunks']} search chunks.",
                    icon="🗑️",
                )
                if st.session_state.session_id == target_id:
                    st.session_state.session_id = None
                    st.session_state.detail = None
                st.session_state.confirm_delete = False
                st.session_state.delete_target = None
                st.session_state.delete_target_title = None
                clear_sessions_cache()
                st.rerun()
            except RuntimeError as exc:
                st.error(f"Delete failed: {exc}")
    with col2:
        if st.button(
            ":material/arrow_back:  Go back",
            key=f"cancel-delete-{target_id}",
            use_container_width=True,
        ):
            st.session_state.confirm_delete = False
            st.session_state.delete_target  = None
            st.session_state.delete_target_title = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    return True


# ═══════════════════════════════════════════════════════════════════════════════
#  HEADER  (metric cards aligned with CSS grid + align-items:stretch)
# ═══════════════════════════════════════════════════════════════════════════════
def header(detail: dict[str, Any]) -> None:
    session     = detail["session"]
    docs        = detail["documents"]
    msgs        = detail["messages"]
    title       = safe(session.get("title") or "New chat")
    chunk_count = total_chunks(docs)

    info        = get_model_info()
    chat_model  = info.get("chat_model",  "—")
    embed_model = info.get("embedding_model", "—")

    # SVG icons — inline, no CDN, always render
    chat_svg   = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
    key_svg    = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;"><circle cx="7" cy="17" r="4"/><path d="M10.85 13.15l7.57-7.57a2 2 0 0 1 2.83 0l.35.35a2 2 0 0 1 0 2.83L14 16"/></svg>'
    clock_svg  = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
    layer_svg  = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>'
    file_svg   = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>'
    msg_svg    = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f97316" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
    chunk_svg  = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0d9488" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>'
    trash_svg  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>'

    # ── Full-width hero card ──────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-card" style="margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;
                      gap:16px;flex-wrap:wrap;">
            <div style="flex:1;min-width:240px;">
              <h1 style="font-size:1.9rem;display:flex;align-items:center;gap:10px;">
                {chat_svg}
                <span class="grad">{title}</span>
              </h1>
              <p style="margin-top:8px;font-size:.82rem;display:flex;align-items:center;gap:10px;">
                <span style="display:flex;align-items:center;gap:5px;">
                  {clock_svg}&nbsp;{fmt_date(session.get("updated_at"))}
                </span>
              </p>
            </div>
            <div style="padding-top:4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
              <div style="display:flex;align-items:center;gap:8px;padding:6px 12px;
                          background:#f0fdf4;border-radius:20px;border:1px solid #d1fae5;
                          font-size:0.78rem;">
                <span style="width:7px;height:7px;background:#22c55e;border-radius:50%;
                             display:inline-block;animation:livePulse 1.6s ease infinite;"></span>
                <span style="color:#52796f;font-weight:600;">Chat:</span>
                <span style="background:#dcfce7;padding:2px 8px;border-radius:12px;
                             font-size:0.74rem;font-weight:700;color:#15803d;">{html.escape(chat_model)}</span>
                <span style="color:#52796f;font-weight:600;">Embed:</span>
                <span style="background:#dcfce7;padding:2px 8px;border-radius:12px;
                             font-size:0.74rem;font-weight:700;color:#15803d;">{html.escape(embed_model)}</span>
              </div>
              <div class="status-badge">
                <span class="live-dot"></span>
                {layer_svg}&nbsp;{chunk_count} chunks indexed
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Delete button — rightmost corner, separate row, red ──────────────
    _, del_col = st.columns([14, 1])
    with del_col:
        del_clicked = st.button(
            "Delete",
            key=f"hdr-del-{session['session_id']}",
            help="Delete this chat session",
            use_container_width=True,
        )
        # Inject JS to force red theme on this button by targeting its text
        st.components.v1.html(
            """<script>
            (function() {
                function styleDeleteBtn() {
                    var btns = window.parent.document.querySelectorAll('button');
                    btns.forEach(function(btn) {
                        var txt = btn.textContent || btn.innerText || '';
                        if (txt.trim() === 'Delete') {
                            btn.style.setProperty('background-color', '#fee2e2', 'important');
                            btn.style.setProperty('background', '#fee2e2', 'important');
                            btn.style.setProperty('color', '#b91c1c', 'important');
                            btn.style.setProperty('border', '2px solid #fca5a5', 'important');
                            btn.style.setProperty('border-radius', '10px', 'important');
                            btn.style.setProperty('font-weight', '700', 'important');
                        }
                    });
                }
                styleDeleteBtn();
                setTimeout(styleDeleteBtn, 300);
                setTimeout(styleDeleteBtn, 800);
            })();
            </script>""",
            height=0,
            scrolling=False,
        )
        if del_clicked:
            st.session_state.confirm_delete       = True
            st.session_state.delete_target        = session["session_id"]
            st.session_state.delete_target_title  = session.get("title") or "New chat"
            st.rerun()

    # ── Metric cards — all same height via CSS grid align-items:stretch ──
    st.markdown(
        f"""
        <div class="metric-grid">
          <div class="metric-card mc-green">
            <div class="mc-icon-wrap">{file_svg}</div>
            <span class="mc-label">Documents</span>
            <span class="mc-value">{len(docs)}</span>
          </div>
          <div class="metric-card mc-orange">
            <div class="mc-icon-wrap">{msg_svg}</div>
            <span class="mc-label">Messages</span>
            <span class="mc-value">{len(msgs)}</span>
          </div>
          <div class="metric-card mc-teal">
            <div class="mc-icon-wrap">{chunk_svg}</div>
            <span class="mc-label">Total Chunks</span>
            <span class="mc-value">{chunk_count}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  DOCUMENTS PANEL
# ═══════════════════════════════════════════════════════════════════════════════
def documents_panel(detail: dict[str, Any]) -> None:
    docs = detail["documents"]
    folder_svg = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#ea580c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/><line x1="12" y1="11" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>'
    if not docs:
        st.markdown(
            f"""<div class="empty-state">
                  <div class="empty-state-icon orange">{folder_svg}</div>
                  <b>{greeting()} — ready when you are</b>
                  <p>Upload one or more PDFs below to start asking grounded questions.</p>
                </div>""",
            unsafe_allow_html=True,
        )
        return

    pdf_chip_svg  = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'
    folder_hdr_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>'
    chips = "".join(
        f"""<span class="doc-chip">
              <span class="doc-chip-icon">{pdf_chip_svg}</span>
              <span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                {safe(doc["filename"])}
              </span>
              <span class="doc-chip-chunks">{doc["chunks_indexed"]} chunks</span>
            </span>"""
        for doc in docs
    )

    st.markdown(
        f"""<div class="info-card">
              <div class="info-card-header">
                <div class="card-icon-wrap">{folder_hdr_svg}</div>
                <span class="info-card-title">Indexed Documents</span>
                <span style="margin-left:auto;font-size:.73rem;font-weight:700;
                             color:var(--green-700);background:var(--green-50);
                             border:1px solid var(--green-200);border-radius:99px;padding:2px 10px;">
                  {len(docs)} PDF{"s" if len(docs) != 1 else ""}
                </span>
              </div>
              <div style="display:flex;flex-wrap:wrap;gap:2px;">{chips}</div>
            </div>""",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  UPLOAD PANEL
# ═══════════════════════════════════════════════════════════════════════════════
def upload_panel(session_id: str) -> None:
    with st.expander(":material/upload_file:  Upload PDFs", expanded=True):
        files = st.file_uploader(
            "Upload PDFs",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            help="Max 20 MB per PDF file.",
        )
        if not files:
            st.markdown(
                """<div class="upload-hint">
                     <span style="font-size:0.9rem;color:#16a34a;">⚡</span>
                     <span>PDFs are stored securely in <b>Azure Blob Storage</b> and indexed for RAG vector search.</span>
                   </div>""",
                unsafe_allow_html=True,
            )
            return

        if st.button(
            ":material/cloud_upload:  Upload & Index",
            type="primary",
            use_container_width=True,
        ):
            progress = st.progress(0, text="Starting upload...")
            successes: list[str] = []

            for index, file in enumerate(files, start=1):
                progress.progress(
                    (index - 1) / len(files),
                    text=f"Indexing {file.name}…",
                )
                try:
                    result = upload_pdf(session_id, file)
                    successes.append(f"{result['filename']} · {result['chunks_indexed']} chunks")
                except RuntimeError as exc:
                    st.error(f"Could not index {file.name}: {exc}")

            progress.progress(1.0, text="Upload complete ✓")
            if successes:
                st.success("Indexed: " + " | ".join(successes))
                clear_sessions_cache()
                load_chat(session_id)
                st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  MESSAGES
# ═══════════════════════════════════════════════════════════════════════════════
def messages(detail: dict[str, Any]) -> None:
    plane_svg = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>'
    conv_svg  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
    if not detail["messages"]:
        if detail["documents"]:
            st.markdown(
                f"""<div class="empty-state" style="margin-top:8px;">
                      <div class="empty-state-icon green">{plane_svg}</div>
                      <b>{greeting()} — ask your first question</b>
                      <p>Try: "Summarize the PDFs", "What are the main risks?", or "Compare both documents."</p>
                    </div>""",
                unsafe_allow_html=True,
            )
        return

    # Conversation header
    st.markdown(
        f"""<div class="conv-header">
             <div class="conv-header-icon">{conv_svg}</div>
             <span>Conversation</span>
           </div>""",
        unsafe_allow_html=True,
    )

    for msg in detail["messages"]:
        role = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(msg["message"])


# ═══════════════════════════════════════════════════════════════════════════════
#  CHAT INPUT
# ═══════════════════════════════════════════════════════════════════════════════
def chat_input(session_id: str) -> None:
    # ─ Chat input — styled entirely by the global css() block ─────────────────
    question = st.chat_input("Ask about your PDFs…")
    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    spinner_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round" style="animation:spin 1s linear infinite;display:inline;"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M12 2 A10 10 0 0 1 22 12"/></svg>'
    bookmark_svg = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:3px;"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>'
    
    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown(
            f"""<div style="display:flex;align-items:center;gap:9px;color:var(--text-muted);font-size:.88rem;">
                 {spinner_svg} Searching indexed chunks and preparing your answer…
               </div>""",
            unsafe_allow_html=True,
        )
        try:
            result = ask(session_id, question)
            box.markdown(result["answer"])

            sources_detail = result.get("sources_detail", [])
            if sources_detail:
                chips = []
                for sd in sources_detail:
                    fname = safe(sd.get("source_file", ""))
                    pg = sd.get("page_number", 0)
                    pg_label = f" · p.{pg}" if pg and pg > 0 else ""
                    chips.append(
                        f'<span class="source-chip">{bookmark_svg} {fname}{pg_label}</span>'
                    )
                st.markdown("".join(chips), unsafe_allow_html=True)
            elif result.get("sources"):
                source_html = "".join(
                    f'<span class="source-chip">{bookmark_svg} {safe(source)}</span>'
                    for source in result["sources"]
                )
                st.markdown(source_html, unsafe_allow_html=True)

            st.caption(
                f"Retrieved {result.get('retrieved_chunks', 0)} chunk(s) · "
                f"{now_str()}"
            )
            clear_sessions_cache()
            load_chat(session_id)
        except RuntimeError as exc:
            box.error(str(exc))
# ═══════════════════════════════════════════════════════════════════════════════
#  ACTIVE CHAT
# ═══════════════════════════════════════════════════════════════════════════════
def active_chat() -> None:
    if delete_confirmation():
        return

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

    st.markdown('<div class="app-shell">', unsafe_allow_html=True)
    header(detail)
    documents_panel(detail)
    upload_panel(session_id)
    messages(detail)
    st.markdown("</div>", unsafe_allow_html=True)
    chat_input(session_id)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    css()
    init()
    sidebar()
    active_chat()


if __name__ == "__main__":
    main()
