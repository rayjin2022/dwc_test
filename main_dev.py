import streamlit as st
import pandas as pd
import base64

with st.sidebar:
    场景 = st.selectbox("请选择一个场景", ["跑步", "徒步", '骑行', '感冒发烧', "肠胃不适", '健身'])
    #st.write('注：肠胃不适和感冒发烧未衡量With Whom')

# 读取Excel文件
original_data = pd.read_excel(f'{场景}result_df.xlsx')
original_data['Who'].fillna('未提及', inplace=True)

st.write(f'您所选的根场景为{场景}, 总文章数{len(original_data)}, 占比为{str(round(100 * len(original_data) / 60000,0))} %')

data = pd.read_excel(f'{场景}result_explode.xlsx', usecols=lambda x: 'Unnamed' not in x)
data.drop_duplicates(subset=["context", 'Where', 'Who', 'With Whom', 'How', 'When', 'Why'], inplace=True)
num_total_context = data.context.nunique()





##########################################################################################
st.write('\n')
st.write('\n')
st.write('\n')
st.header(f"{场景}场景最高的5W1H组合")
with st.sidebar:
    selected_columns = st.multiselect('选择要分析的列', ['Where', 'Who', 'With Whom', 'How', 'When', 'Why'],
                                      default=['Where', 'Who', 'With Whom', 'How', 'When', 'Why'])
    selected_where = st.multiselect("选择Where筛选条件", data['Where'].dropna().unique(),
                                    data['Where'].dropna().unique())

# 选择要分析的列数，2-6列
num_selected_columns = len(selected_columns)

if num_selected_columns < 1:
    st.warning('请选择至少一列进行分析')
else:
    # 根据选择的列进行筛选
    filtered_df = data[selected_columns + ['context']]
    filtered_df = filtered_df[filtered_df['Where'].isin(selected_where)]
    filtered_df = filtered_df.dropna()

    # 创建一个新列，表示每行选中的组合
    filtered_df['Combination'] = filtered_df[selected_columns].apply(lambda x: ' X '.join(x), axis=1)
    grouped_df = filtered_df.groupby(selected_columns)['context'].nunique().reset_index()
    grouped_df.columns = selected_columns + ['文章数']
    grouped_df['占根场景比例'] = grouped_df['文章数'] / num_total_context
    grouped_df = grouped_df.sort_values(by='占根场景比例', ascending=False).reset_index(drop = True)

    st.write('每个组合的文章数:')
    st.dataframe(grouped_df.style.format({'占根场景比例': '{:.2%}'}))

    # 新增代码：添加下载DataFrame的选项
    if st.button('下载数据表'):
        csv = grouped_df.to_csv(index=True)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">点击这里继续下载</a>'
        st.markdown(href, unsafe_allow_html=True)
##########################################################################################






##########################################################################################
st.write('\n')
st.write('\n')
st.write('\n')
st.header("根据 5W1H 组合，查看显示对应的原文")

original_article = data[selected_columns + ['context']]

if num_selected_columns < 1:
    st.warning('请选择至少一列进行分析')
else:
    # 根据选择的列进行筛选
    original_article['5W1H_Combination'] = data[selected_columns].astype(str).apply(lambda x: '+'.join(x), axis=1)
    original_article.dropna(inplace = True)

    selected_combination = st.selectbox('选择5W1H的组合', original_article['5W1H_Combination'].unique(), 0)

    if selected_combination:
        filtered_articles = original_article[original_article['5W1H_Combination'] == selected_combination].reset_index(drop = True)
        filtered_articles.drop_duplicates(subset=["context", '5W1H_Combination'], inplace=True)
        st.dataframe(filtered_articles[['context','5W1H_Combination'] + selected_columns])

        # 新增代码：添加下载DataFrame的选项
        if st.button('下载原文数据表'):
            csv = filtered_articles.to_csv(index=True)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">点击这里继续下载</a>'
            st.markdown(href, unsafe_allow_html=True)

##########################################################################################







##########################################################################################
##########################################################################################






'''
##########################################################################################
st.header('选中5W1H高频词样例')
# 统计Where不为空且其他列不为空的文章占比
with st.sidebar:
    selected_where = st.multiselect("选择Where筛选条件", data['Where'].dropna().unique(), data['Where'].dropna().unique())

st.write('注意：根据Where的筛选条件，对应的筛选词语会发生变化')

top_words_data = pd.DataFrame(columns=['类型', '词语', '占比'])
filtered_data = data[data['Where'].isin(selected_where)]
st.write(f"文章中Where不为空且其他列不为空的占比 (Where={selected_where}): {len(filtered_data) / len(data):.2%}")

# 计算每个选中列的占比最高的词语和频次占比
for col in selected_columns:
    not_null_records = filtered_data[filtered_data[col].notnull()].context.nunique()
    total_records = num_total_context
    percentage = not_null_records / total_records

    # 计算每个列的占比最高的词语和对应唯一上下文数量
    top_words_counts = filtered_data.groupby(col)['context'].nunique()
    top_words_counts = top_words_counts.reset_index()
    top_words_counts = top_words_counts.rename(columns={'context': '唯一上下文数量'})
    top_words_counts = top_words_counts.sort_values(by='唯一上下文数量', ascending=False).head(5)

    # 创建每个选中列的DataFrame并附加到主DataFrame
    top_words_counts['类型'] = col
    top_words_counts['占比'] = top_words_counts['唯一上下文数量'] / total_records
    top_words_counts['占比'] = top_words_counts['占比'].apply(lambda x: f"{x:.0%}")

    top_words_data = pd.concat([top_words_data, top_words_counts])

# 显示每个选中列的占比最高的5个词语和频次占比
st.subheader('5W1H击中率占比最高词语:')
st.write(top_words_data)

# 计算选中列全部不为空的文章占比
all_columns_not_null = original_data[original_data[selected_columns].notnull().all(axis=1)]
all_columns_not_null_percentage = all_columns_not_null['context'].nunique() / data['context'].nunique()
st.write(f"选中列全部不为空的文章占比: {all_columns_not_null_percentage:.2%}")





st.header('2. 5W1H击中率')

# 统计Where不为空的文章占比（不考虑其他列）
not_null_where_without_filter = len(original_data[original_data['Where'].notnull()])
where_percentage_without_filter = not_null_where_without_filter / len(original_data)
st.write(f"文章中Where不为空的占比 (无筛选): {where_percentage_without_filter:.2%}")

# 3. 满足Where,不为空，且Who不为空的文章占比
where_and_who = len(original_data[(original_data['Where'].notnull()) & (original_data['Who'].notnull())])
where_and_who_percentage = where_and_who / len(original_data)
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

'''