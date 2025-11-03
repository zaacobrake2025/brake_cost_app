import streamlit as st
import pandas as pd
import os

st.title("刹车片成本查询")

excel_file = os.path.join(os.path.dirname(__file__), "cost.xlsx")

if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
    st.subheader("成本表内容")
    st.dataframe(df)
else:
    st.error("cost.xlsx 文件不存在，请检查仓库是否包含此文件")
