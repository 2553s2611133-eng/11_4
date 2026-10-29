import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS (귀여운 느낌 테마)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="멍트래블 - 반려견 동반 여행 정보",
    page_icon="🐾",
    layout="wide"
)

# 귀여운 테마 커스텀 CSS (배경색, 카드 디자인, 둥근 모서리)
st.markdown("""
    <style>
    /* 전체 배경색 - 따뜻한 크림/아이보리 톤 */
    .stApp {
        background-color: #FFFDF9;
    }
    
    /* 사이드바 제거 및 메인 콘텐츠 집중 */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* 메인 타이틀 디자인 (귀여운 노란색 하이라이트) */
    h1 {
        color: #FF8F00 !important;
        font-family: 'Comic Sans MS', 'GmarketSansBold', sans-serif;
        text-align: center;
        margin-top: 0;
    }

    /* 검색 바 디자인 (이미지 재현) */
    .stTextInput>div>div>input {
        border-radius: 30px !important;
        border: 2px solid #FFCA28 !important;
        background-color: white !important;
        padding-left: 45px !important; /* 돋보기 아이콘 공간 */
    }
    .stTextInput::before {
        content: '🔎';
        position: absolute;
        left: 15px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        z-index: 1;
    }

    /* 웰컴 배너 디자인 (이미지 재현) */
    .welcome-banner {
        background-color: #FFE8A3;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 3px dashed #FFB300;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .welcome-banner h2 {
        color: #6D4C41 !important;
        margin:0;
    }
    .welcome-banner p {
        color: #8D6E63;
        margin-top: 5px;
        font-size: 16px;
    }

    /* 카테고리 카드 디자인 (이미지 재현) */
    .category-card {
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        cursor: pointer;
        border: 2px solid #FFF3E0;
        margin: 10px;
    }
    .category-card:hover {
        transform: translateY(-5px);
        border: 2px solid #FFCC80;
    }
    .category-card .icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    .category-card .title {
        font-weight: bold;
        color: #6D4C41;
        font-size: 1.1rem;
    }

    /* AI 가이드 카드 뱃지 디자인 */
    .ai-badge {
        position: absolute;
        top: -10px;
        right: -10px;
        background-color: #007BFF;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.8rem;
    }

    /* 버튼 스타일 - 동글동글하고 아기자기하게 */
    .stButton>button {
        border-radius: 20px !important;
        background-color: #FFE082 !important;
        color: #5D4037 !important;
        border: 2px solid #FFCA28 !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FFCA28 !important;
        transform: scale(1.05);
    }

    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Main Title, Search Bar, and Welcome Banner
# -----------------------------------------------------------------------------
# 메인 타이틀 (이미지 텍스트 반영)
st.title("🐾 멍트래블 (Puppy Travel Hub)")

# 검색 바 (이미지 텍스트 반영)
search_query = st.text_input("", placeholder="강아지와 가고 싶은 곳을 검색해보세요 🐾", key="main_search")

# 웰컴 배너 (이미지 텍스트 반영)
st.markdown("""
    <div class="welcome-banner">
        <h2>🐶 안녕하세요! 반려견과 행복한 여행을 시작해개! 🐾</h2>
        <p>우리 댕댕이가 좋아하는 오프리쉬 놀이터부터 편안한 펜션까지 한눈에 찾아보개!</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Category Cards Layout (이미지 재현)
# -----------------------------------------------------------------------------
st.write("### 🎀 카테고리로 빠르게 찾아보개!")

# 각 카드의 클릭 상태를 저장하기 위한 세션 상태 초기화
if "active_category" not in st.session_state:
    st.session_state.active_category = None

# 5개 카테고리 데이터
categories = [
    {"name": "식당/카페", "icon": "☕", "key": "restaurant"},
    {"name": "숙소", "icon": "🏨", "key": "lodging"},
    {"name": "관광지", "icon": "🌳", "key": "sightseeing"},
    {"name": "이동수단", "icon": "🚕", "key": "transport"},
    {"name": "AI 여행 가이드", "icon": "🤖", "key": "ai_guide", "badge": "Gemini AI 추천!"}
]

# 5열 배치
cols = st.columns(5)

for idx, col in enumerate(cols):
    cat = categories[idx]
    with col:
        # 카드 디자인 (HTML/CSS)
        badge_html = f'<div class="ai-badge">{cat["badge"]}</div>' if "badge" in cat else ""
        st.markdown(f"""
            <div class="category-card">
                {badge_html}
                <div class="icon">{cat["icon"]}</div>
                <div class="title">{cat["name"]}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 실제 클릭 인터랙션을 위한 버튼 (디자인은 카드에 숨김)
        if st.button("", key=f"btn_{cat['key']}", help=cat["name"]):
            st.session_state.active_category = cat["key"]
            st.rerun()

st.markdown("---")

# -----------------------------------------------------------------------------
# 4. 기능 실행 영역 (카테고리 클릭 시 하단에 표시)
# -----------------------------------------------------------------------------

# 기본 시범 데이터 초기화 (이전과 동일)
if "places" not in st.session_state:
    st.session_state.places = [
        {
            "id": 1,
            "name": "멍멍 스테이 펜션",
            "category": "숙소",
            "region": "강원",
            "address": "강원도 강릉시 해안로 123",
            "large_dog": True,
            "off_leash": True,
            "description": "넓은 잔디 마당이 있는 반려견 전용 독채 펜션입니다.",
            "image": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=600",
            "reviews": ["마당이 넓어서 아이가 좋아해요!", "대형견도 눈치 안 보고 잘 쉬다 갑니다."]
        },
        {
            "id": 2,
            "name": "바다뷰 애견카페",
            "category": "식당/카페",
            "region": "제주",
            "address": "제주시 애월읍 애월해안로 456",
            "large_dog": False,
            "off_leash": True,
            "description": "실내 오프리쉬 존이 마련되어 있는 해안가 애견 카페입니다.",
            "image": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=600",
            "reviews": ["음료도 맛있고 뷰가 최고예요."]
        },
        {
            "id": 3,
            "name": "펫택시 댕댕이동",
            "category": "이동수단",
            "region": "서울",
            "address": "서울 전지역 맞춤 운행",
            "large_dog": True,
            "off_leash": False,
            "description": "안전 시트벨트와 켄넬이 구비된 반려견 전용 펫택시 서비스.",
            "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600",
            "reviews": ["기사님이 너무 친절하십니다."]
        }
    ]

active_cat = st.session_state.active_category

# 카테고리가 선택되었을 때만 기능 표시
if active_cat:
    # 1. 일반 장소 탐색 (식당, 숙소, 관광지, 이동수단)
    if active_cat != "ai_guide":
        # 카테고리 이름 가져오기
        cat_name = next((c["name"] for c in categories if c["key"] == active_cat), "장소")
        st.header(f"🔎 '{cat_name}' 탐색 결과")

        # 필터링 적용
        filtered_places = [p for p in st.session_state.places if p["category"] == cat_name]
        
        # 검색 바 검색어 적용
        if search_query.strip():
            filtered_places = [p for p in filtered_places if search_query.strip().lower() in p["name"].lower()]

        if not filtered_places:
            st.warning(f"조건에 맞는 '{cat_name}' 장소가 없습니다. 필터를 변경해보거나 다른 키워드로 검색해보세요.")
        else:
            # 목록 표시 (이전과 동일한 2열 카드 형태 layout)
            for idx, place in enumerate(filtered_places):
                with st.container():
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.image(place["image"], use_container_width=True)
                    with c2:
                        st.subheader(f"[{place['category']}] {place['name']}")
                        st.write(f"📍 **주소:** {place['address']} ({place['region']})")
                        
                        # 태그 표시
                        tags = []
                        if place["large_dog"]:
                            tags.append("🐕 대형견 가능")
                        if place["off_leash"]:
                            tags.append("🦮 오프리쉬 구역")
                        st.write(" ".join([f"`{t}`" for t in tags]) if tags else "`일반 소형견 위주`")
                        
                        st.write(place["description"])

                        # 리뷰 영역 Expander
                        with st.expander("💬 사용자 리뷰 보기 및 작성"):
                            for r in place["reviews"]:
                                st.write(f"- {r}")
                            new_review = st.text_input(f"리뷰 남기기", key=f"rev_{place['id']}")
                            if st.button("리뷰 등록", key=f"btn_{place['id']}"):
                                if new_review.strip():
                                    place["reviews"].append(new_review.strip())
                                    st.success("리뷰가 등록되었습니다!")
                                    st.rerun()
                                else:
                                    st.error("내용을 입력해주세요.")
                st.markdown("---")

    # 2. AI 반려견 여행 AI 가이드
    elif active_cat == "ai_guide":
        st.header("🤖 Gemini 맞춤형 반려견 여행 코스 생성")
        st.write("강아지의 정보와 원하는 여행 스타일을 입력하면 AI가 맞춤형 코스를 추천해드립니다.")

        # 사용자 입력
        dog_size = st.radio("반려견 크기", ["소형견 (10kg 미만)", "중형견 (10kg~25kg)", "대형견 (25kg 이상)"], horizontal=True)
        destination = st.text_input("목적지/지역", value="강원도 강릉")
        style = st.text_input("여행 컨셉 (선택)", value="힐링, 산책 중심, 인생샷")

        if st.button("✨ 맞춤형 일정 추천받기"):
            # API Key 확인
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("`GEMINI_API_KEY`가 설정되지 않았습니다. Secrets 설정 방법을 확인해 주세요.")
            else:
                with st.spinner("AI 가이드가 최적의 코스를 작성 중입니다..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = f"""
                        너는 반려견 전문 여행 가이드야. 아래 조건에 맞는 1박 2일 여행 코스를 추천해줘.
                        
                        - 반려견 크기: {dog_size}
                        - 목적지: {destination}
                        - 여행 컨셉: {style}

                        [요청 사항]
                        1. 1일차, 2일차 시간대별 추천 일정 (식당, 카페, 산책로 포함)
                        2. 해당 강아지 크기에 꼭 필요한 준비물 및 여행 주의사항 3가지
                        3. 이 모드에 맞는 친근하고 명확한 말투 사용
                        """

                        response = client.models.generate_content(
                            model='gemini-2.5-flash-lite',
                            contents=prompt,
                        )

                        st.markdown("### 📋 AI 추천 여행 코스")
                        st.write(response.text)

                    except Exception as e:
                        st.error(f"API 호출 중 오류가 발생했습니다: {e}")

# 카테고리가 선택되지 않았을 때 초기 화면
else:
    st.info("위의 카테고리 카드나 검색 바를 이용하여 원하는 장소를 찾아보세요!")
