import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# =========================
# Streamlit Page Config
# =========================
st.set_page_config(
    page_title="NBA Lakers Career Summary",
    page_icon="🏀",
    layout="wide"
)


# =========================
# MySQL Connection
# 使用 Streamlit secrets.toml
# =========================
@st.cache_resource
def get_connection():

    return mysql.connector.connect(
        host=st.secrets["aiven"]["host"],
        port=st.secrets["aiven"]["port"],
        user=st.secrets["aiven"]["user"],
        password=st.secrets["aiven"]["password"],
        database=st.secrets["aiven"]["database"]
    )


# =========================
# 讀取資料
# =========================
@st.cache_data
def load_data():

    conn = get_connection()

    # career_summaries
    c = pd.read_sql(
        "SELECT * FROM career_summaries",
        conn
    )

    # players
    p = pd.read_sql(
        "SELECT * FROM players",
        conn
    )

    # teams
    t = pd.read_sql(
        "SELECT * FROM teams",
        conn
    )

    conn.close()

    # =========================
    # c + p -> cp
    # =========================
    cp = pd.merge(
        c,
        p,
        on="personId",
        how="inner",
        suffixes=("_c", "_p")
    )

    # =========================
    # cp + t -> cpt
    # =========================
    cpt = pd.merge(
        cp,
        t,
        on="teamId",
        how="inner",
        suffixes=("", "_t")
    )

    return cpt


# =========================
# 分頁
# =========================
tab1, tab2 = st.tabs([
    "🏀 Lakers Scatter Plot",
    "📊 Data"
])


# =========================
# Page 1
# =========================
with tab1:

    st.title("🏀 Lakers Career Summary")

    try:
        cpt = load_data()

        # nickname = Lakers
        lakers = cpt[
            cpt["nickname"].astype(str).str.strip() == "Lakers"
        ].copy()

        # 確認必要欄位
        required_columns = [
            "mpg",
            "ppg",
            "temporaryDisplayName",
            "pos"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in lakers.columns
        ]

        if missing_columns:
            st.error(
                f"缺少必要欄位：{', '.join(missing_columns)}"
            )
            st.stop()

        # 確保 mpg / ppg 是數值
        lakers["mpg"] = pd.to_numeric(
            lakers["mpg"],
            errors="coerce"
        )

        lakers["ppg"] = pd.to_numeric(
            lakers["ppg"],
            errors="coerce"
        )

        lakers = lakers.dropna(
            subset=["mpg", "ppg"]
        )

        # =========================
        # 建立標註
        # =========================
        def get_label_color(row):

            if row["ppg"] > 20 and row["mpg"] > 24:
                return "red"

            elif row["ppg"] <= 20 and row["mpg"] > 24:
                return "purple"

            return "black"

        lakers["label_color"] = lakers.apply(
            get_label_color,
            axis=1
        )

        # 只有 MPG > 24 的資料才顯示文字
        lakers["label"] = lakers.apply(
            lambda row:
                row["temporaryDisplayName"]
                if row["mpg"] > 24
                else "",
            axis=1
        )

        # =========================
        # Plotly Scatter
        # =========================
        fig = px.scatter(
            lakers,
            x="mpg",
            y="ppg",
            text="label",
            color="label_color",
            color_discrete_map={
                "red": "red",
                "purple": "purple",
                "black": "gray"
            },
            hover_data=[
                "temporaryDisplayName",
                "pos"
            ],
            labels={
                "mpg": "MPG",
                "ppg": "PPG"
            },
            title="Lakers - MPG vs PPG"
        )

        # =========================
        # y = 20 水平紅色虛線
        # =========================
        fig.add_hline(
            y=20,
            line_dash="dash",
            line_color="red",
            line_width=2
        )

        # =========================
        # x = 24 垂直黑色虛線
        # =========================
        fig.add_vline(
            x=24,
            line_dash="dash",
            line_color="black",
            line_width=2
        )

        # =========================
        # 標註文字顏色
        # =========================
        for trace in fig.data:

            color = trace.marker.color

            if color == "red":
                trace.textfont = dict(color="red")

            elif color == "purple":
                trace.textfont = dict(color="purple")

        fig.update_traces(
            textposition="top center",
            marker=dict(
                size=10
            )
        )

        fig.update_layout(
            height=650,
            legend_title_text="Group",
            xaxis_title="MPG",
            yaxis_title="PPG"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =========================
        # 統計資訊
        # =========================
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Lakers Players",
            len(lakers)
        )

        col2.metric(
            "PPG > 20 & MPG > 24",
            len(
                lakers[
                    (lakers["ppg"] > 20)
                    & (lakers["mpg"] > 24)
                ]
            )
        )

        col3.metric(
            "PPG <= 20 & MPG > 24",
            len(
                lakers[
                    (lakers["ppg"] <= 20)
                    & (lakers["mpg"] > 24)
                ]
            )
        )

    except Exception as e:
        st.error(f"資料庫或資料處理發生錯誤：{e}")


# =========================
# Page 2
# =========================
with tab2:

    st.title("📊 Lakers Data")

    try:
        cpt = load_data()

        lakers = cpt[
            cpt["nickname"].astype(str).str.strip() == "Lakers"
        ].copy()

        st.dataframe(
            lakers,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.error(f"資料讀取失敗：{e}")
