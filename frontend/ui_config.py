ICON_MAP = {
    # Core
    "hospital": "hospital",
    "dashboard": "speedometer2",
    "ai": "robot",
    "appointments": "calendar-event",
    "patients": "person",
    "doctor": "person-badge",
    "lab": "flask",
    "reports": "file-earmark-text",
    "billing": "credit-card",
    "payment": "cash-coin",

    # Actions
    "add": "plus-circle",
    "edit": "pencil-square",
    "delete": "trash",
    "search": "search",

    # Status
    "success": "check-circle",
    "error": "x-circle",
    "pending": "clock",

    # System
    "settings": "gear",
    "logout": "box-arrow-right",
}

COLORS = {
    "primary": "#6366f1",
    "success": "#22c55e",
    "error": "#ef4444",
}

CARD_STYLE = "card"

def render_sidebar_header(title, icon_key, subtitle=None):
    import streamlit as st
    icon = ICON_MAP.get(icon_key, "circle")

    st.markdown(f"""
    <div style="
        display:flex;
        flex-direction:column;
        margin-bottom:15px;
    ">
        <div style="
            display:flex;
            align-items:center;
            gap:10px;
            font-size:20px;
            font-weight:700;
        ">
            <i class="bi bi-{icon}"></i>
            {title}
        </div>
        {f'<span style="font-size:12px; opacity:0.7;">{subtitle}</span>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_header(title, icon_key):
    """Backward-compatible header renderer used by dashboard pages."""
    render_sidebar_header(title, icon_key)