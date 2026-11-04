import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS (귀여운 느낌 테마)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="함께 가개 - 반려견 동반 여행 정보",
    page_icon="🐾",
    layout="wide"
)

# 귀여운 테마 커스텀 CSS (이미지 느낌 반영)
st.markdown("""
    <style>
    /* 전체 배경색 - 따뜻한 크림/베이지 톤 (이미지 반영) */
    .stApp {
        background-color: #F8F5F0;
    }
    
    /* 사이드바 제거 및 메인 콘텐츠 집중 */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* 폰트 설정 (둥글고 친근한 폰트 스택) */
    html, body, [class*="css"]  {
        font-family: 'Comic Sans MS', 'GmarketSansBold', sans-serif;
        color: #6D4C41;
    }

    /* 메인 타이틀 디자인 (이미지 반영) */
    h1 {
        color: #6D4C41 !important;
        font-family: 'Comic Sans MS', 'GmarketSansBold', sans-serif;
        text-align: center;
        margin-top: 0;
    }

    /* 검색 바 디자인 (이미지 반영) */
    .stTextInput>div>div>input {
        border-radius: 30px !important;
        border: 2px solid #D7C9A3 !important;
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

    /* 인기 동반 명소 카드 디자인 (이미지 반영) */
    .destination-card {
        background-color: white;
        border-radius: 20px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid #FFF3E0;
        margin: 10px;
    }
    .destination-card img {
        border-radius: 15px;
        width: 100%;
        height: auto;
    }
    .destination-card .title {
        font-weight: bold;
        color: #6D4C41;
        font-size: 1rem;
        margin-top: 5px;
    }
    
    /* 카테고리 버튼 디자인 (이미지 반영) */
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

    /* 버튼 스타일 - 동글동글하고 아기자기하게 */
    .stButton>button {
        border-radius: 20px !important;
        background-color: #D7C9A3 !important;
        color: #5D4037 !important;
        border: 2px solid #A18D74 !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #A18D74 !important;
        color: white !important;
        transform: scale(1.05);
    }

    /* 웰컴 배너 디자인 (이미지 반영) */
    .welcome-banner {
        background-color: #D7C9A3;
        padding: 20px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 3px dashed #A18D74;
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
    
    /* 탭 스타일 둥글게 */
    div[data-baseweb="tab-list"] {
        border-radius: 30px !important;
        overflow: hidden;
    }
    div[data-baseweb="tab"] {
        background-color: white !important;
        color: #6D4C41 !important;
        border-radius: 30px 30px 0 0 !important;
        padding: 10px 20px !important;
    }
    div[data-baseweb="tab-active"] {
        background-color: #D7C9A3 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Main Title, Profile, and Search Bar (이미지 반영)
# -----------------------------------------------------------------------------
# 상단 프로필 및 환영 메시지 (이미지 반영)
col_head, col_empty = st.columns([3, 1])
with col_head:
    st.markdown("""
        <div style="display: flex; align-items: center;">
            <div style="font-size: 3rem; margin-right: 15px;">👤</div>
            <div>
                <h3 style="margin: 0; color: #6D4C41;">안녕하세요, 알렉스! 👋</h3>
                <p style="margin: 0; color: #8D6E63;">함께 가개 🐾 (Together Go Doggy)</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with col_empty:
    st.write("Current time 10:09 ⚙️")

# 검색 바 (이미지 반영)
search_query = st.text_input("", placeholder="어디로 함께 갈까요? 🐾", key="main_search")

# 웰컴 배너 (이미지 반영)
st.markdown("""
    <div class="welcome-banner">
        <h2>🐶 안녕하세요! 반려견과 행복한 여행을 시작해개! 🐾</h2>
        <p>우리 댕댕이가 좋아하는 오프리쉬 놀이터부터 편안한 펜션, 펫택시까지 한눈에 확인해 보세요!</p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Trending Destinations (인기 동반 명소) (이미지 반영)
# -----------------------------------------------------------------------------
st.write("### 🎀 인기 동반 명소")

# 인기 동반 명소 데이터
destinations = [
    {"name": "경복궁 한복 산책", "image": "https://images.unsplash.com/photo-1594917409204-747f5255474a?w=400"},
    {"name": "부산 달맞이길 카페", "image": "https://images.unsplash.com/photo-1627916327663-1d07914f6d4d?w=400"},
    {"name": "제주 오름 트레킹", "image": "https://images.unsplash.com/photo-1594191370967-b52e3914a5d8?w=400"}
]

cols_dest = st.columns(3)

for idx, col in enumerate(cols_dest):
    dest = destinations[idx]
    with col:
        # 카드 디자인 (HTML/CSS)
        st.markdown(f"""
            <div class="destination-card">
                <img src="{dest['image']}" alt="{dest['name']}">
                <div class="title">{dest['name']}</div>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# -----------------------------------------------------------------------------
# 4. Find your trip by (카테고리 탭 대용) (이미지 반영)
# -----------------------------------------------------------------------------
st.write("### 🎀 카테고리로 빠르게 찾아보개!")

# 각 카테고리의 클릭 상태를 저장하기 위한 세션 상태 초기화
if "active_category" not in st.session_state:
    st.session_state.active_category = None

# 5개 카테고리 데이터
categories = [
    {"name": "식당/카페", "icon": "☕", "key": "restaurant"},
    {"name": "숙소", "icon": "🏨", "key": "lodging"},
    {"name": "관광지", "icon": "🌳", "key": "sightseeing"},
    {"name": "이동수단", "icon": "🚕", "key": "transport"},
    {"name": "전체 보기", "icon": "🏠", "key": "all"}
]

# 5열 배치
cols_cat = st.columns(5)

for idx, col in enumerate(cols_cat):
    cat = categories[idx]
    with col:
        # 카드 디자인 (HTML/CSS)
        st.markdown(f"""
            <div class="category-card">
                <div class="icon">{cat["icon"]}</div>
                <div class="title">{cat["name"]}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # 실제 클릭 인터랙션을 위한 버튼 (디자인은 카드에 숨김)
        if st.button("", key=f"btn_cat_{cat['key']}", help=cat["name"]):
            st.session_state.active_category = cat["key"]
            st.rerun()

st.write("---")

# -----------------------------------------------------------------------------
# 5. Your Upcoming Trip (여행 계획 섹션) (이미지 반영)
# -----------------------------------------------------------------------------
st.write("### 🎀 Your Upcoming Trip")

with st.container():
    c_map, c_info = st.columns([1, 2])
    with c_map:
        # 시각적인 지도 카드 (이미지 반영)
        st.markdown("""
            <div style="background-color: white; border-radius: 20px; padding: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #FFF3E0;">
                <div style="font-size: 5rem;">🗺️</div>
                <div style="font-weight: bold; color: #6D4C41; margin-top: 10px;">서울 종로 한옥마을</div>
                <div style="color: #8D6E63; font-size: 0.9rem;">Current: 10:09, ⚙️</div>
            </div>
        """, unsafe_allow_html=True)
    with c_info:
        # 여행 계획 목록 (이미지 반영)
        places = [
            "1. 한복 대여 (강아지용!) ✅",
            "2. 남산 케이블카 예약 ✅",
            "3. 한옥 민박 체크인 ⏰"
        ]
        st.markdown("""
            <div style="background-color: white; border-radius: 20px; padding: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 2px solid #FFF3E0; height: 100%;">
                <h4 style="color: #6D4C41; margin: 0 0 10px 0;">여행 계획 목록</h4>
                <ul style="color: #8D6E63; list-style-type: none; padding: 0;">
        """ + "".join([f"<li>{p}</li>" for p in places]) + """
                </ul>
            </div>
        """, unsafe_allow_html=True)

st.write("---")

# -----------------------------------------------------------------------------
# 6. 업체 탐색 및 리뷰 섹션 (카테고리 클릭 시 결과 표시)
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

# 공통 장소 표시 함수 (중복 Key 오류 원천 해결)
def display_places(category_filter=None):
    places = st.session_state.places
    
    # 탭 구분을 위한 고유 접두사 설정
    tab_prefix = category_filter if category_filter else "all"

    # 1. 카테고리 필터링
    if category_filter:
        places = [p for p in places if p["category"] == category_filter]
        
    # 2. 검색어 필터링
    if search_query.strip():
        places = [
            p for p in places 
            if search_query.lower() in p["name"].lower() 
            or search_query.lower() in p["address"].lower()
            or search_query.lower() in p["description"].lower()
        ]

    # 조건 검색 필터 (대형견/오프리쉬)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_large = st.checkbox("🐕 대형견 동반 가능만 보기", key=f"chk_large_{tab_prefix}")
    with col_f2:
        filter_off = st.checkbox("🦮 오프리쉬 구역 있음만 보기", key=f"chk_off_{tab_prefix}")

    if filter_large:
        places = [p for p in places if p["large_dog"]]
    if filter_off:
        places = [p for p in places if p["off_leash"]]

    st.write(f"총 **{len(places)}**곳의 장소가 있습니다.")
    st.write("")

    if not places:
        st.warning("조건에 맞는 장소가 없습니다. 다른 검색어나 필터를 선택해 보세요!")
    else:
        for place in places:
            with st.container():
                col_img, col_info = st.columns([1, 2])
                with col_img:
                    st.image(place["image"], use_container_width=True)
                with col_info:
                    st.subheader(f"[{place['category']}] {place['name']}")
                    st.write(f"📍 **주소:** {place['address']} ({place['region']})")
                    
                    # 태그 표시
                    tags = []
                    if place["large_dog"]:
                        tags.append("🐕 대형견 가능")
                    if place["off_leash"]:
                        tags.append("🦮 오프리쉬 구역")
                    st.write(" ".join([f"`{t}`" for t in tags]) if tags else "`소형견 위주`")
                    
                    st.write(place["description"])

                    # 리뷰 보이기/작성 (탭 이름과 장소 ID를 결합하여 완벽하게 고유한 Key 적용)
                    with st.expander("💬 사용자 리뷰 보기 및 작성"):
                        if place["reviews"]:
                            for r in place["reviews"]:
                                st.write(f"- {r}")
                        else:
                            st.write("아직 등록된 리뷰가 없습니다. 첫 리뷰를 작성해보세요!")
                            
                        # 입력창 및 버튼 key 고유화
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

# 기능 실행 영역 (카테고리 클릭 시 하단에 표시)
active_cat = st.session_state.active_category

# 카테고리가 선택되었을 때만 기능 표시
if active_cat:
    # 카테고리 이름 가져오기
    cat_name = next((c["name"] for c in categories if c["key"] == active_cat), "장소")
    st.header(f"🔎 '{cat_name}' 탐색 결과")
    
    if active_cat == "all":
        display_places(category_filter=None)
    else:
        display_places(category_filter=cat_name)

# 카테고리가 선택되지 않았을 때 초기 화면
else:
    st.info("위의 카테고리 카드나 검색 바를 이용하여 원하는 장소를 찾아보세요!")

st.write("---")

# -----------------------------------------------------------------------------
# 7. 사장님 전용 업체 등록 (하단 통합) (이미지 반영)
# -----------------------------------------------------------------------------
st.write("### 🎀 [사장님 전용] 업체 등록 및 수정")

with st.expander("📝 업체 등록 폼 열기/닫기"):
    st.success("사장님이 직접 등록하신 장소는 '함께 가개' 전체 보기 및 카테고리 탭에 즉시 반영됩니다!")

    with st.form("register_form_final", clear_on_submit=True):
        reg_name = st.text_input("업체/서비스명*", placeholder="예: 멍멍 펜션, 댕댕 파크")
        
        c1, c2 = st.columns(2)
        with c1:
            reg_category = st.selectbox("카테고리*", ["식당/카페", "숙소", "관광지", "이동수단"])
        with c2:
            reg_region = st.selectbox("지역*", ["서울", "경기", "강원", "제주", "기타"])
            
        reg_address = st.text_input("상세 주소 또는 운행 구역*", placeholder="예: 강원도 강릉시 해안로 123")
        
        st.write("시설 및 동반 조건")
        reg_large = st.checkbox("대형견 동반 가능 여부")
        reg_off = st.checkbox("오프리쉬(목줄 착용 불필요) 구역 보유")

        reg_desc = st.text_area("상세 설명", placeholder="반려견을 위한 부대시설이나 이용 수칙을 적어주세요.")
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
                st.success(f"🎉 '{reg_name}' 등록이 완료되었습니다! 상단 카테고리에서 확인해 보세요.")
