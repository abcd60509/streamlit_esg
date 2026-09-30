import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# =========================
# Streamlit Page Config
# =========================
st.set_page_config(
    page_title="NBA Career Summary",
    page_icon="🏀",
    layout="wide",
)

st.title("🏀 NBA Career Summary")


# =========================
# MySQL Connection
# =========================
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host=st.secrets["aiven"]["host"],
        port=st.secrets["aiven"]["port"],
        user=st.secrets["aiven"]["user"],
        password=st.secrets["aiven"]["password"],
        database=st.secrets["aiven"]["database"]
    )

    try:
        # c = career_summaries
        c = pd.read_sql(
            "SELECT * FROM career_summaries",
            conn
        )

        # p = players
        p = pd.read_sql(
            "SELECT * FROM players",
            conn
        )

        # t = teams
        t = pd.read_sql(
            "SELECT * FROM teams",
            conn
        )

    finally:
        conn.close()

    # =========================
    # Merge
    # c + p -> cp
    # =========================
    cp = pd.merge(
        c,
        p,
        on="personId",
        how="inner",
        suffixes=("_c", "_p"),
    )

    # =========================
    # cp + t -> cpt
    # =========================
    cpt = pd.merge(
        cp,
        t,
        on="teamId",
        how="inner",
        suffixes=("", "_t"),
    )

    return cpt


# =========================
# Load Data
# =========================
try:
    cpt = load_data()
except Exception as e:
    st.error(f"資料庫連線或資料讀取失敗：{e}")
    st.stop()


# =========================
# Check Required Columns
# =========================
required_columns = [
    "nickname",
    "mpg",
    "ppg",
    "temporaryDisplayName",
    "pos",
]

missing_columns = [
    col for col in required_columns
    if col not in cpt.columns
]

if missing_columns:
    st.error(
        "資料缺少以下必要欄位："
        + ", ".join(missing_columns)
    )
    st.stop()


# =========================
# Create Tabs
# =========================
tab1, tab2 = st.tabs([
    "📊 Scatter Plot",
    "📋 Data",
])


# =========================
# Prepare Team Options
# =========================
nicknames = (
    cpt["nickname"]
    .dropna()
    .astype(str)
    .sort_values()
    .unique()
    .tolist()
)


# =========================
# Tab 1 - Scatter Plot
# =========================
with tab1:
    st.subheader("NBA Player Career Statistics")

    selected_nickname = st.selectbox(
        "選擇 Team",
        options=nicknames,
        index=0 if nicknames else None,
    )

    if selected_nickname:
        filtered_df = cpt[
            cpt["nickname"].astype(str) == selected_nickname
        ].copy()

        # mpg / ppg 轉成數字
        filtered_df["mpg"] = pd.to_numeric(
            filtered_df["mpg"],
            errors="coerce"
        )

        filtered_df["ppg"] = pd.to_numeric(
            filtered_df["ppg"],
            errors="coerce"
        )

        # 移除沒有 mpg / ppg 的資料
        filtered_df = filtered_df.dropna(
            subset=["mpg", "ppg"]
        )

        if filtered_df.empty:
            st.warning("此選項沒有可用的 mpg / ppg 資料。")
        else:

            # =========================
            # 建立標註顏色
            # =========================
            def get_color(row):
                if row["ppg"] > 20 and row["mpg"] > 24:
                    return "red"

                if row["ppg"] <= 20 and row["mpg"] > 24:
                    return "purple"

                return "blue"


            filtered_df["point_color"] = filtered_df.apply(
                get_color,
                axis=1
            )

            # =========================
            # Plotly Scatter
            # =========================
            fig = px.scatter(
                filtered_df,
                x="mpg",
                y="ppg",
                color="point_color",
                color_discrete_map={
                    "red": "red",
                    "purple": "purple",
                    "blue": "blue",
                },
                hover_data=[
                    "temporaryDisplayName",
                    "pos",
                ],
                labels={
                    "mpg": "MPG",
                    "ppg": "PPG",
                    "temporaryDisplayName": "Player",
                    "pos": "Position",
                    "point_color": "Category",
                },
                title=f"{selected_nickname} - MPG vs PPG",
            )

            # =========================
            # y = 20 水平紅色虛線
            # =========================
            fig.add_hline(
                y=20,
                line_dash="dash",
                line_color="red",
                line_width=2,
                annotation_text="PPG = 20",
                annotation_position="top right",
            )

            # =========================
            # x = 24 垂直黑色虛線
            # =========================
            fig.add_vline(
                x=24,
                line_dash="dash",
                line_color="black",
                line_width=2,
                annotation_text="MPG = 24",
                annotation_position="top right",
            )

            # =========================
            # 顯示 Player Name
            # =========================
            for _, row in filtered_df.iterrows():

                # y > 20 且 x > 24 -> 紅色
                if row["ppg"] > 20 and row["mpg"] > 24:
                    fig.add_annotation(
                        x=row["mpg"],
                        y=row["ppg"],
                        text=str(row["temporaryDisplayName"]),
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="red",
                        font=dict(
                            color="red",
                            size=11,
                        ),
                        bgcolor="rgba(255,255,255,0.7)",
                    )

                # y <= 20 且 x > 24 -> 紫色
                elif row["ppg"] <= 20 and row["mpg"] > 24:
                    fig.add_annotation(
                        x=row["mpg"],
                        y=row["ppg"],
                        text=str(row["temporaryDisplayName"]),
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="purple",
                        font=dict(
                            color="purple",
                            size=11,
                        ),
                        bgcolor="rgba(255,255,255,0.7)",
                    )

            # =========================
            # Layout
            # =========================
            fig.update_layout(
                height=700,
                xaxis_title="MPG",
                yaxis_title="PPG",
                legend_title="Category",
                hovermode="closest",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

            # =========================
            # Statistics
            # =========================
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Players",
                    len(filtered_df)
                )

            with col2:
                st.metric(
                    "Average MPG",
                    f"{filtered_df['mpg'].mean():.2f}"
                )

            with col3:
                st.metric(
                    "Average PPG",
                    f"{filtered_df['ppg'].mean():.2f}"
                )


# =========================
# Tab 2 - Data
# =========================
with tab2:
    st.subheader("Filtered Data")

    selected_nickname_data = st.selectbox(
        "選擇 Team",
        options=nicknames,
        index=0 if nicknames else None,
        key="data_team_select",
    )

    if selected_nickname_data:
        filtered_data = cpt[
            cpt["nickname"].astype(str)
            == selected_nickname_data
        ].copy()

        st.dataframe(
            filtered_data,
            use_container_width=True,
            hide_index=True,
        )

        st.write(
            f"共 {len(filtered_data)} 筆資料"
        )
