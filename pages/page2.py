import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from io import BytesIO

# ==========================================
# Streamlit 頁面設定
# ==========================================
st.set_page_config(
    page_title="NBA 球員分析",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 NBA 球員數據分析")


# ==========================================
# 從 secrets.toml 連接 MySQL
# ==========================================
@st.cache_data
def load_data():

    conn = mysql.connector.connect(
        host=st.secrets["aiven"]["host"],
        port=st.secrets["aiven"]["port"],
        user=st.secrets["aiven"]["user"],
        password=st.secrets["aiven"]["password"],
        database=st.secrets["aiven"]["database"]
    )

    # 讀取三張資料表
    c = pd.read_sql("SELECT * FROM career_summaries", conn)
    p = pd.read_sql("SELECT * FROM players", conn)
    t = pd.read_sql("SELECT * FROM teams", conn)

    conn.close()

    # ==========================================
    # 合併資料
    # ==========================================

    # c + p：使用 personId
    cp = pd.merge(
        c,
        p,
        on="personId",
        how="inner"
    )

    # cp + t：使用 teamId
    cpt = pd.merge(
        cp,
        t,
        on="teamId",
        how="inner"
    )

    return cpt


# 載入資料
cpt = load_data()


# ==========================================
# 球隊下拉式選單
# ==========================================

# nickname 取 unique 值
team_options = sorted(
    cpt["nickname"]
    .dropna()
    .unique()
    .tolist()
)

selected_team = st.selectbox(
    "請選擇球隊",
    team_options
)


# ==========================================
# 根據選擇的球隊篩選資料
# ==========================================

filtered_data = cpt[
    cpt["nickname"] == selected_team
].copy()


st.subheader(f"📋 {selected_team} 球員資料")

st.dataframe(
    filtered_data,
    use_container_width=True
)


# ==========================================
# Excel 下載功能
# ==========================================

def convert_to_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="球員資料"
        )

    return output.getvalue()


excel_data = convert_to_excel(filtered_data)

st.download_button(
    label="📥 下載 Excel",
    data=excel_data,
    file_name=f"{selected_team}_球員資料.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# ==========================================
# 建立球員分類
# ==========================================

def player_group(row):

    if row["ppg"] > 20 and row["mpg"] > 24:
        return "PPG > 20、MPG > 24"

    elif row["ppg"] <= 20 and row["mpg"] > 24:
        return "PPG ≤ 20、MPG > 24"

    else:
        return "其他"


filtered_data["球員分類"] = filtered_data.apply(
    player_group,
    axis=1
)


# ==========================================
# Plotly Scatter 散佈圖
# ==========================================

fig = px.scatter(
    filtered_data,
    x="mpg",
    y="ppg",

    color="球員分類",

    color_discrete_map={
        "PPG > 20、MPG > 24": "red",
        "PPG ≤ 20、MPG > 24": "purple",
        "其他": "gray"
    },

    hover_data=[
        "temporaryDisplayName",
        "pos",
        "mpg",
        "ppg"
    ],

    title=f"{selected_team} 球員 MPG vs PPG"
)


# ==========================================
# 水平線：PPG = 20
# ==========================================

fig.add_hline(
    y=20,
    line_dash="dash",
    line_color="white",
    annotation_text="PPG = 20"
)


# ==========================================
# 垂直線：MPG = 24
# ==========================================

fig.add_vline(
    x=24,
    line_dash="dash",
    line_color="black",
    annotation_text="MPG = 24"
)


# ==========================================
# 圖表版面
# ==========================================

fig.update_layout(
    xaxis_title="MPG（平均上場時間）",
    yaxis_title="PPG（平均得分）",
    legend_title="球員分類"
)


# 顯示圖表
st.plotly_chart(
    fig,
    use_container_width=True
)