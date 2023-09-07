import streamlit as st
import pandas as pd

# 读取Excel文件
@st.cache
def load_data():
    data = pd.read_excel('data.xlsx')
    return data

data = load_data()


st.header('1. 4W1H击中率')

# 创建多选框来选择要分析的列
selected_columns = st.multiselect('选择要分析的列', ['Where', 'Who', 'How', 'When', 'Why'] , default=['Where', 'Who', 'How', 'When', 'Why'])

# 计算每个选中列不为空的占比
for col in selected_columns:
    not_null_records = len(data[data[col].notnull()])
    total_records = len(data)
    percentage = not_null_records / total_records
    st.write(f"您选中的{col}不为空的占比: {percentage:.2%}")

# 计算选中列全部不为空的文章占比
all_columns_not_null = data[data[selected_columns].notnull().all(axis=1)]
all_columns_not_null_percentage = len(all_columns_not_null) / len(data)
st.write(f"根据您选中的列，全部不为空的文章占比: {all_columns_not_null_percentage:.2%}")


# 第三个模块 - 根据筛选所选文章的占比
st.header('2. 所选文章的占比')
# 创建每个条件的下拉框
selected_where_3 = st.multiselect('选择筛选的"Where"列', data['Where'].unique(), default=data['Where'].unique())
selected_who_3 = st.multiselect('选择筛选的"Who"列', data['Who'].unique(), default=data['Who'].unique())
selected_how_3 = st.multiselect('选择筛选的"How"列', data['How'].unique(), default=data['How'].unique())
selected_when_3 = st.multiselect('选择筛选的"When"列', data['When'].unique(), default=data['When'].unique())
selected_why_3 = st.multiselect('选择筛选的"Why"列', data['Why'].unique(), default=data['Why'].unique())

# 根据筛选器的条件过滤数据
filtered_data_3 = data[data['Where'].isin(selected_where_3) &
                       data['Who'].isin(selected_who_3) &
                       data['How'].isin(selected_how_3) &
                       data['When'].isin(selected_when_3) &
                       data['Why'].isin(selected_why_3)]

# 计算筛选文章占比
filtered_percentage = len(filtered_data_3) / data['context'].nunique()

st.write(f"筛选文章占比: {filtered_percentage:.2%}")

# 展示符合条件的context
st.subheader('符合条件的context:')
st.write(filtered_data_3['context'].tolist())