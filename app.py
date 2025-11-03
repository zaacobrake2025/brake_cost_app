import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="刹车片成本查询", layout="wide")
st.title("刹车片成本查询系统")

# ---------- 仓库里的 Excel 文件 ----------
excel_file = os.path.join(os.path.dirname(__file__), "cost.xlsx")

try:
    # 读取 Excel
    df = pd.read_excel(excel_file)
    
    st.subheader("成本表内容")
    
    # ---------- 搜索功能 ----------
    search_term = st.text_input("搜索型号或关键字", "")
    if search_term:
        filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = df

    st.dataframe(filtered_df)

    # ---------- 利润和汇率计算系统 ----------
    st.subheader("利润及汇率价格计算")

    col1, col2 = st.columns(2)
    with col1:
        profit_percent = st.number_input("请输入利润率 (%)", min_value=0.0, value=15.0, step=0.1)
    with col2:
        exchange_rate = st.number_input("请输入汇率", min_value=0.0, value=7.1, step=0.01)

    if st.button("计算价格"):
        # 假设成本列名为 "成本"（人民币）
        if "成本" not in filtered_df.columns:
            st.error('Excel 表格中必须包含 "成本" 列')
        else:
            result_df = filtered_df.copy()
            # 计算利润后人民币价格
            result_df["含利润价格（人民币）"] = result_df["成本"] * (1 + profit_percent / 100)
            # 换算美元价格
            result_df["美元价格"] = result_df["含利润价格（人民币）"] / exchange_rate
            st.subheader("计算结果")
            st.dataframe(result_df)

except FileNotFoundError:
    st.error("cost.xlsx 文件不存在，请检查仓库是否包含此文件")
except ImportError as e:
    st.error("读取 Excel 文件失败，请检查依赖是否正确安装")
    st.write(str(e))
except Exception as e:
    st.error("程序运行出错，请查看详细日志")
    st.write(str(e))

