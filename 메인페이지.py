import streamlit as st
import pandas as pd
import urllib.parse

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="함께 가개 - 반려견 동반 여행 정보",
    page_icon="🐾",
    layout="wide"
)

# 커스텀 테마 CSS (베이지 톤)
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F5F0;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    html, body, [class*="css"]  {
        color: #6D4C41;
    }
    h1 {
        color: #6D4C41 !important;
        text-align: center;
        margin-top: 0;
    }
    .stTextInput>div>div>input {
        border-radius: 30px !important;
        border: 2px solid #D7C9A3 !important;
        background-color: white !important;
    }
    .destination-card {
        background-color: white;
        border-radius: 20px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 2px solid #FFF3E0;
        margin-bottom: 10px;
    }
    .destination-card img {
        border-radius: 15px;
        width: 100%;
        height: 150px;
        object-fit: cover;
    }
    .destination-card .title {
        font-weight: bold;
        color: #6D4C41;
        font-size: 0.95rem;
        margin-top: 8px;
    }
    .welcome-banner {
        background-color: #EFEBE4;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 2px dashed #D7C9A3;
    }
    .welcome-banner h2 {
        color: #6D4C41 !important;
        margin: 0;
    }
    .welcome-banner p {
        color: #8D6E63;
        margin-top: 5px;
        font-size: 15px;
    }
    .stButton>button {
        border-radius: 20px !important;
        background-color: #D7C9A3 !important;
        color: #5D4037 !important;
        border: 1px solid #A18D74 !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A18D74 !important;
        color: white !important;
    }
    .map-btn {
        display: inline-block;
        padding: 6px 12px;
        margin-right: 6px;
        margin-top: 5px;
        border-radius: 15px;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: bold;
        color: white !important;
    }
    .naver-map { background-color: #03CF5D; }
    .kakao-map { background-color: #FEE500; color: #191919 !important; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Main Title & Profile
# -----------------------------------------------------------------------------
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
        <div style="display: flex; align-items: center;">
            <div style="font-size: 2.8rem; margin-right: 12px;">🐶</div>
            <div>
                <h3 style="margin: 0; color: #6D4C41;">반가워요! 댕댕이 보호자님! 👋</h3>
                <p style="margin: 0; color: #8D6E63; font-size: 0.95rem;">함께 가개 🐾 (Together Go Doggy)</p>
            </div>
        </div>
        <div style="font-size: 0.9rem; color: #8D6E63;">⚙️ 설정</div>
    </div>
""", unsafe_allow_html=True)

# 실시간 통합 검색창 (장소명, 지역, 상세설명 모두 검색 가능)
search_query = st.text_input("🔎 실시간 검색", placeholder="장소명, 지역(서울, 제주, 강원 등) 또는 단어를 입력하세요", key="main_search_input").strip()

# 웰컴 배너
st.markdown("""
    <div class="welcome-banner">
        <h2>🐶 반려견과 행복한 여행을 시작해개! 🐾</h2>
        <p>우리 댕댕이가 좋아하는 오프리쉬 놀이터부터 편안한 한옥 숙소, 펫택시까지 한눈에 확인해 보세요!</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Trending Destinations (인기 동반 명소)
# -----------------------------------------------------------------------------
st.write("### 🎀 인기 동반 명소 지도 바로가기")

destinations = [
    {"name": "서울 경복궁 산책로", "query": "경복궁 산책로", "image": "https://images.unsplash.com/photo-1594917409204-747f5255474a?w=400"},
    {"name": "부산 달맞이길 카페", "query": "부산 달맞이길 애견동반카페", "image": "https://images.unsplash.com/photo-1627916327663-1d07914f6d4d?w=400"},
    {"name": "제주 오름 트레킹", "query": "제주 애견동반 오름", "image": "https://images.unsplash.com/photo-1594191370967-b52e3914a5d8?w=400"}
]

cols_dest = st.columns(3)
for idx, col in enumerate(cols_dest):
    dest = destinations[idx]
    with col:
        encoded_query = urllib.parse.quote(dest['query'])
        n_map_url = f"https://map.naver.com/v5/search/{encoded_query}"
        k_map_url = f"https://map.kakao.com/?q={encoded_query}"
        
        st.markdown(f"""
            <div class="destination-card">
                <img src="{dest['image']}" alt="{dest['name']}">
                <div class="title">{dest['name']}</div>
                <div style="margin-top: 8px;">
                    <a href="{n_map_url}" target="_blank" class="map-btn naver-map">🟢 네이버</a>
                    <a href="{k_map_url}" target="_blank" class="map-btn kakao-map">🟡 카카오</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# -----------------------------------------------------------------------------
# 4. 세션 데이터 초기화 (12개의 다양해진 전국 장소 데이터)
# -----------------------------------------------------------------------------
if "places" not in st.session_state:
    st.session_state.places = [
        {
            "id": 1,
            "name": "강릉 멍멍 스테이 펜션",
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
            "name": "제주 바다뷰 애견카페",
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
            "name": "속초 댕댕이 해변 공원",
            "category": "관광지",
            "region": "강원",
            "address": "강원도 속초시 해오름로 789",
            "large_dog": True,
            "off_leash": False,
            "description": "반려견과 함께 산책하기 좋은 해변 산책로입니다.",
            "image": "https://images.unsplash.com/photo-1507146426996-ef05306b995a?w=600",
            "reviews": ["바다 바람 쐬며 산책하기 딱 좋아요!"]
        },
        {
            "id": 4,
            "name": "서울 펫택시 댕댕이동",
            "category": "이동수단",
            "region": "서울",
            "address": "서울특별시 종로구 사직로 161",
            "large_dog": True,
            "off_leash": False,
            "description": "안전 시트벨트와 켄넬이 구비된 반려견 전용 펫택시 서비스.",
            "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=600",
            "reviews": ["기사님이 너무 친절하십니다."]
        },
        {
            "id": 5,
            "name": "가평 힐링 멍캠핑장",
            "category": "숙소",
            "region": "경기",
            "address": "경기도 가평군 북면 가화로 100",
            "large_dog": True,
            "off_leash": True,
            "description": "반려견 울타리가 구비된 오토캠핑장 및 글램핑 공간입니다.",
            "image": "https://images.unsplash.com/photo-1510312305653-8ed496efae75?w=600",
            "reviews": ["캠핑장 시설이 깔끔하고 강아지 울타리가 있어서 안전해요."]
        },
        {
            "id": 6,
            "name": "성수 멍다이닝 파스타",
            "category": "식당/카페",
            "region": "서울",
            "address": "서울특별시 성동구 서울숲길 45",
            "large_dog": False,
            "off_leash": False,
            "description": "실내 반려견 동반 가능한 이탈리안 레스토랑. 멍푸치노 무료 제공!",
            "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600",
            "reviews": ["멍푸치노 너무 귀여워요! 사장님도 친절하십니다."]
        },
        {
            "id": 7,
            "name": "부산 해운대 댕댕크루즈",
            "category": "이동수단",
            "region": "기타",
            "address": "부산광역시 해운대구 달맞이길 62",
            "large_dog": False,
            "off_leash": False,
            "description": "반려견과 함께 탑승 가능한 해운대 연안 유람선 서비스.",
            "image": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=600",
            "reviews": ["바다 구경하기 너무 좋았어요."]
        },
        {
            "id": 8,
            "name": "남산 댕댕이 노을 산책길",
            "category": "관광지",
            "region": "서울",
            "address": "서울특별시 용산구 남산공원길 105",
            "large_dog": True,
            "off_leash": False,
            "description": "서울 전경이 한눈에 보이는 반려견 선호 산책로 코스입니다.",
            "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600",
            "reviews": ["경치가 최고예요."]
        },
        {
            "id": 9,
            "name": "양평 수영장 펫리조트",
            "category": "숙소",
            "region": "경기",
            "address": "경기도 양평군 용문면 신점리 88",
            "large_dog": True,
            "off_leash": True,
            "description": "사계절 반려견 전용 미온수 수영장을 갖춘 프라이빗 리조트.",
            "image": "https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=600",
            "reviews": ["수영장이 따뜻해서 가을에도 수영 잘 했습니다."]
        },
        {
            "id": 10,
            "name": "전주 한옥마을 멍카페",
            "category": "식당/카페",
            "region": "기타",
            "address": "전라북도 전주시 완산구 태조로 12",
            "large_dog": False,
            "off_leash": True,
            "description": "고즈넉한 한옥 마당에서 반려견과 전통 차를 즐길 수 있는 카페.",
            "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=600",
            "reviews": ["사진이 너무 예쁘게 잘 나와요."]
        },
        {
            "id": 11,
            "name": "제주 멍멍 자율 렌터카",
            "category": "이동수단",
            "region": "제주",
            "address": "제주시 공항로 100",
            "large_dog": True,
            "off_leash": False,
            "description": "반려견 시트커버와 드라이룸 무료 대여 렌터카 서비스.",
            "image": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=600",
            "reviews": ["제주도 여행 시 털 묻을 걱정 없이 편하게 이용했어요."]
        },
        {
            "id": 12,
            "name": "태안 안면도 꽃지 애견공원",
            "category": "관광지",
            "region": "기타",
            "address": "충청남도 태안군 안면읍 승언리 산28",
            "large_dog": True,
            "off_leash": True,
            "description": "낙조가 아름다운 서해안 최대 규모 오프리쉬 애견공원.",
            "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600",
            "reviews": ["노을 보며 강아지가 마음껏 뛰놀았어요."]
        }
    ]

# -----------------------------------------------------------------------------
# 5. 카테고리 탭
# -----------------------------------------------------------------------------
st.write("### 🎀 카테고리로 찾아보기")

tab_all, tab_cafe, tab_stay, tab_tour, tab_trans = st.tabs([
    "🏠 전체 보기", 
    "☕ 식당/카페", 
    "🏨 숙소", 
    "🌳 관광지", 
    "🚕 이동수단"
])

# -----------------------------------------------------------------------------
# 6. 실시간 검색 및 지도 연계 표시 함수
# -----------------------------------------------------------------------------
def display_places(category_filter=None):
    places = st.session_state.places
    tab_prefix = category_filter if category_filter else "all"

    # 1. 카테고리 필터링
    if category_filter:
        places = [p for p in places if p["category"] == category_filter]
        
    # 2. 실시간 검색어 필터링 (장소명, 주소, 지역, 상세설명 통합)
    if search_query:
        q = search_query.lower()
        places = [
            p for p in places 
            if q in p["name"].lower() 
            or q in p["address"].lower() 
            or q in p["region"].lower()
            or q in p["description"].lower()
        ]

    # 3. 추가 조건 필터
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_large = st.checkbox("🐕 대형견 동반 가능만 보기", key=f"chk_large_{tab_prefix}")
    with col_f2:
        filter_off = st.checkbox("🦮 오프리쉬 구역 있음만 보기", key=f"chk_off_{tab_prefix}")

    if filter_large:
        places = [p for p in places if p["large_dog"]]
    if filter_off:
        places = [p for p in places if p["off_leash"]]

    # 검색 결과 안내
    if search_query:
        st.info(f"🔍 **'{search_query}'** 검색 결과: 총 **{len(places)}**곳")
    else:
        st.write(f"총 **{len(places)}**곳의 장소가 등록되어 있습니다.")

    st.write("")

    if not places:
        st.warning("조건에 맞는 장소가 없습니다. 다른 검색어나 카테고리를 선택해 보세요!")
    else:
        for place in places:
            with st.container():
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    st.image(place["image"], use_container_width=True)
                with col_info:
                    st.subheader(f"[{place['category']}] {place['name']}")
                    st.write(f"📍 **주소:** {place['address']} ({place['region']})")
                    
                    # 🔗 실제 지도 검색어 URL 자동 생성 (장소명 + 주소)
                    search_term = f"{place['name']} {place['address']}"
                    encoded_search = urllib.parse.quote(search_term)
                    
                    naver_url = f"https://map.naver.com/v5/search/{encoded_search}"
                    kakao_url = f"https://map.kakao.com/?q={encoded_search}"
                    
                    # 지도 연계 버튼
                    st.markdown(f"""
                        <div style="margin-bottom: 10px;">
                            <a href="{naver_url}" target="_blank" class="map-btn naver-map">🟢 네이버 지도에서 위치 확인</a>
                            <a href="{kakao_url}" target="_blank" class="map-btn kakao-map">🟡 카카오맵에서 위치 확인</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # 태그 표시
                    tags = []
                    if place["large_dog"]:
                        tags.append("🐕 대형견 가능")
                    if place["off_leash"]:
                        tags.append("🦮 오프리쉬 구역")
                    st.write(" ".join([f"`{t}`" for t in tags]) if tags else "`소형견 위주`")
                    
                    st.write(place["description"])

                    # 리뷰 보이기/작성
                    with st.expander("💬 사용자 리뷰 보기 및 작성"):
                        if place["reviews"]:
                            for r in place["reviews"]:
                                st.write(f"- {r}")
                        else:
                            st.write("아직 등록된 리뷰가 없습니다.")
                            
                        input_key = f"input_{tab_prefix}_{place['id']}"
                        btn_key = f"btn_{tab_prefix}_{place['id']}"
                        
                        new_rev = st.text_input("리뷰 작성", key=input_key)
                        if st.button("리뷰 등록", key=btn_key):
                            if new_rev.strip():
                                place["reviews"].append(new_rev.strip())
                                st.success("리뷰가 등록되었습니다!")
                                st.rerun()
                            else:
                                st.error("내용을 입력해주세요.")
            st.markdown("---")

# -----------------------------------------------------------------------------
# 7. 탭 출력 실행
# -----------------------------------------------------------------------------
with tab_all:
    display_places(category_filter=None)

with tab_cafe:
    display_places(category_filter="식당/카페")

with tab_stay:
    display_places(category_filter="숙소")

with tab_tour:
    display_places(category_filter="관광지")

with tab_trans:
    display_places(category_filter="이동수단")

# -----------------------------------------------------------------------------
# 8. [사장님 전용] 업체 등록
# -----------------------------------------------------------------------------
st.write("### 🎀 [사장님 전용] 신규 업체 등록")

with st.expander("📝 업체 등록 폼 열기"):
    with st.form("register_form_final", clear_on_submit=True):
        reg_name = st.text_input("업체/서비스명*", placeholder="예: 가평 댕댕 글램핑")
        
        c1, c2 = st.columns(2)
        with c1:
            reg_category = st.selectbox("카테고리*", ["식당/카페", "숙소", "관광지", "이동수단"])
        with c2:
            reg_region = st.selectbox("지역*", ["서울", "경기", "강원", "제주", "기타"])
            
        reg_address = st.text_input("상세 주소*", placeholder="예: 경기도 가평군 북면 가화로 100")
        
        st.write("시설 및 동반 조건")
        reg_large = st.checkbox("대형견 동반 가능 여부")
        reg_off = st.checkbox("오프리쉬 구역 보유")

        reg_desc = st.text_area("상세 설명", placeholder="이용 안내 및 주의사항")
        reg_img = st.text_input("대표 이미지 URL", value="https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600")

        submit_btn = st.form_submit_button("등록 완료하기")

        if submit_btn:
            if not reg_name.strip() or not reg_address.strip():
                st.error("업체명과 주소는 필수 입력 사항입니다.")
            else:
                new_item = {
                    "id": len(st.session_state.places) + 1,
                    "name": reg_name.strip(),
                    "category": reg_category,
                    "region": reg_region,
                    "address": reg_address.strip(),
                    "large_dog": reg_large,
                    "off_leash": reg_off,
                    "description": reg_desc.strip() if reg_desc else "상세 설명이 없습니다.",
                    "image": reg_img.strip() if reg_img.strip() else "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600",
                    "reviews": []
                }
                st.session_state.places.append(new_item)
                st.success(f"🎉 '{reg_name}' 등록이 완료되었습니다! 위 상단 탭에서 바로 지도를 연결해 보실 수 있습니다.")
