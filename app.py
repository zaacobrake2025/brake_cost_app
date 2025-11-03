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
    
    # ---------- 独立搜索输入 ----------
    search_term = st.text_input("搜索型号或关键字", "")

    # 如果输入了搜索词，则筛选表格
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
