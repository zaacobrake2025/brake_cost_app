import streamlit as st
import pandas as pd

# 设置网页标题
st.set_page_config(page_title="刹车片成本查询系统", layout="wide")

# 读取 Excel 数据
@st.cache_data
def load_data():
    # 注意：请将 cost_data.xlsx 放在与 app.py 同一文件夹
    df = pd.read_excel("cost_data.xlsx", header=0)
    # 去掉空白行
    df = df.dropna(how="all")
    return df

df = load_data()

st.title("华莱刹车片成本查询系统")
st.markdown("在下方输入型号代码（如 `KD0079`）即可查看详细成本信息。")

# 搜索框
search_term = st.text_input("请输入型号代码：", "").strip().upper()

if search_term:
    results = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False)).any(axis=1)]
    if not results.empty:
        st.success(f"共找到 {len(results)} 条匹配结果：")
        st.dataframe(results, use_container_width=True)
    else:
        st.warning("未找到匹配型号，请检查输入是否正确。")
else:
    st.info("请输入型号代码进行查询。")

# 展示所有数据按钮
with st.expander("📋 查看全部数据表"):
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.caption("© 2025 刹车片成本查询工具 - ZAACO内部使用")
