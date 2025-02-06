import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize-matplotlib

# 데이터 로드
df = pd.read_csv("countriesMBTI.csv")

# 앱 제목
st.title("국가별 MBTI 성향 분석")

# 국가 선택
global_mbti_types = df.columns[1:]
country = st.selectbox("국가를 선택하세요:", df["Country"].unique())

# 선택한 국가의 MBTI 분포 시각화
st.subheader(f"{country}의 MBTI 분포")
selected_data = df[df["Country"] == country].iloc[:, 1:].T
selected_data.columns = [country]
selected_data.plot(kind="bar", figsize=(10, 5), legend=False)
plt.xlabel("MBTI 유형")
plt.ylabel("비율")
plt.title(f"{country}의 MBTI 분포")
st.pyplot(plt)

# 전체 데이터 평균 분석
st.subheader("전체 국가의 MBTI 평균 비율")
mbti_avg = df.iloc[:, 1:].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 5))
mbti_avg.plot(kind="bar")
plt.xlabel("MBTI 유형")
plt.ylabel("평균 비율")
plt.title("전체 국가별 MBTI 평균")
st.pyplot(plt)

# MBTI 유형별 최대/최소 비율 국가 비교
target_mbti = st.selectbox("MBTI 유형을 선택하세요:", global_mbti_types)
st.subheader(f"{target_mbti} 비율 비교")
max_country = df.loc[df[target_mbti].idxmax(), "Country"]
max_value = df[target_mbti].max()
min_country = df.loc[df[target_mbti].idxmin(), "Country"]
min_value = df[target_mbti].min()
korea_value = df[df["Country"] == "South Korea"][target_mbti].values[0] if "South Korea" in df["Country"].values else None

plt.figure(figsize=(8, 5))
plt.bar([max_country, "South Korea" if korea_value is not None else "(없음)", min_country], [max_value, korea_value if korea_value is not None else 0, min_value])
plt.xlabel("국가")
plt.ylabel("비율")
plt.title(f"{target_mbti} 비율이 높은 나라 vs 낮은 나라 vs 한국")
st.pyplot(plt)
