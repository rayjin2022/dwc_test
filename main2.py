import streamlit as st
import pandas as pd

import streamlit as st

# 创建一个下拉框
with st.sidebar:
    场景 = st.selectbox("请选择一个场景", ["跑步", "徒步", '骑行', '感冒发烧', "肠胃不适", '健身'])
    st.write('注：肠胃不适和感冒发烧未衡量With Whom')

# 读取Excel文件
original_data = pd.read_excel(f'{场景}result_df.xlsx')
original_data['Who'].fillna('未提及', inplace=True)

st.write(f'您所选的根场景为{场景}, 占比为{str(100 * round(len(original_data) / 77512, 2))} %')

data = pd.read_excel(f'{场景}result_explode.xlsx')
data['Who'].fillna('未提及', inplace=True)

st.header('1. top words example')


top_words_data = pd.DataFrame(columns=['类型', '词语', '占比'])

with st.sidebar:
    selected_columns = st.multiselect('选择要分析的列', ['Where', 'Who', 'With Whom', 'How', 'When', 'Why'],
                                      default=['Where', 'Who', 'With Whom', 'How', 'When', 'Why'])
    # 添加Where筛选框
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


# 去重

# 计算每个组合列的占比最高的5W1H叠加组合
selected_columns_not_null = filtered_data[selected_columns].dropna()
top_combinations = selected_columns_not_null.apply('+'.join, axis=1).value_counts().reset_index()
top_combinations.columns = ['占比最高的5W1H叠加组合', '频次']
top_combinations['占比'] = top_combinations['频次'].map(lambda x: f"{round(x / len(filtered_data) * 100, 2)}%")
top_combinations = top_combinations.drop_duplicates()
st.dataframe(top_combinations)


selected_combination = st.selectbox('选择你需要观察的组合', top_combinations['占比最高的5W1H叠加组合'].unique())

if st.button('生成原文'):
    # 将叠加组合拆分为各个值
    values = selected_combination.split('+')
    filtered_contexts = pd.DataFrame()

    # 使用条件筛选原文的context
    for column in selected_columns:
        filtered_context = filtered_data[filtered_data[column].isin(values)]['context']

        # 将匹配的context添加到结果DataFrame中
        filtered_contexts = pd.concat([filtered_contexts, filtered_context], ignore_index=True)

    filtered_context_output = filtered_contexts.drop_duplicates()
    st.dataframe(filtered_context_output)