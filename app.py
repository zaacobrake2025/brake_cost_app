import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="华莱刹车片成本查询系统", layout="wide")
st.title("zaaco刹车片成本查询系统")

# ---------- 默认 Excel 文件（仓库中的） ----------
default_excel_file = os.path.join(os.path.dirname(__file__), "cost.xlsx")

# ---------- 上传区域 ----------
st.sidebar.header("📤 数据来源设置")
uploaded_file = st.sidebar.file_uploader("上传新的 成本Excel 文件（可选）", type=["xlsx"])

# 读取 Excel：优先使用上传文件，否则用默认仓库文件
if uploaded_file is not None:
    st.sidebar.success("✅ 使用已上传文件")
    df = pd.read_excel(uploaded_file)
else:
    st.sidebar.info("📂 目前默认10月22日的报价 cost.xlsx")
    df = pd.read_excel(default_excel_file)

# ---------- 利润和汇率设置 ----------
st.sidebar.header("💰 价格计算设置")
profit_percent = st.sidebar.number_input("利润率margin (%)", min_value=0.0, value=15.0, step=0.5)
exchange_rate = st.sidebar.number_input("汇率 currency(RMB → USD)", min_value=0.0, value=7.1, step=0.01)

# ---------- 搜索功能 ----------
search_term = st.text_input("🔍 搜索型号或关键字", "")

# ---------- 数据筛选 ----------
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df.copy()

# ---------- 新增计算列 ----------
if "RMB COST" in filtered_df.columns:
    filtered_df["USD PRICE"] = (filtered_df["RMB COST"] * (1 + profit_percent / 100) / exchange_rate).round(2)
else:
    st.warning("❗ Excel 表中未找到 'RMB COST' 列，请检查文件。")

# ---------- 显示结果 ----------
st.subheader("📊 成本表内容")
st.dataframe(filtered_df)

st.caption("💡 提示：可在侧边栏上传新 Excel 文件进行临时计算，刷新页面后将恢复默认文件。")












