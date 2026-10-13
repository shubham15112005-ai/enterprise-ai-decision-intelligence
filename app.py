import streamlit as st

from database.init_db import (
    initialize_database,
)

from ui.dashboard import (
    render_dashboard,
)

from ui.chat import (
    render_chat,
)


print("Shubham Sharma 23051870")


st.set_page_config(
    page_title="Enterprise AI Decision Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Initialize database
# ---------------------------------------------------------

initialize_database()


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.title(
        "Enterprise AI"
    )

    st.caption(
        "Decision Intelligence Platform"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "AI Decision Assistant",
        ]
    )

    st.divider()

    st.caption(
        "Enterprise AI Decision Intelligence"
    )

    st.caption(
        "Version 1.0.0"
    )


# ---------------------------------------------------------
# Pages
# ---------------------------------------------------------

if page == "Executive Dashboard":

    render_dashboard()

else:

    st.title(
        "AI Decision Assistant"
    )

    st.caption(
        "Ask questions about your business data."
    )

    render_chat()