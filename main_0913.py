import streamlit as st
import pandas as pd
import base64

with st.sidebar:
    场景 = st.selectbox("请选择一个场景", ["跑步", "徒步", '骑行', '感冒发烧', "肠胃不适", '健身'])
    st.write('注：肠胃不适和感冒发烧未衡量With Whom')

# 读取Excel文件
original_data = pd.read_excel(f'{场景}result_df.xlsx')
original_data['Who'].fillna('未提及', inplace=True)

st.write(f'您所选的根场景为{场景}, 总文章数{len(original_data)}, 占比为{str(round(100 * len(original_data) / 60000,0))} %')

data = pd.read_excel(f'{场景}result_explode.xlsx', usecols=lambda x: 'Unnamed' not in x)
data.drop_duplicates(subset=["context", 'Where', 'Who', 'With Whom', 'How', 'When', 'Why'], inplace=True)
num_total_context = data.context.nunique()


##########################################################################################
st.header(f"{场景}场景最高的5W1H组合")
with st.sidebar:
    selected_columns = st.multiselect('选择要分析的列', ['Where', 'Who', 'With Whom', 'How', 'When', 'Why'],
                                      default=['Where', 'Who', 'With Whom', 'How', 'When', 'Why'])

# 选择要分析的列数，2-6列
num_selected_columns = len(selected_columns)

if num_selected_columns < 1:
    st.warning('请选择至少一列进行分析')
else:
    # 根据选择的列进行筛选
    filtered_df = data[selected_columns + ['context']]
    filtered_df = filtered_df.dropna()

    # 创建一个新列，表示每行选中的组合
    filtered_df['Combination'] = filtered_df[selected_columns].apply(lambda x: ' X '.join(x), axis=1)
    grouped_df = filtered_df.groupby(selected_columns)['context'].nunique().reset_index()
    grouped_df.columns = selected_columns + ['文章数']
    grouped_df['占根场景比例'] = grouped_df['文章数'] / num_total_context
    grouped_df = grouped_df.sort_values(by='占根场景比例', ascending=False)

    st.write('每个组合的文章数:')
    st.write(grouped_df)

    # 新增代码：添加下载DataFrame的选项
    if st.button('下载DataFrame'):
        csv = grouped_df.to_csv(index=True)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">点击这里下载DataFrame</a>'
        st.markdown(href, unsafe_allow_html=True)
##########################################################################################
