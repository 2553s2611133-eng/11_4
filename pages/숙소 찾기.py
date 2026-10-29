import streamlit as st
import pandas as pd
import urllib.parse

# 1. 페이지 설정 (완벽한 와이드 모드 및 탭 제목 설정)
st.set_page_config(
    page_title="PetStay - 반려동물 동반 숙소 검색",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 업로드해주신 사진과 한 치의 오차도 없는 1:1 완벽 매칭 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경을 사진 속 따뜻한 크림/아이보리 톤으로 지정 */
    .stApp {
        background-color: #fbf8f2;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    }
    
    /* 레이아웃 여백 미세 조정 */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px;
    }

    /* [중요] 시안 속 둥근 캡슐형 검색바 및 입체 그림자 */
    div[data-testid="stTextInput"] > div > div {
        background-color: #ffffff !important;
        border: 2.5px solid #4a5568 !important;
        border-radius: 40px !important;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.07) !important;
        height: 64px;
        padding-left: 18px;
    }
    
    div[data-testid="stTextInput"] input {
        font-size: 1.15rem !important;
        color: #1a202c !important;
        font-weight: 600;
    }

    /* 시안 속 테두리와 모서리가 아주 둥근 지도 영역 */
    .map-frame-wrapper {
        border-radius: 32px;
        overflow: hidden;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
        border: 4px solid #ffffff;
        background-color: #e2e8f0;
        margin-top: 16px;
    }

    /* 좌우 캐릭터들을 수직으로 예쁘게 정렬하기 위한 박스 */
    .character-box {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 480px;
        padding: 15px 0;
    }

    /* [새로 추가] 필터 확장 버튼을 사진 분위기와 어울리게 둥글게 가공 */
    .stExpander {
        border: 1.5px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
        margin-top: 12px;
    }

    /* 하단 추천 숙소 카드 */
    .stay-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 18px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.04);
        border: 1px solid #eae5da;
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    }
    .stay-card:hover {
        transform: translateY(-4px);
    }
    .badge {
        display: inline-block;
        background-color: #f3eee3;
        color: #7c3aed;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 고화질 벡터 일러스트 (사진 시안 속 4가지 캐릭터 완벽 재현)
ICON_PAW = """
<svg width="115" height="115" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="22" cy="38" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="42" cy="22" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="68" cy="24" rx="10" ry="14" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <ellipse cx="84" cy="42" rx="9" ry="13" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
  <path d="M30 60 C 22 75, 30 92, 53 92 C 76 92, 85 75, 77 60 C 70 48, 38 48, 30 60 Z" fill="#a47560" stroke="#4a2e2b" stroke-width="3"/>
</svg>
"""

ICON_DOG = """
<svg width="125" height="125" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 귀 -->
  <ellipse cx="28" cy="62" rx="16" ry="24" fill="#a46d50" stroke="#3d2314" stroke-width="3.5" transform="rotate(-15 28 62)"/>
  <ellipse cx="92" cy="62" rx="16" ry="24" fill="#a46d50" stroke="#3d2314" stroke-width="3.5" transform="rotate(15 92 62)"/>
  <!-- 얼굴 -->
  <ellipse cx="60" cy="70" rx="42" ry="36" fill="#faebd7" stroke="#3d2314" stroke-width="3.5"/>
  <!-- 눈 주변 얼룩 반점 -->
  <ellipse cx="76" cy="64" rx="14" ry="12" fill="#a46d50" opacity="0.85"/>
  <!-- 눈 -->
  <circle cx="45" cy="64" r="4.5" fill="#3d2314"/>
  <circle cx="75" cy="64" r="4.5" fill="#3d2314"/>
  <!-- 코와 입 -->
  <ellipse cx="60" cy="74" rx="5" ry="4" fill="#3d2314"/>
  <path d="M54 78 Q 60 83 66 78" stroke="#3d2314" stroke-width="3.0" fill="none"/>
  <!-- 혀 -->
  <path d="M57 80 Q 60 89 63 80 Z" fill="#f87171"/>
</svg>
"""

ICON_RABBIT = """
<svg width="125" height="125" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 귀 -->
  <ellipse cx="44" cy="36" rx="11" ry="28" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5" transform="rotate(-8 44 36)"/>
  <ellipse cx="44" cy="36" rx="6" ry="20" fill="#fbcfe8" transform="rotate(-8 44 36)"/>
  <ellipse cx="76" cy="36" rx="11" ry="28" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5" transform="rotate(8 76 36)"/>
  <ellipse cx="76" cy="36" rx="6" ry="20" fill="#fbcfe8" transform="rotate(8 76 36)"/>
  <!-- 얼굴 -->
  <ellipse cx="60" cy="76" rx="38" ry="32" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5"/>
  <!-- 볼터치 -->
  <circle cx="38" cy="80" r="5" fill="#fca5a5" opacity="0.65"/>
  <circle cx="82" cy="80" r="5" fill="#fca5a5" opacity="0.65"/>
  <!-- 눈 -->
  <circle cx="47" cy="73" r="4" fill="#452c1e"/>
  <circle cx="73" cy="73" r="4" fill="#452c1e"/>
  <!-- 코와 입 -->
  <ellipse cx="60" cy="78" rx="3.5" ry="3" fill="#452c1e"/>
  <path d="M56 81 Q 60 84 64 81" stroke="#452c1e" stroke-width="2.5" fill="none"/>
  <!-- 수염 -->
  <line x1="28" y1="76" x2="36" y2="76" stroke="#452c1e" stroke-width="2"/>
  <line x1="27" y1="81" x2="35" y2="80" stroke="#452c1e" stroke-width="2"/>
  <line x1="84" y1="76" x2="92" y2="76" stroke="#452c1e" stroke-width="2"/>
  <line x1="85" y1="80" x2="93" y2="81" stroke="#452c1e" stroke-width="2"/>
</svg>
"""

ICON_HAMSTER = """
<svg width="125" height="125" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 귀 -->
  <circle cx="36" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="36" cy="46" r="9" fill="#d1d5db"/>
  <circle cx="84" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="84" cy="46" r="9" fill="#d1d5db"/>
  <!-- 얼굴 -->
  <ellipse cx="60" cy="72" rx="40" ry="34" fill="#9ca3af" stroke="#2b333e" stroke-width="3.5"/>
  <!-- 주둥이와 볼 터치 -->
  <ellipse cx="60" cy="79" rx="20" ry="16" fill="#f3f4f6"/>
  <!-- 눈 -->
  <circle cx="45" cy="67" r="4" fill="#1f2937"/>
  <circle cx="75" cy="67" r="4" fill="#1f2937"/>
  <!-- 코와 입 -->
  <ellipse cx="60" cy="74" rx="4" ry="3" fill="#374151"/>
  <path d="M57 77 Q 60 80 63 77" stroke="#374151" stroke-width="2.5" fill="none"/>
  <!-- 수염 -->
  <line x1="26" y1="75" x2="37" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="27" y1="81" x2="38" y2="79" stroke="#2b333e" stroke-width="2"/>
  <line x1="83" y1="75" x2="94" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="82" y1="79" x2="93" y2="81" stroke="#2b333e" stroke-width="2"/>
</svg>
"""

# 4. 숙소 데이터베이스 구축
@st.cache_data
def get_stays_data():
    return pd.DataFrame([
        {
            "id": 1,
            "name": "천안 불당 펫파크 독채 하우스",
            "region": "불당동",
            "full_address": "충청남도 천안시 서북구 불당동",
            "stay_type": "펜션/독채",
            "allowed_pets": ["강아지", "고양이"],
            "max_weight": "중형견 (15kg 이하)",
            "amenities": ["독채 잔디마당", "어질리티 구역", "바비큐"],
            "price": 180000,
            "rating": 4.9,
            "image": "https://images.unsplash.com/photo-1587560699334-cc4ff634909a?w=600&auto=format&fit=crop&q=80"
        },
        {
            "id": 2,
            "name": "불당 센트럴 펫 부티크 호텔",
            "region": "불당동",
