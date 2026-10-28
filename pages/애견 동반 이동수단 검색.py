
import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="함께가개 | 반려동물 이동수단 검색",
    page_icon="🐾",
    layout="wide",
)

# 실제 업체 정보가 아닌 화면 확인용 예시 데이터
TRANSPORTS = [
    {
        "id": "taxi",
        "name": "반려동물 동반 택시",
        "category": "택시",
        "region": "전국",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형", "중형", "대형"],
        "condition": "예약 전 동반 가능 여부와 이동장 규정 확인",
        "price": "거리 및 업체별 상이",
        "description": "반려동물과 목적지까지 이동할 때 알아볼 수 있는 서비스",
        "image": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=900",
        "tags": ["예약", "목적지 이동"],
    },
    {
        "id": "rental",
        "name": "반려동물 동반 렌터카",
        "category": "렌터카",
        "region": "전국",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형", "중형", "대형"],
        "condition": "차량별 동반 정책, 이동 안전 장비 및 청소 비용 확인",
        "price": "차량 및 날짜별 상이",
        "description": "여행 일정에 맞춰 자유롭게 이동하고 싶을 때",
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=900",
        "tags": ["여행", "자유 이동"],
    },
    {
        "id": "city_bus",
        "name": "시내버스",
        "category": "버스",
        "region": "지역별 확인",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형"],
        "condition": "운송사별 이동장 및 동반 규정 확인",
        "price": "노선 및 운임별 상이",
        "description": "일상적인 이동을 위한 대중교통",
        "image": "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=900",
        "tags": ["대중교통", "일상 이동"],
    },
    {
        "id": "intercity_bus",
        "name": "고속·시외버스",
        "category": "고속·시외버스",
        "region": "전국",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형"],
        "condition": "운송사 및 노선별 동반 조건을 예매 전에 확인",
        "price": "운송사 및 구간별 상이",
        "description": "다른 도시로 이동하기 전 확인할 장거리 교통수단",
        "image": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=900",
        "tags": ["장거리", "대중교통"],
    },
    {
        "id": "train",
        "name": "기차",
        "category": "기차",
        "region": "전국",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형"],
        "condition": "열차 종류와 운영기관의 최신 운송 규정 확인",
        "price": "노선 및 좌석별 상이",
        "description": "장거리 이동을 위한 철도 교통수단",
        "image": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=900",
        "tags": ["철도", "장거리"],
    },
    {
        "id": "pet_shuttle",
        "name": "반려동물 전용 이동 서비스",
        "category": "전용 이동 서비스",
        "region": "업체별 확인",
        "pets": ["강아지", "고양이"],
        "sizes": ["소형", "중형", "대형"],
        "condition": "서비스 지역, 예약 가능 시간 및 동반 조건 확인",
        "price": "업체별 상이",
        "description": "반려동물 이동을 위해 제공되는 전용 서비스 유형",
        "image": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=900",
        "tags": ["전용 서비스", "예약"],
    },
]

REGIONS = ["전체", "서울", "경기", "인천", "강원", "충청", "전라", "경상", "제주", "전국"]
CATEGORIES = [
    "전체",
    "택시",
    "렌터카",
    "버스",
    "고속·시외버스",
    "기차",
    "전용 이동 서비스",
]
PETS = ["전체", "강아지", "고양이"]
SIZES = ["전체", "소형", "중형", "대형"]

# -------------------------------
# 스타일
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: #F7F8F5;
    color: #26352A;
}
.block-container {
    max-width: 1100px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}
