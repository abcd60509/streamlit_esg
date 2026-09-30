import streamlit as st


# =========================================================
# Theme Colors
# =========================================================
BG_COLOR = "#335c67"
LIGHT_COLOR = "#fff3b0"
ORANGE_COLOR = "#e09f3e"
RED_COLOR = "#9e2a2b"
DARK_RED_COLOR = "#540b0e"


# =========================================================
# Page Style
# =========================================================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BG_COLOR};
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
            border-radius: 15px;
            padding: 18px;
            border: 1px solid {RED_COLOR};
        }}

        [data-testid="stMetricLabel"] {{
            color: {LIGHT_COLOR} !important;
        }}

        [data-testid="stMetricValue"] {{
            color: white !important;
        }}

        [data-testid="stMetricDelta"] {{
            color: {ORANGE_COLOR} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Hero Section
# =========================================================
st.title("🏀 NBA Player Analytics")

st.subheader("用數據，看懂籃球")

st.write(
    """
    歡迎來到 NBA 球員資料分析平台！

    在 NBA 的比賽中，每一位球員都會產生大量的比賽數據。
    透過資料分析與視覺化，我們可以把這些數字轉換成
    更容易理解的資訊，進一步探索球員的比賽表現。
    """
)

st.divider()


# =========================================================
# Why NBA Data Analysis?
# =========================================================
st.header("📊 為什麼 NBA 資料分析很重要？")

st.write(
    """
    一場 NBA 比賽不只是比分而已。

    球員的得分、籃板、助攻、投籃命中率、三分命中率、
    上場時間等資料，都可以幫助我們從不同角度理解比賽。

    如果只看單一數字，很難完整描述一位球員。
    因此，我們可以利用資料分析將不同指標放在一起比較，
    找出資料之間的關係與趨勢。
    """
)


# =========================================================
# Key Metrics
# =========================================================
st.header("🏀 常見的 NBA 球員指標")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏀 PPG",
        value="Points",
        delta="平均得分"
    )

with col2:
    st.metric(
        label="🤝 APG",
        value="Assists",
        delta="平均助攻"
    )

with col3:
    st.metric(
        label="💪 RPG",
        value="Rebounds",
        delta="平均籃板"
    )

with col4:
    st.metric(
        label="🎯 FG%",
        value="Shooting",
        delta="投籃命中率"
    )


st.write("")


# =========================================================
# Three Important Concepts
# =========================================================
st.header("🔎 資料分析可以帶來什麼？")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader("🔍 了解球員")
        st.write(
            """
            透過得分、籃板、助攻等數據，
            可以更有系統地了解球員的比賽特色。
            """
        )

with col2:
    with st.container(border=True):
        st.subheader("📈 發現關係")
        st.write(
            """
            將不同統計資料放在一起，
            可以觀察不同指標之間可能存在的關係。
            """
        )

with col3:
    with st.container(border=True):
        st.subheader("💡 找到洞察")
        st.write(
            """
            利用資料視覺化將數字轉換成圖表，
            可以讓大量資料更容易被理解。
            """
        )


st.write("")


# =========================================================
# Data Analysis Process
# =========================================================
st.header("🧠 NBA 資料分析流程")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.subheader("01 📥")
        st.write("收集資料")
        st.caption("取得球員與比賽統計資料。")

with col2:
    with st.container(border=True):
        st.subheader("02 🧹")
        st.write("整理資料")
        st.caption("處理資料並整理成適合分析的格式。")

with col3:
    with st.container(border=True):
        st.subheader("03 📊")
        st.write("視覺化")
        st.caption("利用 Plotly 將資料轉換成互動式圖表。")

with col4:
    with st.container(border=True):
        st.subheader("04 🔎")
        st.write("探索資料")
        st.caption("從圖表中觀察球員之間的差異。")


st.divider()


# =========================================================
# Example
# =========================================================
st.header("🏀 一張圖可以看懂什麼？")

st.write(
    """
    例如，我們可以把球員的「平均得分 PPG」
    與「平均助攻 APG」放在同一張 Scatter Plot。

    這樣就能快速觀察：

    - 哪些球員具有較高的得分能力
    - 哪些球員具有較高的助攻能力
    - 不同位置的球員是否呈現不同的分布
    - 得分與助攻之間是否存在明顯的關係
    """
)


# =========================================================
# CTA
# =========================================================
st.header("🚀 開始探索 NBA 球員資料")

st.info(
    """
    準備好了嗎？

    請從左側選單進入 **「球員分析」**。

    在分析頁面中，你可以查看 NBA 球員樣板資料，
    並利用 Plotly Scatter Plot 互動探索球員的
    PPG、RPG、APG 與其他統計資料。
    """
)


# =========================================================
# Footer
# =========================================================
st.divider()

st.caption(
    "🏀 NBA Player Analytics · Streamlit + Plotly"
)