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

ICON_HAMSTER = """
<svg width="115" height="115" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="36" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="36" cy="46" r="9" fill="#d1d5db"/>
  <circle cx="84" cy="46" r="16" fill="#88929e" stroke="#2b333e" stroke-width="3.5"/>
  <circle cx="84" cy="46" r="9" fill="#d1d5db"/>
  <ellipse cx="60" cy="72" rx="40" ry="34" fill="#9ca3af" stroke="#2b333e" stroke-width="3.5"/>
  <ellipse cx="60" cy="79" rx="20" ry="16" fill="#f3f4f6"/>
  <circle cx="45" cy="67" r="4" fill="#1f2937"/>
  <circle cx="75" cy="67" r="4" fill="#1f2937"/>
  <ellipse cx="60" cy="74" rx="4" ry="3" fill="#374151"/>
  <path d="M57 77 Q 60 80 63 77" stroke="#374151" stroke-width="2.5" fill="none"/>
  <line x1="26" y1="75" x2="37" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="27" y1="81" x2="38" y2="79" stroke="#2b333e" stroke-width="2"/>
  <line x1="83" y1="75" x2="94" y2="75" stroke="#2b333e" stroke-width="2"/>
  <line x1="82" y1="79" x2="93" y2="81" stroke="#2b333e" stroke-width="2"/>
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

# 5. 메인 레이아웃 (좌측 캐릭터 - 중앙 검색바/지도 - 우측 캐릭터)
col_left, col_center, col_right = st.columns([1.2, 5.5, 1.2])

with col_left:
    st.markdown(f"""
        <div class="character-box">
            <div>{ICON_PAW}</div>
            <div>{ICON_DOG}</div>
        </div>
    """, unsafe_allow_html=True)

with col_center:
    # 사진과 동일한 통합 검색창
    search_query = st.text_input(
        label="search",
        placeholder="🔍 반려동물 크기, 위치, 숙소 형태 등을 입력해 주세요",
        label_visibility="collapsed"
    )
    
    # 실제 구글 검색 및 지도 쿼리 생성
    raw_query = search_query.strip()
    actual_search_target = raw_query if raw_query else "불당동 반려동물 동반 숙소"
    
    # 숙소 관련 키워드가 누락되어 있으면 검색 결과 정확도를 위해 자동 결합
    google_keyword = actual_search_target
    if not any(word in google_keyword for word in ["숙소", "호텔", "펜션", "동반", "애견"]):
        google_keyword += " 반려동물 동반 숙소"

    encoded_google = urllib.parse.quote(google_keyword)
    google_web_search_url = f"https://www.google.com/search?q={encoded_google}"
    google_maps_search_url = f"https://www.google.com/maps/search/{encoded_google}"

    # 실제 구글 검색 바로가기 버튼 제공 (입력 후 클릭 시 새 창에서 실제 구글 검색 결과 오픈)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.link_button(f"🌐 구글 포털에서 '{actual_search_target}' 실제 검색", google_web_search_url, use_container_width=True)
    with btn_col2:
        st.link_button(f"📍 구글 지도에서 '{actual_search_target}' 실제 검색", google_maps_search_url, use_container_width=True)

    # 중앙 화면에 실제 구글 지도 결과 즉시 렌더링
    google_map_embed_url = f"https://maps.google.com/maps?q={encoded_google}&t=&z=14&ie=UTF8&iwloc=&output=embed"
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

# 6. 세부 필터 (선택 옵션)
with st.expander("⚙️ 세부 옵션 필터 (반려동물 종류 / 크기 / 숙소 형태)", expanded=False):
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        pet_kind = st.selectbox("동반 동물 종류", ["전체", "강아지", "고양이", "소동물(토끼/친칠라)"])
    with f_col2:
        size_filter = st.selectbox("반려동물 크기", ["전체", "소형견 (7kg 이하)", "중형견 (15kg 이하)", "대형견 (15kg 초과)"])
    with f_col3:
        stay_type_filter = st.selectbox("숙소 형태", ["전체", "호텔", "풀빌라", "글램핑", "펜션/독채", "에어비앤비/원룸"])

# 7. 내부 데이터베이스 매칭 필터링
filtered_df = df.copy()

if raw_query:
    q = raw_query.lower()
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

# 8. 앱 내 등록 숙소 카드 리스트
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(f"✨ 추천 등록 숙소 ({len(filtered_df)}건)")

if filtered_df.empty:
    st.info(f"등록 데이터베이스에는 매칭되는 숙소가 없으나, 위의 **'🌐 구글 포털에서 검색'** 및 **'📍 구글 지도에서 검색'** 버튼을 통해 구글 전체 실시간 검색 결과를 즉시 확인하실 수 있습니다.")
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
            
            # 개별 숙소 구글 실제 지도 바로가기
            target_map_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(row['name'] + ' ' + row['full_address'])}"
            st.link_button(f"🗺️ '{row['name']}' 구글 지도 바로 확인", target_map_url, use_container_width=True)
