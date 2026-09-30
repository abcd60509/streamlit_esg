import streamlit as st


# =========================================================
# Page Config
# =========================================================
st.set_page_config(
    page_title="NBA Player Analytics",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# Theme
# =========================================================
BG_COLOR = "#335c67"
LIGHT_COLOR = "#fff3b0"
ORANGE_COLOR = "#e09f3e"
RED_COLOR = "#9e2a2b"
DARK_RED_COLOR = "#540b0e"


# =========================================================
# Global Style
# =========================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BG_COLOR};
        }}

        section[data-testid="stSidebar"] {{
            background-color: {DARK_RED_COLOR};
        }}

        section[data-testid="stSidebar"] * {{
            color: {LIGHT_COLOR};
        }}

        h1 {{
            color: {LIGHT_COLOR} !important;
        }}

        h2 {{
            color: {ORANGE_COLOR} !important;
        }}

        h3 {{
            color: {LIGHT_COLOR} !important;
        }}

        [data-testid="stMetric"] {{
            background-color: {DARK_RED_COLOR};
            border-radius: 12px;
            padding: 15px;
        }}

        [data-testid="stMetricLabel"] {{
            color: {LIGHT_COLOR} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: white !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Navigation
# =========================================================

# pages是一個變數  它是一個list
# 這個list裡面放了一個一個的st.Page(這個就是Streamlit原生元件的其中一種)
pages = [
    st.Page(
        "pages/home.py",       #把檔案路徑放進來
        title="首頁",    #導覽列上面顯示的文字 
        icon="🏠"       #文字前面的小小icon
    ),

    st.Page(
        "pages/page1.py",
        title="球員分析",
        icon="📊"
    ),

    st.Page(
            "pages/nba1.py",
            title="湖人隊球員分析",
            icon="📊"
        ),

    st.Page(
            "pages/nba2.py",
            title="各隊球員分析",
            icon="📊"
        ),
    st.Page(
            "pages/page2.py",
            title="球隊下載專區",
            icon="📊"
            )

]

# 這個就是在建立導航欄
pg = st.navigation(pages)


# =========================================================
# Run
# =========================================================
pg.run()