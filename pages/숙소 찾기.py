import streamlit as st
import pandas as pd
import urllib.parse
import os
import google.generativeai as genai

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="PetStay - 반려동물 동반 숙소 검색",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 사진 시안 스타일 100% 반영 커스텀 CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #faf6ef;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* 캡슐형 검색창 */
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

    /* 둥근 구글 지도 테두리 */
    .map-frame-wrapper {
        border-radius: 28px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.09);
        border: 4px solid #ffffff;
        background-color: #e5e7eb;
        margin-top: 10px;
    }

    /* 캐릭터 영역 */
    .character-box {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 460px;
        padding: 10px 0;
    }

    /* 결과 카드 스타일 */
    .stay-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.05);
        border: 1px solid #ede8df;
        margin-bottom: 20px;
    }
    .stay-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 6px;
    }
    .badge-tag {
        display: inline-block;
        background-color: #f3efe6;
        color: #d97706;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 고화질 SVG 캐릭터 일러스트
ICON_PAW = """
<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="22" cy="38" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="42" cy="22" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="68" cy="24" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="84" cy="42" rx="9" ry="13" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <path d="M30 60 C 22 75, 30 92, 53 92 C 76 92, 85 75, 77 60 C 70 48, 38 48, 30 60 Z" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
</svg>
"""

ICON_DOG = """
<svg width="110" height="110" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
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
"""

ICON_RABBIT = """
<svg width="110" height="110" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="44" cy="36" rx="11" ry="28" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5" transform="rotate(-8 44 36)"/>
  <ellipse cx="44" cy="36" rx="6" ry="20" fill="#fbcfe8" transform="rotate(-8 44 36)"/>
  <ellipse cx="76" cy="36" rx="11" ry="28" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5" transform="rotate(8 76 36)"/>
  <ellipse cx="76" cy="36" rx="6" ry="20" fill="#fbcfe8" transform="rotate(8 76 36)"/>
  <ellipse cx="60" cy="76" rx="38" ry="32" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5"/>
  <circle cx="38" cy="80" r="5" fill="#fca5a5" opacity="0.6"/>
  <circle cx="82" cy="80" r="5" fill="#fca5a5" opacity="0.6"/>
  <circle cx="47" cy="73" r="4" fill="#452c1e"/>
  <circle cx="73" cy="73" r="4" fill="#452c1e"/>
  <ellipse cx="60" cy="78" rx="3.5" ry="3" fill="#452c1e"/>
  <path d="M56 81 Q 60 84 64 81" stroke="#452c1e" stroke-width="2.5" fill="none"/>
  <line x1="28" y1="76" x2="36" y2="76" stroke="#452c1e" stroke-width="2"/>
  <line x1="27" y1="81" x2="35" y2="80" stroke="#452c1e" stroke-width="2"/>
  <line x1="84" y1="76" x2="92" y2="76" stroke="#452c1e" stroke-width="2"/>
  <line x1="85" y1="80" x2="93" y2="81" stroke="#452c1e" stroke-width="2"/>
</svg>
"""

ICON_HAMSTER = """
<svg width="110" height="110" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="36" cy="46" r="9" fill="#d1d5db"/>
  <circle cx="84" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="84" cy="46" r="9" fill="#d1d5db"/>
  <ellipse cx="60" cy="72" rx="40" ry="34" fill="#9ca3af" stroke="#2b333e" stroke-width="3.5"/>
  <ellipse cx="60" cy="79" rx="20" ry="16" fill="#f3f4f6"/>
  <circle cx="45" cy="67" r="4" fill="#1f2937"/>
  <circle cx="75" cy="67" r="4" fill="#1f2937"/>
  <ellipse cx="60" cy="74" rx="5" ry="4" fill="#374151"/>
  <path d="M57 77 Q 60 80 63 77" stroke="#374151" stroke-width="2.5" fill="none"/>
  <line x1="26" y1="75" x2="37" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="27" y1="81" x2="38" y2="79" stroke="#2b333e" stroke-width="2"/>
  <line x1="83" y1="75" x2="94" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="82" y1="79" x2="93" y2="81" stroke="#2b333e" stroke-width="2"/>
</svg>
"""

# 4. Gemini API 호출 함수 (안정적인 SDK 사용)
def ask_gemini(search_query):
    api_key = None
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "message": "Streamlit Secrets에 GEMINI_API_KEY 설정이 안 되어 있습니다."
        }

    try:
        genai.configure(api_key=api_key)
        # gemini-2.5-flash-lite 모델 호출
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        prompt = (
            "너는 반려동물 동반 숙소 전문 AI다. "
            "사용자가 입력한 다음 키워드를 기반으로 지역, 반려동물 제한, 숙소 특징을 파악해서 "
            "해당 조건에 딱 맞는 추천 숙소 3곳과 특징을 정갈하게 정리해줘.\n\n"
            f"검색어: {search_query}"
        )
        
        response = model.generate_content(prompt)
        return {
            "status": "success",
            "text": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"API 호출 오류 발생: {str(e)}"
        }

# 5. 메인 레이아웃
col_left, col_center, col_right = st.columns([1.2, 5.5, 1.2])

with col_left:
    st.markdown(f'<div class="character-box"><div>{ICON_PAW}</div><div>{ICON_DOG}</div></div>', unsafe_allow_html=True)

with col_center:
    search_input = st.text_input(
        label="search",
        placeholder="🔍 반려동물 크기, 위치, 숙소 형태 등을 입력해 주세요",
        label_visibility="collapsed"
    )
    
    query_text = search_input.strip() if search_input.strip() else "불당동"
    
    # 구글 지도 생성
    encoded_q = urllib.parse.quote(query_text + " 반려동물 동반 숙소")
    map_url = "https://maps.google.com/maps?q=" + encoded_q + "&t=&z=14&ie=UTF8&iwloc=&output=embed"
    
    st.markdown(
        f'<div class="map-frame-wrapper"><iframe width="100%" height="450" frameborder="0" scrolling="no" src="{map_url}"></iframe></div>',
        unsafe_allow_html=True
    )

with col_right:
    st.markdown(f'<div class="character-box"><div>{ICON_RABBIT}</div><div>{ICON_HAMSTER
