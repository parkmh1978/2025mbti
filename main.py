import koreanize_matplotlib

import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 로드
df = pd.read_csv("countriesMBTI.csv")

# MBTI 유형 단순화 (-T, -A 제거)
df.columns = [col[:-2] if col not in ["Country"] else col for col in df.columns]
df = df.groupby("Country", as_index=False).sum()

# 앱 제목 (이모지 활용)
st.title("🌍 국가별 MBTI 성향 분석 🔍")

# 국가 선택
global_mbti_types = df.columns[1:].tolist()
country = st.selectbox("🌏 국가를 선택하세요:", df["Country"].unique())

# 선택한 국가의 MBTI 분포 시각화 (내림차순 정렬 및 마우스 오버 시 퍼센트 표시)
st.subheader(f"📊 {country}의 MBTI 분포")
selected_data = df[df["Country"] == country].iloc[:, 1:].T
selected_data.columns = [country]
selected_data = selected_data.sort_values(by=country, ascending=False)
fig = px.bar(selected_data, x=selected_data.index, y=country, text=selected_data[country],
             title=f"{country}의 MBTI 분포", labels={country: "비율"},
             hover_data={country: ':.2%'})
st.plotly_chart(fig)

# 전체 데이터 평균 분석 (내림차순 정렬 및 마우스 오버 시 퍼센트 표시)
st.subheader("📊 전체 국가의 MBTI 평균 비율")
mbti_avg = df.iloc[:, 1:].mean().sort_values(ascending=False)
fig_avg = px.bar(mbti_avg, x=mbti_avg.index, y=mbti_avg.values, text=mbti_avg.values,
                 title="전체 국가별 MBTI 평균", labels={"y": "평균 비율"},
                 hover_data={"y": ':.2%'})
st.plotly_chart(fig_avg)

# MBTI 유형별 상위 10개국 & 한국 시각화
target_mbti = st.selectbox("💡 MBTI 유형을 선택하세요:", global_mbti_types)
st.subheader(f"🏆 {target_mbti} 비율이 높은 국가 TOP 10 & 한국")

if target_mbti in df.columns:
    top_10 = df.nlargest(10, target_mbti)[["Country", target_mbti]]
    korea_value = df[df["Country"] == "South Korea"][target_mbti].values[0] if "South Korea" in df["Country"].values else None

    if korea_value is not None:
        korea_data = pd.DataFrame({"Country": ["South Korea"], target_mbti: [korea_value]})
        top_10 = pd.concat([top_10, korea_data])

    top_10 = top_10.sort_values(by=target_mbti, ascending=False)
    fig_top = px.bar(top_10, x="Country", y=target_mbti, text=top_10[target_mbti], color="Country",
                     color_discrete_map={"South Korea": "red"}, title=f"{target_mbti} 비율 TOP 10 & 한국",
                     labels={target_mbti: "비율"}, hover_data={target_mbti: ':.2%'})
    st.plotly_chart(fig_top)
else:
    st.error("선택한 MBTI 유형이 데이터에 존재하지 않습니다.")

