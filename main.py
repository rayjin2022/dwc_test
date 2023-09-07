import streamlit as st
import pandas as pd

# 读取Excel文件
@st.cache
def load_data(path):
    data = pd.read_excel(path)
    return data

original_data = load_data(path = '跑步result_df.xlsx')

st.header('1. top words example')


# 创建多选框来选择要分析的列
selected_columns = st.multiselect('选择要分析的列', ['Where', 'Who', 'With Whom', 'How', 'When', 'Why'], default=['Where', 'Who', 'With Whom', 'How', 'When', 'Why'])
# 初始化DataFrame以存储每个选中列的占比最高的5个词语和频次占比
top_words_data = pd.DataFrame(columns=['类型', '词语', '占比'])


# 2. 添加Where筛选框

data = load_data(path = '跑步result_explode.xlsx')
selected_where = st.multiselect("选择Where筛选条件", data['Where'].dropna().unique(),data['Where'].dropna().unique())
# 统计Where不为空且其他列不为空的文章占比
filtered_data = data[data['Where'].isin(selected_where)]
st.write(f"文章中Where不为空且其他列不为空的占比 (Where={selected_where}): {len(filtered_data) / len(data):.2%}")

# 计算每个选中列的占比最高的词语和频次占比
for col in selected_columns:
    not_null_records = len(filtered_data[filtered_data[col].notnull()])
    total_records = len(filtered_data)
    percentage = not_null_records / total_records

    # 计算每个列的占比最高的词语和频次占比
    top_word_counts = filtered_data[col].value_counts()
    top_words = top_word_counts.head(5)  # 获取占比最高的5个词语

    # 创建每个选中列的DataFrame并附加到主DataFrame
    top_words_df = pd.DataFrame({'类型': [col] * len(top_words), '词语': top_words.index,
                                 '占比': (top_words / total_records).apply(lambda x: f"{x:.0%}")})
    top_words_data = pd.concat([top_words_data, top_words_df])

# 显示每个选中列的占比最高的5个词语和频次占比
st.subheader('5W1H击中率占比最高词语:')
st.write(top_words_data)

# 计算选中列全部不为空的文章占比
all_columns_not_null = original_data[original_data[selected_columns].notnull().all(axis=1)]
all_columns_not_null_percentage = all_columns_not_null['context'].nunique() / data['context'].nunique()
st.write(f"选中列全部不为空的文章占比: {all_columns_not_null_percentage:.2%}")

# 计算每个组合列的占比最高的4W1H叠加组合
selected_columns_not_null = data[selected_columns].dropna()
top_combinations = selected_columns_not_null.apply('+'.join, axis=1).value_counts().reset_index()
top_combinations.columns = ['占比最高的5W1H叠加组合', '频次']
top_combinations['占比'] = [str(100*i/ len(original_data)) + '%' for i in top_combinations['频次']]


st.header('2. 5W1H击中率')

# 统计Where不为空的文章占比（不考虑其他列）
not_null_where_without_filter = len(data[data['Where'].notnull()])
where_percentage_without_filter = not_null_where_without_filter / len(data)
st.write(f"文章中Where不为空的占比 (无筛选): {where_percentage_without_filter:.2%}")

# 3. 满足Where,不为空，且Who不为空的文章占比
where_and_who = len(filtered_data[(filtered_data['Where'].notnull()) & (filtered_data['Who'].notnull())])
where_and_who_percentage = where_and_who / len(filtered_data)
st.write(f"文章中Where和Who都不为空的占比: {where_and_who_percentage:.2%}")
# 满足Where,不为空，且With Whom不为空的文章占比
where_and_ww = len(filtered_data[(filtered_data['Where'].notnull()) & (filtered_data['With Whom'].notnull())])
where_and_ww_percentage = where_and_ww / len(filtered_data)
st.write(f"文章中Where和With Whom都不为空的占比: {where_and_ww_percentage:.2%}")


# 4. 满足Where,不为空，且When不为空的文章占比
where_and_when = len(filtered_data[(filtered_data['Where'].notnull()) & (filtered_data['When'].notnull())])
where_and_when_percentage = where_and_when / len(filtered_data)
st.write(f"文章中Where和When都不为空的占比: {where_and_when_percentage:.2%}")

# 5. 满足Where,不为空，且How不为空的文章占比
where_and_how = len(filtered_data[(filtered_data['Where'].notnull()) & (filtered_data['How'].notnull())])
where_and_how_percentage = where_and_how / len(filtered_data)
st.write(f"文章中Where和How都不为空的占比: {where_and_how_percentage:.2%}")

# 6. 满足Where,不为空，且Why不为空的文章占比
where_and_why = len(filtered_data[(filtered_data['Where'].notnull()) & (filtered_data['Why'].notnull())])
where_and_why_percentage = where_and_why / len(filtered_data)
st.write(f"文章中Where和Why都不为空的占比: {where_and_why_percentage:.2%}")


# 计算每个组合列的占比最高的5W1H叠加组合
selected_columns = ['Where', 'Who', 'With Whom', 'How', 'When', 'Why']
selected_columns_not_null = filtered_data[selected_columns].dropna()
top_combinations = selected_columns_not_null.apply('+'.join, axis=1).value_counts().reset_index()
top_combinations.columns = ['占比最高的5W1H叠加组合', '频次']
top_combinations['占比'] = [str(round(i,2)) + '%' for i in top_combinations['频次'] / len(filtered_data) * 100]

# 去重
top_combinations = top_combinations.drop_duplicates()

# 显示占比最高的4W1H叠加组合
st.subheader('根据您选中的5W1H，占比最高的叠加组合:')
st.write(top_combinations)





st.header('3. 查看原文')
# 创建筛选器
selected_where = st.multiselect("选择Where筛选条件", data['Where'].dropna().unique(),default = '赛事')
selected_who = st.multiselect("选择Who筛选条件", data['Who'].dropna().unique(),default = '选手')
selected_how = st.multiselect("选择How筛选条件", data['How'].dropna().unique(),data['How'].dropna().unique())
selected_when = st.multiselect("选择When筛选条件", data['When'].dropna().unique(), data['When'].dropna().unique())
selected_why = st.multiselect("选择Why筛选条件", data['Why'].dropna().unique(), data['Why'].dropna().unique())

# 根据筛选条件，统计“文章占比”并展示符合条件的context
filtered_data = data[data['Where'].isin(selected_where)]

filtered_data = data[(data['Where'].isin(selected_where)) &
                     (data['Who'].isin(selected_who)) &
                     (data['How'].isin(selected_how)) &
                     (data['When'].isin(selected_when)) &
                     (data['Why'].isin(selected_why))]
filtered_percentage = len(filtered_data) / len(data)

filtered_data.drop_duplicates(subset=["context"], inplace=True)
filtered_data = filtered_data.reset_index(drop = True)

st.subheader("符合筛选条件的文章占比")
st.write(f"文章占比: {filtered_percentage:.2%}")

st.subheader("符合筛选条件的Context")
st.write(filtered_data['context'])