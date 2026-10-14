
import streamlit as st

st.set_page_config(
    page_title="함께가개",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 데모용 데이터: 실제 업체 및 실시간 정보가 아닙니다.
TRANSPORTS = [
    {
        "name": "반려동물 동반 택시",
        "category": "택시",
        "area": "전국",
        "icon": "🚕",
        "summary": "반려견과 함께 목적지까지 이동",
        "tags": ["예약형", "승하차 편리"],
        "sizes": ["소형견", "중형견", "대형견"],
        "cost": "업체별 상이",
        "details": "예약 전에 반려견 동반 가능 여부, 이동장 필요 여부, 추가 요금을 확인하세요.",
    },
    {
        "name": "반려동물 동반 렌터카",
        "category": "렌터카",
        "area": "전국",
        "icon": "🚙",
        "summary": "여행 일정에 맞춰 자유롭게 이동",
        "tags": ["자유로운 일정", "차량별 규정"],
        "sizes": ["소형견", "중형견", "대형견"],
        "cost": "차량 및 날짜별 상이",
        "details": "반려동물 동반을 허용하는 차량인지, 안전 장비와 청소 비용 규정은 어떤지 확인하세요.",
    },
    {
        "name": "시내버스",
        "category": "대중교통",
        "area": "지역별 확인",
        "icon": "🚌",
        "summary": "지역별 운송 규정을 확인하고 이용",
        "tags": ["노선 확인", "이동장 준비"],
        "sizes": ["소형견"],
        "cost": "일반 운임 기준",
        "details": "지역과 운송사에 따라 규정이 다를 수 있습니다. 이용 전 해당 운송사의 최신 안내를 확인하세요.",
    },
    {
        "name": "도시철도",
        "category": "대중교통",
        "area": "운영 지역별 확인",
        "icon": "🚇",
        "summary": "운영기관의 반려동물 운송 규정 확인",
        "tags": ["노선 확인", "이동장 준비"],
        "sizes": ["소형견"],
        "cost": "일반 운임 기준",
        "details": "운영기관의 최신 규정과 이동장 관련 조건을 확인한 뒤 이용하세요.",
    },
    {
        "name": "고속·시외버스",
        "category": "시외 이동",
        "area": "전국",
        "icon": "🚍",
        "summary": "장거리 이동 전 운송 조건 확인",
        "tags": ["장거리", "사전 확인"],
        "sizes": ["소형견"],
        "cost": "운송사별 상이",
        "details": "운송사와 노선에 따라 동반 조건이 다를 수 있으므로 예매 전에 약관을 확인하세요.",
    },
    {
        "name": "기차",
        "category": "시외 이동",
        "area": "전국",
        "icon": "🚆",
        "summary": "열차 종류에 따른 동반 조건 확인",
        "tags": ["장거리", "좌석 확인"],
        "sizes": ["소형견"],
        "cost": "열차 및 구간별 상이",
        "details": "열차 종류와 운영 규정에 따라 조건이 다를 수 있습니다. 예약 전 공식 안내를 확인하세요.",
    },
]

# 디자인
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

.stApp {
    background: #fbfcfa;
    color: #26372b;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.brand {
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: #26372b;
}

.brand span {
    color: #426b4f;
}

.hero {
    background: #f0f4ed;
    border: 1px solid #e6ece2;
    border-radius: 22px;
    padding: 32px;
    margin: 18px 0 26px;
}

.hero .eyebrow {
    color: #426b4f;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}

.hero h1 {
    color: #26372b;
    font-size: clamp(2rem, 4vw, 2.8rem);
    line-height: 1.2;
    letter-spacing: -0.05em;
    margin: 12px 0;
}

.hero p {
    color: #657267;
    line-height: 1.7;
    margin-bottom: 0;
}

.section-title {
    color: #29392e;
    font-size: 1.2rem;
    font-weight: 800;
    margin: 1.1rem 0 0.3rem;
}

.section-sub {
    color: #78847a;
    font-size: 0.9rem;
    margin-bottom: 1.1rem;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border-color: #e5eae3;
    border-radius: 16px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #dce4da;
    color: #35543d;
    background: white;
    font-weight: 600;
}

div.stButton > button[kind="primary"] {
    background: #426b4f;
    border-color: #426b4f;
    color: white;
}

.result-name {
    color: #26372b;
    font-size: 1.02rem;
    font-weight: 750;
    margin-bottom: 5px;
}

.result-summary {
    color: #6c786e;
    font-size: 0.88rem;
    line-height: 1.55;
}

.pill {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 7px;
    background: #f1f5ef;
    color: #4e6854;
    font-size: 0.75rem;
    margin: 3px 4px 0 0;
}

.small-label {
    color: #758177;
    font-size: 0.8rem;
}

.cost {
    color: #344e39;
    font-size: 0.92rem;
    font-weight: 700;
}

.footer-note {
    color: #859087;
    font-size: 0.78rem;
    line-height: 1.7;
    border-top: 1px solid #e7ece5;
    padding-top: 16px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# 저장 목록 상태
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "show_favorites" not in st.session_state:
    st.session_state.show_favorites = False

# 상단 메뉴
top_left, top_right = st.columns([3, 1])

with top_left:
    st.markdown(
        '<div class="brand">🐾 함께<span>가개</span></div>',
        unsafe_allow_html=True,
    )

with top_right:
    button_label = (
        "← 전체 목록"
        if st.session_state.show_favorites
        else "♡ 저장 목록"
    )

    if st.button(button_label, use_container_width=True):
        st.session_state.show_favorites = (
            not st.session_state.show_favorites
        )
        st.rerun()

# 메인 소개
st.markdown("""
<div class="hero">
    <div class="eyebrow">PET-FRIENDLY MOBILITY</div>
    <h1>반려견과 함께,<br>어디든 편하게.</h1>
    <p>
        이동수단별 동반 조건을 한곳에서 비교하고<br>
        우리에게 맞는 이동 방법을 찾아보세요.
    </p>
</div>
""", unsafe_allow_html=True)

# 검색 영역
st.markdown(
    '<div class="section-title">어떤 이동 방법을 찾으세요?</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-sub">검색어와 조건을 선택해 결과를 좁혀보세요.</div>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([2, 1.2, 1.2])

with col1:
    keyword = st.text_input(
        "지역 또는 키워드",
        placeholder="예: 택시, 기차, 전국",
        label_visibility="collapsed",
    )

with col2:
    category = st.selectbox(
        "이동수단",
        ["전체", "택시", "렌터카", "대중교통", "시외 이동"],
        label_visibility="collapsed",
    )

with col3:
    dog_size = st.selectbox(
        "반려견 크기",
        ["크기 무관", "소형견", "중형견", "대형견"],
        label_visibility="collapsed",
    )

st.caption(
    "현재 결과는 화면 확인용 예시 데이터이며, "
    "실제 업체의 이용 가능 여부를 보장하지 않습니다."
)

# 검색 및 필터
filtered = []

for item in TRANSPORTS:
    searchable = " ".join([
        item["name"],
        item["category"],
        item["area"],
        item["summary"],
        " ".join(item["tags"]),
    ])

    if keyword.strip():
        if keyword.strip().lower() not in searchable.lower():
            continue

    if category != "전체" and item["category"] != category:
        continue

    if dog_size != "크기 무관" and dog_size not in item["sizes"]:
        continue

    if (
        st.session_state.show_favorites
        and item["name"] not in st.session_state.favorites
    ):
        continue

    filtered.append(item)

title = (
    "저장한 이동수단"
    if st.session_state.show_favorites
    else "이동수단 둘러보기"
)

st.markdown(
    f'<div class="section-title">{title} '
    f'<span style="font-size:.85rem;color:#839087;'
    f'font-weight:500;">{len(filtered)}개</span></div>',
    unsafe_allow_html=True,
)

# 결과 카드
if not filtered:
    st.info("조건에 맞는 결과가 없어요. 검색어나 필터를 바꿔보세요.")

else:
    columns = st.columns(2, gap="large")

    for index, item in enumerate(filtered):
        with columns[index % 2]:
            with st.container(border=True):
                icon_col, info_col = st.columns([0.8, 3.5])

                with icon_col:
                    st.markdown(
                        f"""
                        <div style="
                            width:60px;
                            height:60px;
                            border-radius:15px;
                            background:#f0f4ed;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            font-size:28px;">
                            {item["icon"]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with info_col:
                    st.markdown(
                        f'<div class="result-name">{item["name"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="small-label">'
                        f'{item["area"]} · {item["category"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(
                        f'<div class="result-summary">'
                        f'{item["summary"]}</div>',
                        unsafe_allow_html=True,
                    )

                tags_html = "".join(
                    f'<span class="pill">{tag}</span>'
                    for tag in item["tags"]
                )
                st.markdown(tags_html, unsafe_allow_html=True)

                st.markdown(
                    f'<div style="margin-top:14px">'
                    f'<span class="small-label">이용 비용</span><br>'
                    f'<span class="cost">{item["cost"]}</span></div>',
                    unsafe_allow_html=True,
                )

                with st.expander("동반 조건 확인"):
                    st.write(item["details"])
                    st.caption(
                        "실제 이용 전 해당 운영사의 최신 안내를 확인하세요."
                    )

                save_col, check_col = st.columns(2)

                with save_col:
                    saved = item["name"] in st.session_state.favorites

                    if st.button(
                        "♥ 저장됨" if saved else "♡ 저장하기",
                        key=f"save_{index}_{item['name']}",
                        use_container_width=True,
                    ):
                        if saved:
                            st.session_state.favorites.remove(item["name"])
                        else:
                            st.session_state.favorites.append(item["name"])

                        st.rerun()

                with check_col:
                    if st.button(
                        "이용 전 확인",
                        key=f"check_{index}_{item['name']}",
                        use_container_width=True,
                    ):
                        st.session_state[
                            f"notice_{item['name']}"
                        ] = True

                if st.session_state.get(
                    f"notice_{item['name']}", False
                ):
                    st.info(
                        "현재는 데모 사이트입니다. "
                        "실제 업체의 최신 규정과 이용 가능 여부를 확인하세요."
                    )

# 하단 안내
st.markdown("""
<div class="footer-note">
    <b>서비스 안내</b><br>
    현재 버전은 화면과 검색 기능을 확인하기 위한 데모입니다.
    실제 업체 목록, 실시간 운행 정보, 정확한 비용은 연결되어 있지 않습니다.
    정식 서비스로 사용하려면 업체 데이터와 공식 이용 규정을 연동해야 합니다.
</div>
""", unsafe_allow_html=True)
requirments.txt
streamlit>=1.36,<2.0
README.md

# 함께가개 🐾

반려견과 함께 이용할 수 있는 이동수단을 검색하고 비교하는 웹사이트입니다.

## 주요 기능
- 키워드 검색
- 이동수단별 필터
- 반려견 크기별 필터
- 카드형 검색 결과
- 이동수단별 동반 조건 확인
- 관심 목록 저장

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 안내

현재 버전은 데모입니다.
실제 업체 정보와 실시간 이용 가능 여부는 연동되어 있지 않습니다.