.brand {
    font-size: 27px;
    font-weight: 850;
    letter-spacing: -1px;
}
.brand span {
    color: #4C8058;
}
.hero {
    background: #EAF1E7;
    border: 1px solid #DDE8D9;
    border-radius: 20px;
    padding: 28px;
    margin: 18px 0 25px;
}
.eyebrow {
    color: #52775A;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
}
.hero h1 {
    color: #26352A;
    font-size: clamp(28px, 4vw, 42px);
    line-height: 1.3;
    letter-spacing: -1px;
    margin: 10px 0;
}
.hero p {
    color: #647267;
    line-height: 1.8;
    margin-bottom: 0;
}
.section-title {
    font-size: 21px;
    font-weight: 800;
    margin: 22px 0 5px;
}
.muted {
    color: #7A857B;
    font-size: 13px;
    line-height: 1.7;
}
.card-name {
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 4px;
}
.card-meta {
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
    margin-top: 10px;
}
.info-value {
    color: #344C38;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.7;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: white;
    border-color: #E4E9E1;
    border-radius: 15px;
}
div.stButton > button {
    border-radius: 9px;
    min-height: 40px;
    font-weight: 650;
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

# -------------------------------
# 상태 초기화
# -------------------------------
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

if "favorites_only" not in st.session_state:
    st.session_state["favorites_only"] = False

# -------------------------------
# 상단 메뉴
# -------------------------------
left, right = st.columns([3, 1])

with left:
    st.markdown(
        '<div class="brand">🐾 함께<span>가개</span></div>',
        unsafe_allow_html=True,
    )

with right:
    label = "전체 검색" if st.session_state["favorites_only"] else "♡ 저장 목록"
    if st.button(label, use_container_width=True):
        st.session_state["favorites_only"] = not st.session_state["favorites_only"]
        st.rerun()

st.markdown("""
<div class="hero">
    <div class="eyebrow">PET-FRIENDLY MOBILITY</div>
    <h1>반려동물과 함께,<br>어떤 방법으로 이동할까요?</h1>
    <p>
        택시부터 대중교통까지.<br>
        반려동물과 함께 이용할 이동수단을 검색해 보세요.
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# 검색창
# -------------------------------
st.markdown('<div class="section-title">이동수단 검색</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="muted">이동수단 이름이나 특징을 검색하고 조건을 선택하세요.</div>',
    unsafe_allow_html=True,
)

keyword = st.text_input(
    "검색어",
    placeholder="예: 택시, 기차, 장거리 이동",
    label_visibility="collapsed",
    key="mobility_search",
)

c1, c2, c3 = st.columns(3)

with c1:
    region = st.selectbox("지역", REGIONS, key="mobility_region")

with c2:
    category = st.selectbox("이동수단 종류", CATEGORIES, key="mobility_category")

with c3:
    pet = st.selectbox("반려동물 종류", PETS, key="mobility_pet")

size = st.selectbox("반려동물 크기", SIZES, key="mobility_size")

st.caption(
    "아래 정보는 화면 확인용 예시입니다. 실제 운행 업체나 이용 가능 여부를 보장하지 않습니다."
)

# -------------------------------
# 필터링
# -------------------------------
results = []

for item in TRANSPORTS:
    searchable = " ".join([
        item["name"],
        item["category"],
        item["region"],
        item["description"],
        item["condition"],
        item["price"],
        *item["tags"],
        *item["pets"],
        *item["sizes"],
    ]).casefold()

    if keyword.strip() and keyword.strip().casefold() not in searchable:
        continue

    if category != "전체" and item["category"] != category:
        continue

    if region != "전체":
        if item["region"] not in (region, "전국", "지역별 확인", "업체별 확인"):
            continue

    if pet != "전체" and pet not in item["pets"]:
        continue

    if size != "전체" and size not in item["sizes"]:
        continue

    if (
        st.session_state["favorites_only"]
        and item["id"] not in st.session_state["favorites"]
    ):
        continue

    results.append(item)

# -------------------------------
# 결과 카드
# -------------------------------
heading = "저장한 이동수단" if st.session_state["favorites_only"] else "검색 결과"

st.markdown(
    f'<div class="section-title">{heading} · {len(results)}개</div>',
    unsafe_allow_html=True,
)

if not results:
    st.info("검색 결과가 없습니다. 검색어 또는 필터를 바꿔 보세요.")

else:
    for start in range(0, len(results), 2):
        batch = results[start:start + 2]
        cols = st.columns(2, gap="medium")

        for col, item in zip(cols, batch):
            with col:
                with st.container(border=True):
                    try:
                        st.image(item["image"], use_container_width=True)
                    except Exception:
                        st.write("🐾 이미지가 표시되지 않습니다.")

                    st.markdown(
                        f'<div class="card-name">{item["name"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="card-meta">{item["category"]} · {item["region"]}</div>',
                        unsafe_allow_html=True,
                    )

                    st.write(item["description"])

                    tags = "".join(
                        f'<span class="tag">{tag}</span>'
                        for tag in item["tags"]
                    )
                    st.markdown(tags, unsafe_allow_html=True)

                    st.markdown(
                        f'<div class="info-label">동반 가능 동물</div>'
                        f'<div class="info-value">{", ".join(item["pets"])}</div>'
                        f'<div class="info-label">동반 크기</div>'
                        f'<div class="info-value">{", ".join(item["sizes"])}</div>'
                        f'<div class="info-label">이용 조건</div>'
                        f'<div class="info-value">{item["condition"]}</div>'
                        f'<div class="info-label">비용 안내</div>'
                        f'<div class="info-value">{item["price"]}</div>',
                        unsafe_allow_html=True,
                    )

                    with st.expander("이용 전 확인 사항"):
                        st.write(
                            "운영기관이나 업체의 최신 규정을 확인하세요. "
                            "반려동물 크기 제한, 이동장 사용, 추가 비용, 예약 필요 여부를 "
                            "이용 전에 직접 확인하는 것이 좋습니다."
                        )

                    map_url = (
                        "https://map.naver.com/p/search/"
                        + quote(item["name"] + " " + item["region"])
                    )
                    st.link_button(
                        "네이버 지도에서 검색 ↗",
                        map_url,
                        use_container_width=True,
                    )

                    saved = item["id"] in st.session_state["favorites"]
                    save_label = "♥ 저장 취소" if saved else "♡ 즐겨찾기 저장"

                    if st.button(
                        save_label,
                        key=f"favorite_{item['id']}",
                        use_container_width=True,
                    ):
                        if saved:
                            st.session_state["favorites"].remove(item["id"])
                        else:
                            st.session_state["favorites"].append(item["id"])
                        st.rerun()

# -------------------------------
# 하단 안내
# -------------------------------
st.markdown("""
<div class="footer">
    <b>함께가개 · 반려동물 이동수단 검색</b><br>
    이 앱은 이동수단 검색 화면을 확인하기 위한 예시 버전입니다.
    업체명과 정보는 실제 서비스 제공 업체를 의미하지 않습니다.
    사진은 미리보기용이며 실제 차량이나 서비스 사진이 아닐 수 있습니다.<br>
    즐겨찾기는 현재 세션에서만 유지됩니다.
</div>
""", unsafe_allow_html=True)
