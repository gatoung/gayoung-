import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import random

st.set_page_config(page_title="삼각함수 애니메이션 도우미", layout="wide")
st.title("📐 삼각함수 애니메이션 도우미")

# 각도 슬라이더
angle_deg = st.slider("각도 (θ, 도 단위)", 0, 360, 0)
angle_rad = math.radians(angle_deg)

col1, col2 = st.columns(2)

with col1:
    st.subheader("단위원 상의 점")
    fig1, ax1 = plt.subplots()
    circle = plt.Circle((0, 0), 1, color='lightblue', fill=False)
    ax1.add_artist(circle)

    x = math.cos(angle_rad)
    y = math.sin(angle_rad)

    ax1.plot([0, x], [0, y], color='red')
    ax1.plot(x, y, 'bo')
    ax1.set_xlim([-1.2, 1.2])
    ax1.set_ylim([-1.2, 1.2])
    ax1.set_aspect('equal')
    ax1.grid(True)
    st.pyplot(fig1)

    st.markdown(f"🔹 sin(θ) = {math.sin(angle_rad):.2f}")
    st.markdown(f"🔹 cos(θ) = {math.cos(angle_rad):.2f}")
    if abs(math.cos(angle_rad)) < 1e-6:
        st.markdown("🔹 tan(θ) = 무한")
    else:
        st.markdown(f"🔹 tan(θ) = {math.tan(angle_rad):.2f}")

with col2:
    st.subheader("y = sin(θ) 그래프")
    theta = np.linspace(0, 2*np.pi, 361)
    sin_values = np.sin(theta)

    fig2, ax2 = plt.subplots()
    ax2.plot(np.degrees(theta), sin_values, label='y = sin(θ)', color='#007acc')
    ax2.axvline(x=angle_deg, color='red', linestyle='--')
    ax2.set_xlim([0, 360])
    ax2.set_ylim([-1.2, 1.2])
    ax2.set_xlabel('θ (deg)')
    ax2.set_ylabel('y')
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

    st.markdown("**함수 정보**")
    st.markdown("- 주기: 360°")
    st.markdown("- 진폭: 1")
    st.markdown("- 최대값: 1")
    st.markdown("- 최소값: -1")

# 퀴즈 기능
st.subheader("🧠 퀴즈 시간!")
quiz_list = [
    {"q": "y = 2sin(θ)의 진폭은?", "a": "2"},
    {"q": "y = cos(θ)의 주기는? (단위: 도)", "a": "360"},
    {"q": "y = -3sin(θ)의 최소값은?", "a": "-3"},
    {"q": "y = 0.5cos(θ)의 최대값은?", "a": "0.5"},
]

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

if st.button("퀴즈 시작"):
    st.session_state.current_quiz = random.choice(quiz_list)
    st.session_state.answer = ""

if st.session_state.current_quiz:
    st.write(st.session_state.current_quiz["q"])
    st.session_state.answer = st.text_input("답을 입력하세요", value=st.session_state.get("answer", ""))
    if st.button("제출"):
        if st.session_state.answer.strip() == st.session_state.current_quiz["a"]:
            st.success("✅ 정답입니다!")
        else:
            st.error(f"❌ 오답입니다. 정답은 {st.session_state.current_quiz['a']}입니다.")
