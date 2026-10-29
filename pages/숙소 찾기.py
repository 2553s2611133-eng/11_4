import streamlit as st
import pandas as pd
import urllib.parse

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="PetStay - 반려동물 동반 숙소 검색",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 사진 디자인 기반 커스텀 스타일 (크림 톤, 캡슐 검색바, 둥근 지도)
st.markdown("""
    <style>
    .stApp {
        background-color: #faf6ef;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* 시안 속 둥근 캡슐형 검색창 */
    div[data-testid="stTextInput"] > div > div {
        background-color: #ffffff !important;
        border: 2.5px solid #6b7280 !important;
        border-radius: 40px !important;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08) !important;
        height: 62px;
        padding-left: 15px;
    }
    
    div[data-testid="stTextInput"] input {
        font-size: 1.12rem !important;
        color: #1f2937 !important;
        font-weight: 500;
    }

    /* 사진 속 둥근 모서리 지도 컨테이너 */
    .map-frame-wrapper {
        border-radius: 28px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.09);
        border: 4px solid #ffffff;
        background-color: #e5e7eb;
        margin-top: 14px;
    }

    /* 좌우 캐릭터 정렬 */
    .character-box {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 480px;
        padding: 10px 0;
    }

    /* 하단 추천 숙소 카드 */
    .stay-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.05);
        border: 1px solid #ede8df;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .stay-card:hover {
        transform: translateY(-4px);
    }
    .badge {
        display: inline-block;
        background-color: #f3efe6;
        color: #7c3aed;
        padding: 4px 9px;
        border-radius: 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 고화질 벡터 일러스트 (발자국, 강아지, 토끼, 친칠라)
ICON_PAW = """
<svg width="105" height="105" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="22" cy="38" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="42" cy="22" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="68" cy="24" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="84" cy="42" rx="9" ry="13" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <path d="M30 60 C 22 75, 30 92, 53 92 C 76 92, 85 75, 77 60 C 70 48, 38 48, 30 60 Z" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
</svg>
"""

ICON_DOG = """
<svg width="115" height="115" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="62" rx="16" ry="24" fill="#a46d50" stroke="#3d2314" stroke-width="3.5" transform="rotate(-15 28 62)"/>
  <ellipse cx="92" cy="62" rx="16" ry="24" fill="#a46d50" stroke="#3d2314" stroke-width="3.5" transform="rotate(15 92 62)"/>
  <ellipse cx="60" cy="70" rx="42" ry="36" fill="#faebd7" stroke="#3d2314" stroke-width="3.5"/>
  <ellipse cx="76" cy="64" rx="14" ry="12" fill="#a46d50" opacity="0.85"/>
  <circle cx="45" cy="64" r="4.5" fill="#3d2314"/>
  <circle cx="75" cy="64" r="4.5" fill="#3d2314"/>
  <ellipse cx="60" cy="74" rx="5" ry="4" fill="#3d2314"/>
  <path d="M54 78 Q 60 83 66 78" stroke="#3d2314" stroke-width="3" fill="none"/>
  <path d="M57 80 Q 60 89 63 80 Z" fill="#f87171"/>
</svg>
