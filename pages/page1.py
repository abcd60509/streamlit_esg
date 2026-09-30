import streamlit as st
import pandas as pd
import plotly.express as px


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
# Page Title
# =========================================================
st.title("📊 NBA 球員分析")

st.write(
    """
    透過 NBA 球員統計資料，
    探索球員的得分、助攻與籃板表現。
    """
)


# =========================================================
# Sample Data
# =========================================================
data = {
    "Player": [
        "LeBron James",
        "Stephen Curry",
        "Nikola Jokic",
        "Luka Doncic",
        "Giannis Antetokounmpo",
        "Jayson Tatum",
        "Kevin Durant",
        "Anthony Edwards",
        "Shai Gilgeous-Alexander",
        "Ja Morant",
        "Trae Young",
        "Jimmy Butler"
    ],

    "Team": [
        "Lakers",
        "Warriors",
        "Nuggets",
        "Mavericks",
        "Bucks",
        "Celtics",
        "Suns",
        "Timberwolves",
        "Thunder",
        "Grizzlies",
        "Hawks",
        "Heat"
    ],

    "Position": [
        "SF",
        "PG",
        "C",
        "PG",
        "PF",
        "SF",
        "SF",
        "SG",
        "PG",
        "PG",
        "PG",
        "SF"
    ],

    "PPG": [
        25.7,
        26.4,
        29.6,
        32.4,
        30.4,
        27.2,
        28.1,
        25.9,
        31.0,
        25.1,
        26.7,
        21.4
    ],

    "RPG": [
        7.3,
        4.5,
        12.7,
        8.6,
        11.5,
        8.1,
        6.7,
        5.4,
        5.5,
        5.6,
        2.8,
        5.9
    ],

    "APG": [
        8.3,
        5.1,
        9.0,
        8.0,
        6.5,
        4.9,
        5.0,
        5.1,
        6.2,
        8.1,
        10.8,
        5.0
    ],

    "FG_PCT": [
        54.0,
        45.0,
        58.3,
        48.7,
        61.1,
        47.2,
        52.3,
        46.1,
        53.5,
        46.8,
        43.2,
        49.1
    ]
}

df = pd.DataFrame(data)


# =========================================================
# Sidebar Filters
# =========================================================
st.sidebar.header("🔎 資料篩選")

selected_positions = st.sidebar.multiselect(
    "選擇球員位置",
    options=sorted(df["Position"].unique()),
    default=sorted(df["Position"].unique())
)

min_ppg = st.sidebar.slider(
    "最低 PPG",
    min_value=float(df["PPG"].min()),
    max_value=float(df["PPG"].max()),
    value=float(df["PPG"].min()),
    step=0.5
)


# =========================================================
# Filter Data
# =========================================================
filtered_df = df[
    (df["Position"].isin(selected_positions))
    & (df["PPG"] >= min_ppg)
].copy()


# =========================================================
# Summary
# =========================================================
st.subheader("📌 資料摘要")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "球員數量",
        len(filtered_df)
    )

with col2:
    avg_ppg = (
        filtered_df["PPG"].mean()
        if not filtered_df.empty
        else 0
    )

    st.metric(
        "平均 PPG",
        f"{avg_ppg:.1f}"
    )

with col3:
    avg_rpg = (
        filtered_df["RPG"].mean()
        if not filtered_df.empty
        else 0
    )

    st.metric(
        "平均 RPG",
        f"{avg_rpg:.1f}"
    )

with col4:
    avg_apg = (
        filtered_df["APG"].mean()
        if not filtered_df.empty
        else 0
    )

    st.metric(
        "平均 APG",
        f"{avg_apg:.1f}"
    )


st.divider()


# =========================================================
# Scatter Plot
# =========================================================
st.subheader("🏀 PPG vs APG")

st.write(
    """
    X 軸代表平均得分（PPG），
    Y 軸代表平均助攻（APG），
    圓點大小代表平均籃板（RPG）。
    不同顏色代表不同球員位置。
    """
)


if not filtered_df.empty:

    fig = px.scatter(
        filtered_df,

        x="PPG",
        y="APG",

        size="RPG",

        color="Position",

        hover_name="Player",

        hover_data={
            "Team": True,
            "Position": True,
            "PPG": ":.1f",
            "RPG": ":.1f",
            "APG": ":.1f",
            "FG_PCT": ":.1f"
        },

        color_discrete_sequence=[
            ORANGE_COLOR,
            LIGHT_COLOR,
            RED_COLOR,
            "#6fa3a8",
            "#c96f5d"
        ],

        size_max=45,

        labels={
            "PPG": "平均得分 PPG",
            "APG": "平均助攻 APG",
            "RPG": "平均籃板 RPG",
            "Position": "位置"
        }
    )


    # -----------------------------------------------------
    # Plotly Theme
    # -----------------------------------------------------
    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=DARK_RED_COLOR,

        font=dict(
            color="white"
        ),

        title=dict(
            text="NBA Player Scoring vs Playmaking",
            font=dict(
                color=LIGHT_COLOR,
                size=22
            )
        ),

        xaxis=dict(
            title="平均得分 PPG",
            gridcolor="#52747d"
        ),

        yaxis=dict(
            title="平均助攻 APG",
            gridcolor="#52747d"
        ),

        legend=dict(
            title="球員位置"
        )
    )


    # -----------------------------------------------------
    # Display Chart
    # -----------------------------------------------------
    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.warning(
        "目前沒有符合篩選條件的球員，"
        "請調整左側的篩選條件。"
    )


# =========================================================
# Data Table
# =========================================================
st.divider()

st.subheader("📋 球員資料")

st.dataframe(
    filtered_df,

    use_container_width=True,

    hide_index=True,

    column_config={
        "Player": "球員",

        "Team": "球隊",

        "Position": "位置",

        "PPG": st.column_config.NumberColumn(
            "PPG",
            format="%.1f"
        ),

        "RPG": st.column_config.NumberColumn(
            "RPG",
            format="%.1f"
        ),

        "APG": st.column_config.NumberColumn(
            "APG",
            format="%.1f"
        ),

        "FG_PCT": st.column_config.NumberColumn(
            "FG%",
            format="%.1f"
        )
    }
)


# =========================================================
# Explanation
# =========================================================
st.divider()

with st.expander("📖 如何閱讀這張 Scatter Plot？"):

    st.write(
        """
        **X 軸：PPG（Points Per Game）**

        代表球員平均每場比賽的得分。

        **Y 軸：APG（Assists Per Game）**

        代表球員平均每場比賽的助攻。

        **圓點大小：RPG（Rebounds Per Game）**

        圓點越大，代表平均籃板數越高。

        **顏色：Position**

        不同顏色代表不同的球員位置。
        """
    )