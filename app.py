import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="ZAACO Cost Tracking System", layout="wide")
st.title("ZAACO价格表")

# ---------- 仓库里的 Excel 文件 ----------
excel_file = os.path.join(os.path.dirname(__file__), "cost.xlsx")

try:
    # 读取 Excel
    df = pd.read_excel(excel_file)

    st.subheader("Detail")

    # ---------- 独立搜索输入 ----------
    search_term = st.text_input("Enter model number to search", "")

    # ---------- 利润和汇率输入 ----------
    st.sidebar.header("价格计算设置     Price Calculation Setting")
    profit_percent = st.sidebar.number_input("利润率 margin (%)", min_value=0.0, value=15.0, step=0.5)
    exchange_rate = st.sidebar.number_input("汇率 currency(RMB → USD)", min_value=0.0, value=7.1, step=0.01)

    # ---------- 表格筛选 ----------
    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df.copy()

    # ---------- 新增价格列 ----------
    if 'RMB COST' in filtered_df.columns:
        filtered_df['USD PRICE'] = (filtered_df['RMB COST'] * (1 + profit_percent / 100) / exchange_rate).round(2)
    else:
        st.warning("Excel 表格中没有 'RMB COST' 列，请检查文件")

    st.dataframe(filtered_df)

except FileNotFoundError:
    st.error("cost.xlsx 文件不存在，请检查仓库是否包含此文件")
except ImportError as e:
    st.error("读取 Excel 文件失败，请检查依赖是否正确安装")
    st.write(str(e))
except Exception as e:
    st.error("程序运行出错，请查看详细日志")
    st.write(str(e))









