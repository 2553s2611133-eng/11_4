
import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="함께가개 | 반려동물 동반 검색",
    page_icon="🐾",
    layout="wide",
)

# -----------------------------------------------
# 1. 예시 데이터
# 실제 업체 정보가 아닌 UI 확인용 샘플입니다.
# -----------------------------------------------
ITEMS = [
    {
        "id": "place_01",
        "name": "초록마루 애견카페",
        "kind": "카페",
        "region": "서울",
        "address": "서울 지역 예시 주소",
        "pets": ["강아지"],
        "sizes": ["소형", "중형"],
        "indoor": "실내 동반 조건 확인 필요",
        "price": "메뉴별 상이",
        "description": "반려견과 함께 쉬어 가는 카페 유형",
        "tags": ["카페", "휴식", "실내"],
        "image": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=900",
        "type": "장소",
    },
    {
        "id": "place_02",
        "name": "댕댕 테라스 식당",
        "kind": "식당",
        "region": "경기",
        "address": "경기 지역 예시 주소",
        "pets": ["강아지"],
        "sizes": ["소형", "중형", "대형"],
        "indoor": "야외 좌석 및 동반 규정 확인 필요",
        "price": "메뉴별 상이",
        "description": "반려견 동반 식사를 알아볼 때 참고할 유형",
        "tags": ["식사", "테라스", "야외"],
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=900",
        "type": "장소",
    },
    {
        "id": "place_03",
        "name": "반려견 동반 숙소",
        "kind": "숙소",
        "region": "강원",
        "address": "강원 지역 예시 주소",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형", "중형", "대형"],
        "indoor": "객실별 동반 가능 여부 확인 필요",
        "price": "날짜 및 객실별 상이",
        "description": "여행 전 반려동물 동반 숙소를 찾을 때 참고할 유형",
        "tags": ["여행", "숙박", "예약"],
        "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=900",
        "type": "장소",
    },
    {
        "id": "place_04",
        "name": "반려견 산책 공원",
        "kind": "공원",
        "region": "서울",
        "address": "서울 지역 예시 주소",
        "pets": ["강아지"],
        "sizes": ["소형", "중형", "대형"],
        "indoor": "야외 공간 · 목줄 등 현장 규정 확인",
        "price": "무료 또는 시설별 상이",
        "description": "산책과 야외 활동 장소를 찾을 때 참고할 유형",
        "tags": ["산책", "야외", "공원"],
        "image": "https://images.unsplash.com/photo-1511497584788-876760111969?w=900",
        "type": "장소",
    },
    {
        "id": "place_05",
        "name": "반려동물 동반 캠핑장",
        "kind": "캠핑",
        "region": "충청",
        "address": "충청 지역 예시 주소",
        "pets": ["강아지"],
        "sizes": ["소형", "중형", "대형"],
        "indoor": "사이트별 규정 및 안전 수칙 확인 필요",
        "price": "예약 날짜별 상이",
        "description": "반려견과 야외에서 시간을 보내기 위한 캠핑 유형",
        "tags": ["캠핑", "여행", "야외"],
        "image": "https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=900",
        "type": "장소",
    },
    {
        "id": "move_01",
        "name": "반려동물 동반 택시",
        "kind": "택시",
        "region": "전국",
        "address": "서비스 지역은 업체별 확인",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형", "중형", "대형"],
        "indoor": "예약 전 이동장 및 동반 조건 확인",
        "price": "거리 및 업체별 상이",
        "description": "반려동물과 목적지까지 이동하는 서비스 유형",
        "tags": ["택시", "예약", "이동"],
        "image": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=900",
        "type": "이동수단",
    },
    {
        "id": "move_02",
        "name": "반려동물 동반 렌터카",
        "kind": "렌터카",
        "region": "전국",
        "address": "대여 지점 및 이용 지역 확인",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형", "중형", "대형"],
        "indoor": "차량별 동반 정책 및 청소 비용 확인",
        "price": "차량 및 날짜별 상이",
        "description": "일정에 맞춰 이동할 수 있는 차량 대여 유형",
        "tags": ["렌터카", "여행", "자유 이동"],
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=900",
        "type": "이동수단",
    },
    {
        "id": "move_03",
        "name": "반려동물 대중교통 이용 안내",
        "kind": "대중교통",
        "region": "전국",
        "address": "노선 및 운영기관별 확인",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형"],
        "indoor": "운영기관별 이동장 및 운송 규정 확인",
        "price": "노선 및 운임별 상이",
        "description": "버스·철도 이용 전 반려동물 운송 규정을 확인하는 유형",
        "tags": ["대중교통", "규정 확인", "이동"],
        "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=900",
        "type": "이동수단",
    },
]

