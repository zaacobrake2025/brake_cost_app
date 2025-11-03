import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="刹车片成本查询", layout="wide")

st.title("刹车片成本查询系统")

# ---------- 读取仓库里的 Excel ----------
excel_file = os.path.join(os.path.dirname(__file__), "cost.xlsx")

try:
    df = pd.read_excel(excel_file)
    st.subheader("成本表内容")
    st.dataframe(df)
except FileNotFoundError:
    st.error("cost.xlsx 文件不存在，请检查仓库是否包含此文件")
except ImportError as e:
    st.error("读取 Excel 文件失败，请检查依赖是否正确安装")
    st.write(str(e))
except Exception as e:
    st.error("程序运行出错，请查看详细日志")
    st.write(str(e))
