import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. Page Configuration & Initial State Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="멍트래블 - 반려견 동반 여행 정보",
    page_icon="🐾",
    layout="wide"
)

# 기본 시범 데이터 초기화
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

# -----------------------------------------------------------------------------
# 2. Main Title & Navigation Bar
# -----------------------------------------------------------------------------
st.title("🐾 멍트래블 (Puppy Travel Hub)")
st.caption("반려견과 함께하는 행복한 여행! 업체 탐색부터 AI 일정 추천까지 한번에 해결하세요.")

menu = st.sidebar.radio("원하는 작업을 선택하세요", ["장소 탐색하기", "사장님 업체 등록", "AI 반려견 여행 AI 가이드"])

# -----------------------------------------------------------------------------
# 3. Menu 1: 장소 탐색하기
# -----------------------------------------------------------------------------
if menu == "장소 탐색하기":
    st.header("🔎 동반 가능 업체 및 이동수단 탐색")
    
    # 검색 및 필터 옵션
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    with col_filter1:
        selected_category = st.selectbox("카테고리 선택", ["전체", "식당/카페", "숙소", "이동수단", "관광지/놀이터"])
    with col_filter2:
        selected_region = st.selectbox("지역 선택", ["전체", "서울", "경기", "강원", "제주", "기타"])
    with col_filter3:
        st.write("맞춤 조건 필터")
        filter_large_dog = st.checkbox("대형견 동반 가능")
        filter_off_leash = st.checkbox("오프리쉬 구역 있음")

    # 데이터 필터링 적용
    filtered_places = st.session_state.places
    if selected_category != "전체":
        filtered_places = [p for p in filtered_places if p["category"] == selected_category]
    if selected_region != "전체":
        filtered_places = [p for p in filtered_places if p["region"] == selected_region]
    if filter_large_dog:
        filtered_places = [p for p in filtered_places if p["large_dog"]]
    if filter_off_leash:
        filtered_places = [p for p in filtered_places if p["off_leash"]]

    st.markdown("---")
    st.subheader(f"총 {len(filtered_places)}개의 장소를 찾았습니다.")

    # 목록 표시 (2열 카드 형태 layout)
    if not filtered_places:
        st.warning("조건에 맞는 장소가 없습니다. 필터를 변경해보세요.")
    else:
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

# -----------------------------------------------------------------------------
# 4. Menu 2: 사장님 업체 등록
# -----------------------------------------------------------------------------
elif menu == "사장님 업체 등록":
    st.header("📝 사장님 전용 - 애견 동반 장소/수단 등록")
    st.info("등록하신 정보는 사용자들이 확인할 수 있도록 탐색 목록에 즉시 반영됩니다.")

    with st.form("register_form", clear_on_submit=True):
        name = st.text_input("업체/서비스명*", placeholder="예: 멍멍 펜션, 댕댕 파크")
        
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("카테고리*", ["식당/카페", "숙소", "이동수단", "관광지/놀이터"])
        with col2:
            region = st.selectbox("지역*", ["서울", "경기", "강원", "제주", "기타"])
            
        address = st.text_input("상세 주소 또는 운행 구역*", placeholder="예: 강원도 강릉시 해안로 123")
        
        st.write("시설 및 이용 동반 조건")
        c_large = st.checkbox("대형견 동반 가능 여부")
        c_off = st.checkbox("오프리쉬(목줄 착용 불필요) 구역 보유")

        description = st.text_area("상세 설명", placeholder="반려견을 위한 부대시설이나 이용 수칙을 작성해주세요.")
        image_url = st.text_input("대표 이미지 URL", value="https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600")

        submitted = st.form_submit_button("등록 완료하기")

        if submitted:
            if not name.strip() or not address.strip():
                st.error("업체명과 주소는 필수 입력 사항입니다.")
            else:
                new_id = len(st.session_state.places) + 1
                new_place = {
                    "id": new_id,
                    "name": name.strip(),
                    "category": category,
                    "region": region,
                    "address": address.strip(),
                    "large_dog": c_large,
                    "off_leash": c_off,
                    "description": description.strip() if description else "상세 설명이 없습니다.",
                    "image": image_url if image_url.strip() else "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=600",
                    "reviews": []
                }
                st.session_state.places.append(new_place)
                st.success(f"'{name}' 등록이 완료되었습니다! [장소 탐색하기] 탭에서 확인하세요.")

# -----------------------------------------------------------------------------
# 5. Menu 3: AI 반려견 여행 AI 가이드 (Gemini API)
# -----------------------------------------------------------------------------
elif menu == "AI 반려견 여행 AI 가이드":
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
