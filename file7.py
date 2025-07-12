import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import random

st.set_page_config(page_title="삼각함수 애니메이션 도우미", layout="wide")

# 페이지 스타일 커스텀 (CSS 삽입)
st.markdown("""
    <style>
    .main > div {
        max-width: 900px;
        margin: auto;
        padding: 1rem 2rem;
    }
    h1 {
        color: #004d99;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .stSlider > div > div > input {
        accent-color: #007acc;
    }
    .stButton>button {
        background-color: #007acc;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        padding: 8px 20px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #005fa3;
        cursor: pointer;
    }
    .quiz-area {
        background: #f0f8ff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 3px 15px rgba(0, 122, 204, 0.15);
        margin-top: 2rem;
    }
    .result-success {
        color: green;
        font-weight: 700;
        margin-top: 1rem;
    }
    .result-error {
        color: red;
        font-weight: 700;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📐 삼각함수 애니메이션 도우미")

# 각도 슬라이더
angle_deg = st.slider("각도 (θ, 도 단위)", 0, 360, 0, help="슬라이더를 움직여 단위원상의 점과 삼각함수 값을 확인하세요.")
angle_rad = math.radians(angle_deg)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("단위원 상의 점")
    fig1, ax1 = plt.subplots(figsize=(4,4))
    circle = plt.Circle((0, 0), 1, color='#a8d0ff', fill=False, linewidth=2)
    ax1.add_artist(circle)

    x = math.cos(angle_rad)
    y = math.sin(angle_rad)

    ax1.plot([0, x], [0, y], color='#ff595e', linewidth=3)
    ax1.plot(x, y, 'o', color='#1982c4', markersize=12)
    ax1.set_xlim([-1.2, 1.2])
    ax1.set_ylim([-1.2, 1.2])
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_title(f"θ = {angle_deg}°", fontsize=14, color="#004d99")
    st.pyplot(fig1)

    st.markdown(f"🔹 **sin(θ)** = {y:.3f}")
    st.markdown(f"🔹 **cos(θ)** = {x:.3f}")
    if math.isclose(x, 0, abs_tol=1e-6):
        st.markdown("🔹 **tan(θ)** = 무한")
    else:
        st.markdown(f"🔹 **tan(θ)** = {math.tan(angle_rad):.3f}")

with col2:
    st.subheader("y = sin(θ) 그래프")
    theta = np.linspace(0, 2*np.pi, 361)
    sin_values = np.sin(theta)

    fig2, ax2 = plt.subplots(figsize=(8, 3))
    ax2.plot(np.degrees(theta), sin_values, label='y = sin(θ)', color='#007acc', linewidth=2)
    ax2.axvline(x=angle_deg, color='#ff595e', linestyle='--', linewidth=2, label=f'θ = {angle_deg}°')
    ax2.set_xlim([0, 360])
    ax2.set_ylim([-1.2, 1.2])
    ax2.set_xlabel('θ (deg)', fontsize=12)
    ax2.set_ylabel('y', fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    st.pyplot(fig2)

    st.markdown("**함수 정보**")
    st.markdown("- 주기: 360°")
    st.markdown("- 진폭: 1")
    st.markdown("- 최대값: 1")
    st.markdown("- 최소값: -1")

# 퀴즈 기능 영역
st.markdown('<div class="quiz-area">', unsafe_allow_html=True)
st.subheader("🧠 퀴즈 시간!")

quiz_list = [
    {"q": "y = 2sin(θ)의 진폭은?", "a": "2"},
    {"q": "y = cos(θ)의 주기는? (단위: 도)", "a": "360"},
    {"q": "y = -3sin(θ)의 최소값은?", "a": "-3"},
    {"q": "y = 0.5cos(θ)의 최대값은?", "a": "0.5"},
    {"q": "sin(90°)의 값은?", "a": "1"},
    {"q": "cos(180°)의 값은?", "a": "-1"},
    {"q": "tan(45°)의 값은?", "a": "1"},
    {"q": "sin(0°)의 값은?", "a": "0"},
    {"q": "tan(90°)의 값은?", "a": "무한"},
    {"q": "y = sin(θ)의 주기는 몇 도인가요?", "a": "360"},
    {"q": "y = 3cos(θ)의 진폭은?", "a": "3"},
    {"q": "y = -2sin(θ)의 최대값은?", "a": "2"},
    {"q": "tan(0°)의 값은?", "a": "0"},
    {"q": "cos(270°)의 값은?", "a": "0"},
    {"q": "sin(180°)의 값은?", "a": "0"},
]

if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

col3, col4 = st.columns([1,1])

with col3:
    if st.button("퀴즈 시작", key="start_quiz"):
        st.session_state.current_quiz = random.choice(quiz_list)
        st.session_state.answer = ""
        st.session_state.quiz_result = None

with col4:
    if st.button("퀴즈 초기화", key="reset_quiz"):
        st.session_state.current_quiz = None
        st.session_state.answer = ""
        st.session_state.quiz_result = None

if st.session_state.current_quiz:
    st.markdown(f"**문제:** {st.session_state.current_quiz['q']}")
    st.session_state.answer = st.text_input("답을 입력하세요", value=st.session_state.answer, key="quiz_answer_input")

    if st.button("제출", key="submit_quiz"):
        user_answer = st.session_state.answer.strip()
        correct_answer = st.session_state.current_quiz["a"].strip()
        # 정답 대소문자 무시 비교 및 '무한'도 처리
        if user_answer.lower() == correct_answer.lower():
            st.session_state.quiz_result = ("success", "✅ 정답입니다!")
        else:
            st.session_state.quiz_result = ("error", f"❌ 오답입니다. 정답은 {correct_answer}입니다.")

if st.session_state.quiz_result:
    status, msg = st.session_state.quiz_result
    if status == "success":
        st.markdown(f'<p class="result-success">{msg}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<p class="result-error">{msg}</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
