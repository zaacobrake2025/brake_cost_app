import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="刹车片成本查询", layout="wide")
st.title("刹车片成本查询系统")

# ---------- 仓库里的 Excel ----------
excel_file = os.path.join(os.path.dirname(__file__), "cost.xlsx")

try:
    df = pd.read_excel(excel_file)
    
    st.subheader("成本表内容")

    # ---------- 用户输入利润率和汇率 ----------
    st.sidebar.header("计算参数")
    profit_percent = st.sidebar.number_input("利润率 (%)", min_value=0.0, value=15.0, step=1.0)
    exchange_rate = st.sidebar.number_input("汇率 (RMB → USD)", min_value=0.0, value=7.1, step=0.01)

    # ---------- 添加计算列 ----------
    if "Cost (RMB)" in df.columns:
        # 利润价格
        df["Price with Profit (RMB)"] = df["Cost (RMB)"] * (1 + profit_percent/100)
        # 汇率换算
        df["Price with Profit (USD)"] = df["Price with Profit (RMB)"] / exchange_rate
    else:
        st.warning("表格中没有 'Cost (RMB)' 列，请检查 Excel 列名是否正确")

    # ---------- 搜索功能 ----------
    search_term = st.text_input("搜索型号或关键字", "")
    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
        st.dataframe(filtered_df)
    else:
        st.dataframe(df)

except FileNotFoundError:
    st.error("cost.xlsx 文件不存在，请检查仓库是否包含此文件")
except ImportError as e:
    st.error("读取 Excel 文件失败，请检查依赖是否正确安装")
    st.write(str(e))
except Exception as e:
    st.error("程序运行出错，请查看详细日志")
    st.write(str(e))

