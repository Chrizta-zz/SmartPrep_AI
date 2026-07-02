"""
SmartPrep AI - UI Theme System
Clean, reusable, production-ready Streamlit UI components
"""

import re
import streamlit as st
import os


# =====================================================
# LOAD CSS
# =====================================================
_CSS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")


def _load_css() -> str:
    """
    Load and sanitize the global CSS file.
    Strips block comments (/* ... */) to prevent HTML parser issues
    when the CSS is embedded inside a <style> tag in st.markdown.
    """
    try:
        with open(_CSS_PATH, "r", encoding="utf-8") as f:
            raw = f.read()
        # Remove all CSS block comments — they can contain < > & that break HTML
        clean = re.sub(r'/\*.*?\*/', '', raw, flags=re.DOTALL)
        return clean
    except FileNotFoundError:
        return ""


# =====================================================
# APPLY THEME
# =====================================================
def apply_theme():
    """Inject global CSS + Google Font into Streamlit app."""

    # 1. Inject Google Font via <link> — separate call, no CSS mixing
    st.markdown(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap">',
        unsafe_allow_html=True
    )

    # 2. Inject CSS separately — comments already stripped by _load_css()
    css = _load_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# =====================================================
# HEADER
# =====================================================
def page_header(title, subtitle="", icon="🎓"):
    """Render styled hero header and apply theme."""
    apply_theme()

    subtitle_html = f'<p style="color:#8b9cc8;font-size:1rem;margin-top:6px;">{subtitle}</p>' if subtitle else ""

    st.markdown(
        f'<div class="sp-hero">'
        f'<h1>{icon} {title}</h1>'
        f'{subtitle_html}'
        f'</div>',
        unsafe_allow_html=True
    )


# =====================================================
# SECTION TITLE
# =====================================================
def section_title(text, icon=""):
    """Render a styled h2 section header."""
    st.markdown(
        f'<h2 style="margin-top:20px;margin-bottom:10px;">{icon} {text}</h2>',
        unsafe_allow_html=True
    )


# =====================================================
# DIVIDER
# =====================================================
def divider():
    """Render a thin teal divider."""
    st.markdown(
        '<hr style="border:none;border-top:1px solid rgba(0,212,204,0.2);margin:20px 0;">',
        unsafe_allow_html=True
    )


# =====================================================
# SUCCESS CARD
# =====================================================
def success_card(message: str):
    """Render a green tinted success message card."""
    st.markdown(
        f'<div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);'
        f'padding:12px 16px;border-radius:10px;color:#6ee7b7;font-weight:500;">✅ {message}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# AI PLAN CARD
# =====================================================
def ai_plan_card(plan_text="", time_slot="Not Set", sessions=None):
    """Render the AI study plan with time slot badges."""
    if sessions is None:
        sessions = []

    sessions_str = ", ".join(sessions) if sessions else "Flexible"

    st.markdown(
        f'<div class="sp-card">'
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px;">'
        f'<span class="sp-badge sp-badge-teal">🕒 {time_slot}</span>'
        f'<span class="sp-badge sp-badge-purple">⏱ {sessions_str}</span>'
        f'</div>'
        f'<hr style="border:none;border-top:1px solid rgba(0,212,204,0.15);margin:10px 0;">'
        f'</div>',
        unsafe_allow_html=True
    )

    if plan_text:
        st.markdown(plan_text)


# =====================================================
# GENERIC CARD
# =====================================================
def card(content_html: str):
    """Render a glassmorphism card with arbitrary HTML inside."""
    st.markdown(
        f'<div class="sp-card">{content_html}</div>',
        unsafe_allow_html=True
    )


# =====================================================
# BADGE (returns HTML string)
# =====================================================
def badge(text: str, color: str = "teal") -> str:
    """Return an HTML badge string. color: teal | purple | green | orange"""
    return f'<span class="sp-badge sp-badge-{color}">{text}</span>'

# =====================================================
# DASHBOARD METRIC CARD
# =====================================================
def dashboard_card(title, value, icon="📊"):

    st.markdown(
        f"""
        <div class="dashboard-card">
            <div class="dashboard-icon">{icon}</div>

            <div class="dashboard-title">
                {title}
            </div>

            <div class="dashboard-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# FEATURE CARD
# =====================================================
def feature_card(icon, title, description):

    st.markdown(
        f"""
        <div class="feature-card">

            <div class="feature-icon">
                {icon}
            </div>

            <div class="feature-title">
                {title}
            </div>

            <div class="feature-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# INFO CARD
# =====================================================
def info_card(title, body, icon="ℹ️"):

    st.markdown(
        f"""
        <div class="info-card">

            <div class="info-title">
                {icon} {title}
            </div>

            <div class="info-body">
                {body}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# AI RESPONSE CARD
# =====================================================
def ai_response_card(text):

    st.markdown(
        f"""
        <div class="ai-response-card">

            <div class="ai-title">
                🤖 SmartPrep AI
            </div>

            <hr>

            <div class="ai-body">

{text}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# EMPTY STATE
# =====================================================
def empty_state(title, subtitle, icon="📂"):

    st.markdown(
        f"""
        <div class="empty-state">

            <div class="empty-icon">
                {icon}
            </div>

            <div class="empty-title">
                {title}
            </div>

            <div class="empty-subtitle">
                {subtitle}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

def dashboard_card(title, value, icon):
    st.markdown(
        f"""
        <div class="dashboard-card">
            <div style="font-size:40px;">{icon}</div>
            <h3>{title}</h3>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


def feature_card(icon, title, description):
    st.markdown(
        f"""
        <div class="feature-card">
            <div style="font-size:45px;">{icon}</div>
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(title, text):
    st.markdown(
        f"""
        <div class="info-card">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )    


# =====================================================
# SECTION CARD
# =====================================================
def section_card(title, body):

    st.markdown(
        f"""
        <div class="section-card">

            <h3>{title}</h3>

            <p>{body}</p>

        </div>
        """,
        unsafe_allow_html=True
    )    

