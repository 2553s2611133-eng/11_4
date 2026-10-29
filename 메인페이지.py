import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 세션 데이터 초기화
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="멍트래블 - 반려견 동반 여행 정보",
    page_icon="🐾",
    layout="wide"
)

# 기본 시범 데이터 세팅
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
            "name": "댕댕이 해변 공원",
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

# -----------------------------------------------------------------------------
# 2. 메인 헤더 및 검색창 영역
# -----------------------------------------------------------------------------
st.title("🐾 멍트래블 (Puppy Travel Hub)")

# 안내 배너
st.info("🐶 **안녕하세요! 반려견과 행복한 여행을 시작해개!** \n\n우리 댕댕이가 좋아하는 오프리쉬 놀이터부터 편안한 펜션, 펫택시까지 한눈에 확인해보세요!")

# 통합 검색창
search_keyword = st.text_input("🔎 검색어 입력", placeholder="강아지와 가고 싶은 곳의 이름이나 지역을 입력해보세요 (예: 펜션, 강릉, 바다)").strip()

st.write("---")

# -----------------------------------------------------------------------------
# 3. 카테고리 탭 (상단 이동/선택 메뉴)
# -----------------------------------------------------------------------------
tab_all, tab_cafe, tab_stay, tab_tour, tab_trans, tab_register = st.tabs([
    "🏠 전체 보기", 
    "☕ 식당/카페", 
    "🏨 숙소", 
    "🌳 관광지", 
    "🚕 이동수단", 
    "📝 [사장님] 업체 등록"
])

# 공통 장소 표시 함수 (오류 없이 반복 출력을 위해 정의)
def display_places(category_filter=None):
    places = st.session_state.places
    
    # 1. 카테고리 필터링
    if category_filter:
        places = [p for p in places if p["category"] == category_filter]
        
    # 2. 검색어 필터링
    if search_keyword:
        places = [
            p for p in places 
            if search_keyword.lower() in p["name"].lower() 
            or search_keyword.lower() in p["address"].lower()
            or search_keyword.lower() in p["description"].lower()
        ]

    # 조건 검색 필터 (대형견/오프리쉬)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_large = st.checkbox("🐕 대형견 동반 가능만 보기", key=f"chk_large_{category_filter}")
    with col_f2:
        filter_off = st.checkbox("🦮 오프리쉬 구역 있음만 보기", key=f"chk_off_{category_filter}")

    if filter_large:
        places = [p for p in places if p["large_dog"]]
    if filter_off:
        places = [p for p in places if p["off_leash"]]

    st.write(f"총 **{len(places)}**곳의 장소가 있습니다.")
    st.write("")

    if not places:
        st.warning("조건에 맞는 장소가 없습니다. 다른 검색어나 필터를 선택해보세요!")
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

                    # 리뷰 보이기/작성
                    with st.expander("💬 사용자 리뷰 보기 및 작성"):
                        if place["reviews"]:
                            for r in place["reviews"]:
                                st.write(f"- {r}")
                        else:
                            st.write("아직 등록된 리뷰가 없습니다. 첫 리뷰를 작성해보세요!")
                            
                        new_rev = st.text_input("리뷰 작성", key=f"input_rev_{place['id']}")
                        if st.button("리뷰 등록", key=f"btn_rev_{place['id']}"):
                            if new_rev.strip():
                                place["reviews"].append(new_rev.strip())
                                st.success("리뷰가 등록되었습니다!")
                                st.rerun()
                            else:
                                st.error("내용을 입력해주세요.")
            st.markdown("---")

# -----------------------------------------------------------------------------
# 4. 각 탭별 화면 출력
# -----------------------------------------------------------------------------
with tab_all:
    st.header("🏠 전체 등록 장소")
    display_places(category_filter=None)

with tab_cafe:
    st.header("☕ 애견 동반 식당 및 카페")
    display_places(category_filter="식당/카페")

with tab_stay:
    st.header("🏨 애견 동반 숙소 및 펜션")
    display_places(category_filter="숙소")

with tab_tour:
    st.header("🌳 애견 동반 관광지 및 놀이터")
    display_places(category_filter="관광지")

with tab_trans:
    st.header("🚕 펫택시 및 이동수단")
    display_places(category_filter="이동수단")

# -----------------------------------------------------------------------------
# 5. [사장님] 업체 등록 탭
# -----------------------------------------------------------------------------
with tab_register:
    st.header("📝 사장님 전용 업체/이동수단 등록")
    st.success("사장님이 직접 등록하신 장소는 [전체 보기] 및 해당 카테고리 탭에 즉시 반영됩니다!")

    with st.form("register_form_clean", clear_on_submit=True):
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
                st.success(f"🎉 '{reg_name}' 등록이 완료되었습니다! 상단 탭에서 확인해 보세요.")
