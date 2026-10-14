import streamlit as st
st.title('숙소 찾기')
st.write('원하는 숙소를 찾아보세요!')
import streamlit as st
import pandas as pd
import urllib.parse

# 1. 페이지 설정
st.set_page_config(
    page_title="PetStay - 반려동물 동반 숙소 검색",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"  # 이미지 시안처럼 깔끔한 중앙 집중형 화면을 위해 기본 접힘
)

# 2. 사진 디자인을 그대로 구현한 커스텀 CSS
st.markdown("""
    <style>
    /* 전체 배경을 사진과 동일한 포근한 크림 톤으로 설정 */
    .stApp {
        background-color: #faf6ef;
        font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    }
    
    /* 상단 기본 헤더 및 패딩 조정 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* 시안 속 둥근 캡슐형 검색바 스타일링 */
    div[data-testid="stTextInput"] > div > div {
        background-color: #ffffff !important;
        border: 2.5px solid #6b7280 !important;
        border-radius: 40px !important;
        box-shadow: 0px 8px 18px rgba(0, 0, 0, 0.08) !important;
        height: 62px;
        padding-left: 15px;
    }
    
    div[data-testid="stTextInput"] input {
        font-size: 1.12rem !important;
        color: #1f2937 !important;
        font-weight: 500;
    }

    /* 사진 속 둥근 모서리의 중앙 지도 컨테이너 */
    .map-frame-wrapper {
        border-radius: 28px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.09);
        border: 4px solid #ffffff;
        background-color: #e5e7eb;
        margin-top: 10px;
    }

    /* 캐릭터 및 발자국 아이콘 컨테이너 */
    .character-box {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 480px;
        padding: 10px 0;
    }

    /* 하단 결과 숙소 카드 */
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
        color: #8b5cf6;
        padding: 4px 9px;
        border-radius: 10px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 고화질 벡터 일러스트레이션 (시안 사진의 4개 캐릭터 재현)
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
  <!-- 귀 -->
  <ellipse cx="28" cy="62" rx="16" ry="24" fill="#a46d50" stroke="#3d2314" stroke-width="3.5" transform="rotate(-15 28 62)"/>
  <ellipse cx="92" cy="62" rx="16" ry="24" fill="#a46d50" stroke="#3d2314" stroke-width="3.5" transform="rotate(15 92 62)"/>
  <!-- 얼굴 -->
  <ellipse cx="60" cy="70" rx="42" ry="36" fill="#faebd7" stroke="#3d2314" stroke-width="3.5"/>
  <!-- 눈 주위 반점 -->
  <ellipse cx="76" cy="64" rx="14" ry="12" fill="#a46d50" opacity="0.85"/>
  <!-- 눈 -->
  <circle cx="45" cy="64" r="4.5" fill="#3d2314"/>
  <circle cx="75" cy="64" r="4.5" fill="#3d2314"/>
  <!-- 코와 입 -->
  <ellipse cx="60" cy="74" rx="5" ry="4" fill="#3d2314"/>
  <path d="M54 78 Q 60 83 66 78" stroke="#3d2314" stroke-width="3" fill="none"/>
  <!-- 혀 -->
  <path d="M57 80 Q 60 89 63 80 Z" fill="#f87171"/>
</svg>
"""

ICON_RABBIT = """
<svg width="115" height="115" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 귀 -->
  <ellipse cx="44" cy="36" rx="11" ry="28" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5" transform="rotate(-8 44 36)"/>
  <ellipse cx="44" cy="36" rx="6" ry="20" fill="#fbcfe8" transform="rotate(-8 44 36)"/>
  <ellipse cx="76" cy="36" rx="11" ry="28" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5" transform="rotate(8 76 36)"/>
  <ellipse cx="76" cy="36" rx="6" ry="20" fill="#fbcfe8" transform="rotate(8 76 36)"/>
  <!-- 얼굴 -->
  <ellipse cx="60" cy="76" rx="38" ry="32" fill="#fdf2e9" stroke="#452c1e" stroke-width="3.5"/>
  <!-- 볼터치 -->
  <circle cx="38" cy="80" r="5" fill="#fca5a5" opacity="0.6"/>
  <circle cx="82" cy="80" r="5" fill="#fca5a5" opacity="0.6"/>
  <!-- 눈 -->
  <circle cx="47" cy="73" r="4" fill="#452c1e"/>
  <circle cx="73" cy="73" r="4" fill="#452c1e"/>
  <!-- 코/입 -->
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
<svg width="115" height="115" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- 귀 -->
  <circle cx="36" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="36" cy="46" r="9" fill="#d1d5db"/>
  <circle cx="84" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="84" cy="46" r="9" fill="#d1d5db"/>
  <!-- 얼굴 -->
  <ellipse cx="60" cy="72" rx="40" ry="34" fill="#9ca3af" stroke="#2b333e" stroke-width="3.5"/>
  <!-- 주둥이 흰 부분 -->
  <ellipse cx="60" cy="79" rx="20" ry="16" fill="#f3f4f6"/>
  <!-- 눈 -->
  <circle cx="45" cy="67" r="4" fill="#1f2937"/>
  <circle cx="75" cy="67" r="4" fill="#1f2937"/>
  <!-- 코/입 -->
  <ellipse cx="60" cy="74" rx="4" ry="3" fill="#374151"/>
  <path d="M57 77 Q 60 80 63 77" stroke="#374151" stroke-width="2.5" fill="none"/>
  <!-- 수염 -->
  <line x1="26" y1="75" x2="37" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="27" y1="81" x2="38" y2="79" stroke="#2b333e" stroke-width="2"/>
  <line x1="83" y1="75" x2="94" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="82" y1="79" x2="93" y2="81" stroke="#2b333e" stroke-width="2"/>
</svg>
"""

# 4. 숙소 데이터베이스 (예시: 불당동, 제주, 가평, 해운대 등)
@st.cache_data
def get_stays_data():
    return pd.DataFrame([
        {
            "id": 1,
            "name": "천안 불당 펫파크 하우스",
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
            "name": "가평 포레스트 펫 글램핑",
            "region": "가평",
            "full_address": "경기도 가평군 북면",
            "stay_type": "글램핑",
            "allowed_pets": ["강아지"],
            "max_weight": "중형견 (15kg 이하)",
            "amenities": ["독채 잔디마당", "불멍존", "바비큐"],
            "price": 160000,
            "rating": 4.7,
            "image": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=600&auto=format&fit=crop&q=80"
        },
        {
            "id": 5,
            "name": "해운대 오션 냥스테이",
            "region": "부산",
            "full_address": "부산광역시 해운대구 우동",
            "stay_type": "에어비앤비/원룸",
            "allowed_pets": ["고양이", "소동물(토끼/친칠라)"],
            "max_weight": "소형견 (7kg 이하)",
            "amenities": ["캣타워 구비", "방충망 안심시설"],
            "price": 120000,
            "rating": 4.85,
            "image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600&auto=format&fit=crop&q=80"
        }
    ])

df = get_stays_data()

# 5. 사진 레이아웃 메인 화면 (좌측 동물 - 중앙 검색바/지도 - 우측 동물)
col_left, col_center, col_right = st.columns([1.2, 5.5, 1.2])

with col_left:
    st.markdown(f"""
        <div class="character-box">
            <div>{ICON_PAW}</div>
            <div>{ICON_DOG}</div>
        </div>
    """, unsafe_allow_html=True)

with col_center:
    # 사진과 동일한 통합 검색창 (아이콘 + placeholder)
    search_query = st.text_input(
        label="search",
        placeholder="🔍 반려동물 크기, 위치, 숙소 형태 등을 입력해 주세요",
        label_visibility="collapsed"
    )
    
    # 지도 검색 키워드 결정 (사진의 기본값은 '불당동')
    map_location = search_query.strip() if search_query.strip() else "천안시 불당동"
    encoded_loc = urllib.parse.quote(map_location + " 숙소")
    google_map_embed_url = f"https://maps.google.com/maps?q={encoded_loc}&t=&z=14&ie=UTF8&iwloc=&output=embed"

    # 사진 속 둥근 모서리 구글 지도
    st.markdown(f"""
        <div class="map-frame-wrapper">
            <iframe width="100%" height="450" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{google_map_embed_url}"></iframe>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"""
        <div class="character-box">
            <div>{ICON_RABBIT}</div>
            <div>{ICON_HAMSTER}</div>
        </div>
    """, unsafe_allow_html=True)

# 6. 상세 검색 필터 토글 (선택 옵션)
with st.expander("⚙️ 세부 상세 필터 설정 (반려동물 크기 / 시설 조건 / 숙소 형태)", expanded=False):
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        pet_kind = st.selectbox("동반 동물 종류", ["전체", "강아지", "고양이", "소동물(토끼/친칠라)"])
    with f_col2:
        size_filter = st.selectbox("반려동물 크기", ["전체", "소형견 (7kg 이하)", "중형견 (15kg 이하)", "대형견 (15kg 초과)"])
    with f_col3:
        stay_type_filter = st.selectbox("숙소 형태", ["전체", "호텔", "풀빌라", "글램핑", "펜션/독채", "에어비앤비/원룸"])

# 7. 검색 필터링 엔진 로직
filtered_df = df.copy()

if search_query.strip():
    q = search_query.strip().lower()
    # 검색어가 지역, 이름, 숙소 형태, 허용 동물, 시설 등에 매칭되는지 다중 체크
    filtered_df = filtered_df[filtered_df.apply(
        lambda row: q in row["name"].lower() or 
                    q in row["region"].lower() or 
                    q in row["stay_type"].lower() or 
                    any(q in pet.lower() for pet in row["allowed_pets"]) or 
                    any(q in am.lower() for am in row["amenities"]), axis=1
    )]

if pet_kind != "전체":
    filtered_df = filtered_df[filtered_df["allowed_pets"].apply(lambda pets: pet_kind in pets)]

if size_filter != "전체":
    size_levels = {"소형견 (7kg 이하)": 1, "중형견 (15kg 이하)": 2, "대형견 (15kg 초과)": 3}
    filtered_df = filtered_df[filtered_df["max_weight"].apply(lambda w: size_levels.get(w, 1) >= size_levels[size_filter])]

if stay_type_filter != "전체":
    filtered_df = filtered_df[filtered_df["stay_type"].str.contains(stay_type_filter)]

# 8. 하단 맞춤 숙소 카드 리스트
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(f"✨ 추천 숙소 리스트 ({len(filtered_df)}건)")

if filtered_df.empty:
    st.info("검색 조건에 맞는 숙소가 없습니다. 상단 검색창에 '불당동', '제주', '대형견' 등으로 다시 검색해 보세요!")
else:
    card_cols = st.columns(2)
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        with card_cols[idx % 2]:
            badges_html = "".join([f"<span class='badge'>{am}</span>" for am in row["amenities"]])
            pets_allowed_str = ", ".join(row["allowed_pets"])
            st.markdown(f"""
                <div class="stay-card">
                    <img src="{row['image']}" style="width:100%; height:200px; object-fit:cover; border-radius:14px; margin-bottom:12px;">
                    <div style="font-size:1.2rem; font-weight:700; color:#1e293b; margin-bottom:4px;">{row['name']}</div>
                    <div style="font-size:0.9rem; color:#64748b; margin-bottom:8px;">📍 {row['full_address']} | ⭐ {row['rating']}</div>
                    <div style="font-size:0.85rem; color:#475569; margin-bottom:8px;">🐾 동반 가능: <b>{pets_allowed_str}</b> ({row['max_weight']})</div>
                    <div style="margin-bottom:12px;">{badges_html}</div>
                    <div style="font-size:1.15rem; font-weight:800; color:#d97706; text-align:right;">₩{row['price']:,} / 1박</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 구글 지도 상세 이동 링크
            target_map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(row['name'] + ' ' + row['full_address'])}"
            st.link_button(f"🗺️ '{row['name']}' 실제 위치 구글 지도로 열기", target_map_url, use_container_width=True)