REGIONS = ["전체", "서울", "경기", "인천", "강원", "충청", "전라", "경상", "제주", "전국"]
KINDS = ["전체", "카페", "식당", "숙소", "공원", "캠핑", "택시", "렌터카", "대중교통"]
PET_TYPES = ["전체", "강아지", "고양이"]
PET_SIZES = ["전체", "소형", "중형", "대형"]

# -----------------------------------------------
# 2. 화면 디자인
# -----------------------------------------------
st.markdown("""
<style>
.stApp {
    background: #F7F8F5;
    color: #26352A;
}
.block-container {
    max-width: 1120px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}
.brand {
    font-size: 26px;
    font-weight: 850;
    letter-spacing: -1px;
    color: #26352A;
}
.brand span {
    color: #4C8058;
}
.hero {
    background: #EAF1E7;
    border: 1px solid #DDE8D9;
    border-radius: 22px;
    padding: 28px;
    margin: 18px 0 25px;
}
.eyebrow {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #52775A;
}
.hero h1 {
    font-size: clamp(28px, 4vw, 42px);
    line-height: 1.25;
    letter-spacing: -1.4px;
    margin: 10px 0;
    color: #26352A;
}
.hero p {
    color: #647267;
    line-height: 1.8;
    margin-bottom: 0;
}
.section-title {
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 22px 0 5px;
}
.muted {
    color: #7A857B;
    font-size: 13px;
    line-height: 1.7;
}
.result-name {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 4px;
    color: #29392D;
}
.result-meta {
    font-size: 12px;
    color: #798479;
}
.tag {
    display: inline-block;
    background: #EDF3E9;
    color: #4A6E4E;
    padding: 5px 8px;
    margin: 3px 4px 3px 0;
    border-radius: 6px;
    font-size: 11px;
}
.info-label {
    color: #7B857C;
    font-size: 12px;
}
.info-value {
    color: #344C38;
    font-size: 13px;
    font-weight: 650;
    line-height: 1.7;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-color: #E4E9E1;
    border-radius: 15px;
}
div.stButton > button {
    border-radius: 9px;
    min-height: 40px;
    font-weight: 650;
}
div[data-testid="stImage"] img {
    border-radius: 10px;
}
.footer {
    border-top: 1px solid #E2E7DF;
    margin-top: 30px;
    padding-top: 18px;
    color: #7C867D;
    font-size: 12px;
    line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# 3. 상태 초기화
# -----------------------------------------------
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "favorites_only" not in st.session_state:
    st.session_state["favorites_only"] = False

# -----------------------------------------------
# 4. 상단 브랜드 및 즐겨찾기
# -----------------------------------------------
head_left, head_right = st.columns([3, 1])

with head_left:
    st.markdown(
        '<div class="brand">🐾 함께<span>가개</span></div>',
        unsafe_allow_html=True,
    )

with head_right:
    label = "전체 검색" if st.session_state["favorites_only"] else "♡ 저장 목록"
    if st.button(label, use_container_width=True):
        st.session_state["favorites_only"] = not st.session_state["favorites_only"]
        st.rerun()

st.markdown("""
<div class="hero">
    <div class="eyebrow">PET-FRIENDLY PLACE & MOBILITY</div>
    <h1>우리 함께,<br>어디든 가개.</h1>
    <p>반려동물과 갈 장소부터 이동수단까지.<br>
    필요한 조건을 선택하고 한눈에 비교해 보세요.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------
# 5. 검색 및 필터
# -----------------------------------------------
st.markdown('<div class="section-title">어디로 떠나볼까요?</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="muted">장소명, 지역, 종류 또는 특징을 검색할 수 있어요.</div>',
    unsafe_allow_html=True,
)

keyword = st.text_input(
    "검색어",
    placeholder="예: 서울 카페, 택시, 캠핑",
    label_visibility="collapsed",
    key="search_keyword",
)

f1, f2, f3, f4 = st.columns(4)

with f1:
    selected_region = st.selectbox("지역", REGIONS, key="filter_region")
with f2:
    selected_kind = st.selectbox("종류", KINDS, key="filter_kind")
with f3:
    selected_pet = st.selectbox("반려동물", PET_TYPES, key="filter_pet")
with f4:
    selected_size = st.selectbox("크기", PET_SIZES, key="filter_size")

type_filter = st.radio(
    "검색 범위",
    ["전체", "장소", "이동수단"],
    horizontal=True,
    key="filter_type",
)

# -----------------------------------------------
# 6. 검색 결과 계산
# -----------------------------------------------
results = []

for item in ITEMS:
    searchable = " ".join([
        item["name"],
        item["kind"],
        item["region"],
        item["address"],
        item["description"],
        item["indoor"],
        item["price"],
        *item["tags"],
        *item["pets"],
        *item["sizes"],
    ]).casefold()

    if keyword.strip() and keyword.strip().casefold() not in searchable:
        continue

    if selected_region != "전체":
        if item["region"] not in (selected_region, "전국"):
            continue

    if selected_kind != "전체" and item["kind"] != selected_kind:
        continue

    if selected_pet != "전체" and selected_pet not in item["pets"]:
        continue

    if selected_size != "전체" and selected_size not in item["sizes"]:
        continue

    if type_filter != "전체" and item["type"] != type_filter:
        continue

    if (
        st.session_state["favorites_only"]
        and item["id"] not in st.session_state["favorites"]
    ):
        continue

    results.append(item)

# -----------------------------------------------
# 7. 결과 카드
# -----------------------------------------------
if st.session_state["favorites_only"]:
    st.markdown('<div class="section-title">저장한 목록</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="section-title">검색 결과</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="muted">{len(results)}개의 결과 · '
    '카드를 눌러 이용 조건을 확인하세요.</div>',
    unsafe_allow_html=True,
)

if not results:
    st.info("검색 결과가 없어요. 검색어 또는 필터를 바꿔 보세요.")
else:
    for start in range(0, len(results), 2):
        pair = results[start:start + 2]
        cols = st.columns(2, gap="medium")

        for col, item in zip(cols, pair):
            with col:
                with st.container(border=True):
                    try:
                        st.image(item["image"], use_container_width=True)
                    except Exception:
                        st.markdown(
                            f'<div style="background:#EDF3E9;padding:38px;'
                            f'text-align:center;border-radius:10px;font-size:30px">'
                            f'🐾</div>',
                            unsafe_allow_html=True,
                        )

                    st.markdown(
                        f'<div class="result-name">{item["name"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="result-meta">'
                        f'{item["region"]} · {item["kind"]} · {item["type"]}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    st.write(item["description"])

                    tags = "".join(
                        f'<span class="tag">{tag}</span>'
                        for tag in item["tags"]
                    )
                    st.markdown(tags, unsafe_allow_html=True)

                    st.markdown(
                        f'<div style="margin-top:12px">'
                        f'<div class="info-label">위치</div>'
                        f'<div class="info-value">{item["address"]}</div>'
                        f'<div class="info-label" style="margin-top:8px">'
                        f'동반 가능 동물</div>'
                        f'<div class="info-value">'
                        f'{", ".join(item["pets"])} · '
                        f'{", ".join(item["sizes"])}견</div>'
                        f'<div class="info-label" style="margin-top:8px">'
                        f'이용 조건</div>'
                        f'<div class="info-value">{item["indoor"]}</div>'
                        f'<div class="info-label" style="margin-top:8px">'
                        f'비용 안내</div>'
                        f'<div class="info-value">{item["price"]}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

                    with st.expander("상세 정보 및 확인 사항"):
                        st.write(item["description"])
                        st.write("**이용 전 확인:** 반려동물 동반 가능 여부, 크기 제한, 이동장·목줄 규정, 추가 비용을 운영자에게 확인하세요.")

                    map_url = (
                        "https://map.naver.com/p/search/"
                        + quote(item["address"] + " " + item["name"])
                    )
                    st.link_button("네이버 지도에서 검색 ↗", map_url, use_container_width=True)

                    is_saved = item["id"] in st.session_state["favorites"]
                    save_text = "♥ 저장 취소" if is_saved else "♡ 즐겨찾기 저장"

                    if st.button(save_text, key=f"save_{item['id']}", use_container_width=True):
                        if is_saved:
                            st.session_state["favorites"].remove(item["id"])
                        else:
                            st.session_state["favorites"].append(item["id"])
                        st.rerun()

# -----------------------------------------------
# 8. 안내
# -----------------------------------------------
st.markdown("""
<div class="footer">
    <b>함께가개 · 반려동물 동반 검색</b><br>
    현재 버전은 배포 및 화면 확인용 예시 데이터로 구성되어 있습니다.
    표시된 장소명과 위치는 실제 업체 정보가 아닐 수 있으며,
    사진은 디자인 미리보기용 이미지입니다.<br>
    실제 방문 전에는 업체의 최신 동반 규정, 운영 시간, 요금 및 위치를 직접 확인하세요.
    즐겨찾기는 로그인 없는 현재 세션에서만 유지됩니다.
</div>
""", unsafe_allow_html=True)
