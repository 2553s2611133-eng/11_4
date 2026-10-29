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
"""

ICON_RABBIT = """
<svg width="115" height="115" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
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

# [수정] 오른쪽 아래 캐릭터: 실제 친칠라 디자인 (큰 동그란 귀, 회색 털, 수염 디테일)
ICON_CHINCHILLA = """
<svg width="120" height="120" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 친칠라 큰 귀 (왼쪽, 오른쪽) -->
  <ellipse cx="32" cy="42" rx="18" ry="22" fill="#8d99ae" stroke="#2b2d42" stroke-width="3.5" transform="rotate(-18 32 42)"/>
  <ellipse cx="32" cy="42" rx="11" ry="14" fill="#edf2f4" opacity="0.7" transform="rotate(-18 32 42)"/>
  <ellipse cx="88" cy="42" rx="18" ry="22" fill="#8d99ae" stroke="#2b2d42" stroke-width="3.5" transform="rotate(18 88 42)"/>
  <ellipse cx="88" cy="42" rx="11" ry="14" fill="#edf2f4" opacity="0.7" transform="rotate(18 88 42)"/>
  
  <!-- 친칠라 통통한 얼굴 -->
  <ellipse cx="60" cy="72" rx="42" ry="36" fill="#a2abb8" stroke="#2b2d42" stroke-width="3.5"/>
  <!-- 하얀 주둥이 영역 -->
  <ellipse cx="60" cy="80" rx="22" ry="17" fill="#f8fafc"/>
  
  <!-- 눈 -->
  <circle cx="43" cy="66" r="5" fill="#1e293b"/>
  <circle cx="41.5" cy="64.5" r="1.5" fill="#ffffff"/>
  <circle cx="77" cy="66" r="5" fill="#1e293b"/>
  <circle cx="75.5" cy="64.5" r="1.5" fill="#ffffff"/>
  
  <!-- 분홍빛 코 & 입 -->
  <ellipse cx="60" cy="74" rx="4.5" ry="3.5" fill="#fb7185"/>
  <path d="M56 78 Q 60 82 64 78" stroke="#2b2d42" stroke-width="2.5" fill="none"/>
  
  <!-- 친칠라 매력 긴 수염 -->
  <line x1="22" y1="74" x2="36" y2="75" stroke="#2b2d42" stroke-width="2"/>
  <line x1="20" y1="80" x2="36" y2="79" stroke="#2b2d42" stroke-width="2"/>
  <line x1="24" y1="86" x2="37" y2="83" stroke="#2b2d42" stroke-width="2"/>
  
  <line x1="98" y1="74" x2="84" y2="75" stroke="#2b2d42" stroke-width="2"/>
  <line x1="100" y1="80" x2="84" y2="79" stroke="#2b2d42" stroke-width="2"/>
  <line x1="96" y1="86" x2="83" y2="83" stroke="#2b2d42" stroke-width="2"/>
</svg>
"""

# 4. 숙소 샘플 데이터베이스
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
            "full_address": "충청남도 천안시 서북구 불당동 카페거리",
            "stay_type": "호텔",
            "allowed_pets": ["강아지", "고양이", "소동물(토끼/친칠라)"],
            "max_weight": "소형견 (7kg 이하)",
            "amenities": ["실내 놀이터", "전용 드라이룸"],
            "price": 130000,
            "rating": 4.8,
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&auto=format&fit=crop&q=80"
        },
        {
            "id": 3,
            "name": "제주 애월 멍스테이 풀빌라",
            "region": "제주",
            "full_address": "제주특별자치도 제주시 애월읍",
            "stay_type": "풀빌라",
            "allowed_pets": ["강아지"],
            "max_weight": "대형견 (15kg 초과)",
            "amenities": ["독채 잔디마당", "반려견 전용수영장", "바비큐"],
            "price": 290000,
            "rating": 4.95,
            "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=600&auto=format&fit=crop&q=80"
        },
        {
            "id": 4,
            "name": "가평 포레스트 
