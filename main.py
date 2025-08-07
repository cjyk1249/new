import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="국가별 MBTI 유형 분포", layout="centered")

st.title("🌍 국가별 MBTI 유형 분포 분석")
st.write("""
이 웹앱은 세계 각국의 MBTI 16가지 성격 유형 비율을 시각화하여 
국가 간 성격 경향의 차이를 이해하는 데 도움을 줍니다.
""")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    df['Total'] = df.iloc[:, 1:].sum(axis=1)
    return df

df = load_data()

# 국가 선택
country_list = df["Country"].sort_values().tolist()
selected_country = st.selectbox("국가를 선택하세요", country_list, index=country_list.index("South Korea") if "South Korea" in country_list else 0)

# MBTI 추출
mbti_columns = ['INFJ', 'ISFJ', 'INTP', 'ISFP', 'ENTP', 'INFP', 'ENTJ', 'ISTP',
                'INTJ', 'ESFP', 'ESTJ', 'ENFP', 'ESTP', 'ISTJ', 'ENFJ', 'ESFJ']

# 선택한 국가 데이터
selected_data = df[df["Country"] == selected_country][mbti_columns].T.reset_index()
selected_data.columns = ['MBTI', '비율']
selected_data['비율'] = selected_data['비율'] * 100  # 퍼센트화

# 비교용 국가 선택 (선택사항)
st.write("선택한 국가와 다른 국가의 MBTI 분포를 비교해보세요.")
compare = st.checkbox("비교 국가 선택하기")
if compare:
    compare_country = st.selectbox("비교할 국가를 선택하세요", [c for c in country_list if c != selected_country])
    compare_data = df[df["Country"] == compare_country][mbti_columns].T.reset_index()
    compare_data.columns = ['MBTI', '비율']
    compare_data['비율'] = compare_data['비율'] * 100
    selected_data['비교'] = compare_data['비율']

# Altair 차트
st.subheader(f"🇨🇳 {selected_country}의 MBTI 분포")

chart = alt.Chart(selected_data).mark_bar().encode(
    x=alt.X('MBTI', sort=mbti_columns),
    y=alt.Y('비율', title='비율 (%)'),
    tooltip=['MBTI', '비율']
).properties(width=600, height=400)

if compare:
    line = alt.Chart(selected_data).mark_line(color='orange').encode(
        x='MBTI',
        y='비교',
        tooltip=['MBTI', '비교']
    )
    st.altair_chart(chart + line, use_container_width=True)
else:
    st.altair_chart(chart, use_container_width=True)

# MBTI 합계 확인
st.caption(f"⚠️ 선택한 국가의 MBTI 총합: {df[df['Country'] == selected_country]['Total'].values[0]:.4f}")
