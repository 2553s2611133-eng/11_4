import sqlite3
from pathlib import Path
from typing import Any

import streamlit as st

st.set_page_config(
    page_title="반려동물 동반 장소 관리",
    page_icon="🐾",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "pet_friendly_places.db"

# ----------------------------
# Database
# ----------------------------
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS pet_friendly_places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                business_type TEXT NOT NULL,
                address TEXT NOT NULL,
                contact TEXT NOT NULL,
                pet_size TEXT NOT NULL DEFAULT '제한없음',
                pet_conditions TEXT NOT NULL,
                usage_guide TEXT NOT NULL,
                parking_info TEXT NOT NULL DEFAULT '정보 없음',
                pet_fee TEXT NOT NULL DEFAULT '무료',
                region TEXT NOT NULL DEFAULT '기타',
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_pet_friendly_places_business
            ON pet_friendly_places (business_name)
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_pet_friendly_places_type
            ON pet_friendly_places (business_type)
            """
        )


def save_place(place: dict[str, str]) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO pet_friendly_places (
                business_name,
                business_type,
                address,
                contact,
                pet_size,
                pet_conditions,
                usage_guide,
                parking_info,
                pet_fee,
                region,
                notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                place["업체명"].strip(),
                place["업체 유형"].strip(),
                place["주소"].strip(),
                place["연락처"].strip(),
                place["반려동물 크기"].strip(),
                place["반려동물 동반 조건"].strip(),
                place["이용 안내"].strip(),
                place["주차 정보"].strip(),
                place["반려동물 이용 요금"].strip(),
                place["지역"].strip(),
                place["추가 메모"].strip(),
            ),
        )
        if cursor.lastrowid is None:
            raise sqlite3.DatabaseError("등록 번호를 확인할 수 없습니다.")
        return int(cursor.lastrowid)


def fetch_places(
    search: str = "",
    business_type: str = "전체",
    region: str = "전체",
) -> list[dict[str, Any]]:
    query = """
        SELECT *
        FROM pet_friendly_places
        WHERE 1=1
    """
    params: list[str] = []

    if search.strip():
        query += """
            AND (
                business_name LIKE ? OR
                address LIKE ? OR
                contact LIKE ? OR
                pet_conditions LIKE ? OR
                usage_guide LIKE ?
            )
        """
        keyword = f"%{search.strip()}%"
        params.extend([keyword, keyword, keyword, keyword, keyword])

    if business_type != "전체":
        query += " AND business_type = ?"
        params.append(business_type)

    if region != "전체":
        query += " AND region = ?"
        params.append(region)

    query += " ORDER BY created_at DESC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def get_place_by_id(place_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM pet_friendly_places WHERE id = ?",
            (place_id,),
        ).fetchone()
        return dict(row) if row else None


def update_place(place_id: int, place: dict[str, str]) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE pet_friendly_places
            SET
                business_name = ?,
                business_type = ?,
                address = ?,
                contact = ?,
                pet_size = ?,
                pet_conditions = ?,
                usage_guide = ?,
                parking_info = ?,
                pet_fee = ?,
                region = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                place["업체명"].strip(),
                place["업체 유형"].strip(),
                place["주소"].strip(),
                place["연락처"].strip(),
                place["반려동물 크기"].strip(),
                place["반려동물 동반 조건"].strip(),
                place["이용 안내"].strip(),
                place["주차 정보"].strip(),
                place["반려동물 이용 요금"].strip(),
                place["지역"].strip(),
                place["추가 메모"].strip(),
                place_id,
            ),
        )


def delete_place(place_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM pet_friendly_places WHERE id = ?", (place_id,))


def place_exists(name: str, address: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT 1 FROM pet_friendly_places
            WHERE LOWER(TRIM(business_name)) = LOWER(TRIM(?))
              AND LOWER(TRIM(address)) = LOWER(TRIM(?))
            LIMIT 1
            """,
            (name, address),
        ).fetchone()
        return row is not None


def get_count_stats() -> dict[str, int]:
    with get_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM pet_friendly_places").fetchone()[0]
        restaurants = conn.execute(
            "SELECT COUNT(*) FROM pet_friendly_places WHERE business_type = '식당'"
        ).fetchone()[0]
        cafes = conn.execute(
            "SELECT COUNT(*) FROM pet_friendly_places WHERE business_type = '카페'"
        ).fetchone()[0]
        lodgings = conn.execute(
            "SELECT COUNT(*) FROM pet_friendly_places WHERE business_type = '숙소'"
        ).fetchone()[0]
        return {
            "total": total,
            "restaurants": restaurants,
            "cafes": cafes,
            "lodgings": lodgings,
        }


# ----------------------------
# UI helpers
# ----------------------------
def render_kpi_cards(stats: dict[str, int]) -> None:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 등록 수", stats["total"])
    with col2:
        st.metric("식당", stats["restaurants"])
    with col3:
        st.metric("카페", stats["cafes"])
    with col4:
        st.metric("숙소", stats["lodgings"])


def build_place_form(defaults: dict[str, str] | None = None) -> dict[str, str]:
    defaults = defaults or {}

    col1, col2 = st.columns(2)
    with col1:
        business_name = st.text_input(
            "업체명 *",
            value=defaults.get("업체명", ""),
            placeholder="예: 포근한 멍멍 카페",
        )
    with col2:
        business_type = st.selectbox(
            "업체 유형 *",
            ["식당", "카페", "숙소", "관광지", "교통수단", "기타"],
            index=["식당", "카페", "숙소", "관광지", "교통수단", "기타"].index(
                defaults.get("업체 유형", "식당")
            )
            if defaults.get("업체 유형") in ["식당", "카페", "숙소", "관광지", "교통수단", "기타"]
            else 0,
        )

    col3, col4 = st.columns(2)
    with col3:
        address = st.text_input(
            "주소 *",
            value=defaults.get("주소", ""),
            placeholder="예: 서울시 강남구 테헤란로 123",
        )
    with col4:
        contact = st.text_input(
            "연락처 *",
            value=defaults.get("연락처", ""),
            placeholder="예: 041-123-4567",
        )

    col5, col6 = st.columns(2)
    with col5:
        region = st.selectbox(
            "지역 *",
            ["서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "강원", "충청", "전라", "경상", "제주", "기타"],
            index=["서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "강원", "충청", "전라", "경상", "제주", "기타"].index(
                defaults.get("지역", "서울")
            )
            if defaults.get("지역") in ["서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "강원", "충청", "전라", "경상", "제주", "기타"]
            else 0,
        )
    with col6:
        pet_size = st.selectbox(
            "반려동물 크기 *",
            ["제한없음", "소형견", "중형견", "대형견", "10kg 이하", "15kg 이하", "20kg 이하"],
            index=["제한없음", "소형견", "중형견", "대형견", "10kg 이하", "15kg 이하", "20kg 이하"].index(
                defaults.get("반려동물 크기", "제한없음")
            )
            if defaults.get("반려동물 크기") in ["제한없음", "소형견", "중형견", "대형견", "10kg 이하", "15kg 이하", "20kg 이하"]
            else 0,
        )

    pet_conditions = st.text_area(
        "반려동물 동반 조건 *",
        value=defaults.get("반려동물 동반 조건", ""),
        placeholder="예: 목줄 착용 필수, 10kg 이하 동반 가능, 대형견은 제한",
        height=120,
    )
    usage_guide = st.text_area(
        "이용 안내 *",
        value=defaults.get("이용 안내", ""),
        placeholder="예: 입장 시간, 예약 방법, 주차 정책, 준비물 등",
        height=140,
    )

    col7, col8 = st.columns(2)
    with col7:
        parking_info = st.text_input(
            "주차 정보 *",
            value=defaults.get("주차 정보", ""),
            placeholder="예: 무료 주차 2대 가능",
        )
    with col8:
        pet_fee = st.text_input(
            "반려동물 이용 요금 *",
            value=defaults.get("반려동물 이용 요금", ""),
            placeholder="예: 무료 / 1,000원 / 별도 요금",
        )

    notes = st.text_area(
        "추가 메모",
        value=defaults.get("추가 메모", ""),
        placeholder="예: 실내 밖으로 나가기 금지, 애견 전용 좌석 있음",
        height=100,
    )

    return {
        "업체명": business_name,
        "업체 유형": business_type,
        "주소": address,
        "연락처": contact,
        "지역": region,
        "반려동물 크기": pet_size,
        "반려동물 동반 조건": pet_conditions,
        "이용 안내": usage_guide,
        "주차 정보": parking_info,
        "반려동물 이용 요금": pet_fee,
        "추가 메모": notes,
    }


# ----------------------------
# Main page
# ----------------------------
def main() -> None:
    try:
        initialize_database()
    except sqlite3.Error as error:
        st.error(f"데이터베이스를 준비하지 못했습니다: {error}")
        st.stop()

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

        :root {
            --ink: #243b2f;
            --muted: #6a7e70;
            --green: #4d7d5f;
            --green-deep: #355d45;
            --green-soft: #edf7ee;
            --cream: #fffaf2;
            --peach: #fff1e8;
            --card: rgba(255,255,255,0.9);
            --line: #e3eadf;
            --danger: #d9654d;
            --shadow: 0 10px 28px rgba(34, 51, 40, 0.08);
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 10%, rgba(165,204,170,0.2), transparent 22%),
                radial-gradient(circle at 90% 8%, rgba(255,195,145,0.2), transparent 20%),
                linear-gradient(180deg, #f7f5f1 0%, #f4f8f3 100%);
            color: var(--ink);
            font-family: 'Gowun Dodum', sans-serif;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        div[data-testid="stMetric"] > div {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 18px;
            box-shadow: var(--shadow);
            padding: 0.8rem 1rem;
        }

        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.82);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 1.2rem 1.1rem 0.5rem;
            box-shadow: var(--shadow);
        }

        .hero {
            background: linear-gradient(120deg, #edf7ee 0%, #fffaf2 60%, #fff0e8 100%);
            border: 1px solid var(--line);
            border-radius: 28px;
            padding: 1.7rem 1.8rem;
            box-shadow: var(--shadow);
            margin-bottom: 1.2rem;
        }

        .hero-tag {
            color: var(--green);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }

        .hero h1 {
            margin: 0 0 0.5rem;
            font-size: clamp(2rem, 4vw, 2.9rem);
            color: var(--ink);
        }

        .hero p {
            margin: 0;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.7;
        }

        .info-card {
            padding: 1rem 1.1rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: rgba(255,255,255,0.8);
            box-shadow: var(--shadow);
        }

        .note-box {
            background: var(--cream);
            border-left: 4px solid var(--green);
            padding: 0.9rem 1rem;
            border-radius: 12px;
            color: var(--muted);
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero">
            <div class="hero-tag">🐾 반려동물 동반 장소 관리</div>
            <h1>반려동물 동반 업체 · 숙소 등록/관리</h1>
            <p>반려동물과 함께 갈 수 있는 장소를 등록하고, 등록된 정보를 검색하고 관리할 수 있습니다.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stats = get_count_stats()
    render_kpi_cards(stats)

    tab_register, tab_manage = st.tabs(["등록", "목록/관리"])

    with tab_register:
        st.subheader("📝 장소 등록")
        st.caption("필수 항목을 빠짐없이 입력해 주세요.")

        with st.form("register_form", clear_on_submit=True):
            place = build_place_form()
            submit = st.form_submit_button("🐶 장소 등록하기", use_container_width=True)

        if submit:
            cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in place.items()}
            missing = [label for label, value in cleaned.items() if not value]

            if missing:
                st.error("아직 입력하지 않은 항목이 있어요. 모든 필수 항목을 확인해 주세요.")
                st.write("미입력 항목: " + ", ".join(missing))
            else:
                try:
                    if place_exists(cleaned["업체명"], cleaned["주소"]):
                        st.warning("이미 같은 이름과 주소의 장소가 등록되어 있어요.")
                    else:
                        place_id = save_place(cleaned)
                        st.success(f"장소가 성공적으로 등록되었어요! (등록 번호: {place_id})")
                        st.session_state["last_registered_place_id"] = place_id
                        st.session_state["last_registered_place"] = cleaned
                except sqlite3.Error as error:
                    st.error(f"데이터를 저장하지 못했어요: {error}")

        if st.session_state.get("last_registered_place"):
            place_info = st.session_state["last_registered_place"]
            st.markdown(
                """
                <div class="note-box">
                    최근 등록한 장소 정보를 확인해 보세요.
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.json(place_info)

    with tab_manage:
        st.subheader("📚 등록된 장소 목록")

        search = st.text_input("검색", placeholder="업체명, 주소, 조건, 안내 내용을 입력하세요")
        colA, colB = st.columns(2)
        with colA:
            business_type_filter = st.selectbox(
                "업체 유형",
                ["전체", "식당", "카페", "숙소", "관광지", "교통수단", "기타"],
            )
        with colB:
            region_filter = st.selectbox(
                "지역",
                ["전체", "서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "강원", "충청", "전라", "경상", "제주", "기타"],
            )

        places = fetch_places(search, business_type_filter, region_filter)

        if not places:
            st.info("조건에 맞는 등록된 장소가 없습니다.")
        else:
            st.write(f"총 {len(places)}건 조회됨")

            for place in places:
                with st.container():
                    st.markdown(
                        """
                        <div class="info-card">
                        """,
                        unsafe_allow_html=True,
                    )
                    col_left, col_right = st.columns([3, 1])
                    with col_left:
                        st.markdown(
                            f"""
                            <div style='padding:0.4rem 0;'>
                                <h3 style='margin:0; color:#243b2f;'>{place['business_name']}</h3>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        st.write(
                            f"유형: {place['business_type']} | 지역: {place['region']} | 연락처: {place['contact']}"
                        )
                        st.write(f"주소: {place['address']}")
                        st.write(f"반려동물 크기: {place['pet_size']}")
                        st.write(f"동반 조건: {place['pet_conditions']}")
                        st.write(f"이용 안내: {place['usage_guide']}")
                        st.write(f"주차 정보: {place['parking_info']} | 요금: {place['pet_fee']}")
                        if place["notes"]:
                            st.write(f"추가 메모: {place['notes']}")
                    with col_right:
                        st.button(
                            "수정",
                            key=f"edit_{place['id']}",
                            use_container_width=True,
                            on_click=lambda pid=place["id"]: st.session_state.__setitem__("edit_place_id", pid),
                        )
                        st.button(
                            "삭제",
                            key=f"delete_{place['id']}",
                            type="secondary",
                            use_container_width=True,
                            on_click=lambda pid=place["id"]: st.session_state.__setitem__("delete_place_id", pid),
                        )

                    st.markdown("</div>", unsafe_allow_html=True)
                    st.write("---")

            if "delete_place_id" in st.session_state:
                target_id = st.session_state.pop("delete_place_id")
                if target_id:
                    delete_place(target_id)
                    st.success("장소가 삭제되었습니다.")
                    st.rerun()

            if "edit_place_id" in st.session_state:
                edit_id = st.session_state.pop("edit_place_id")
                edit_row = get_place_by_id(edit_id)
                if edit_row:
                    st.subheader("✏️ 장소 수정")
                    edit_data = {
                        "업체명": edit_row["business_name"],
                        "업체 유형": edit_row["business_type"],
                        "주소": edit_row["address"],
                        "연락처": edit_row["contact"],
                        "지역": edit_row["region"],
                        "반려동물 크기": edit_row["pet_size"],
                        "반려동물 동반 조건": edit_row["pet_conditions"],
                        "이용 안내": edit_row["usage_guide"],
                        "주차 정보": edit_row["parking_info"],
                        "반려동물 이용 요금": edit_row["pet_fee"],
                        "추가 메모": edit_row["notes"],
                    }

                    with st.form(f"edit_form_{edit_id}"):
                        updated = build_place_form(edit_data)
                        save_edit = st.form_submit_button("수정 저장")

                    if save_edit:
                        cleaned = {k: (v.strip() if isinstance(v, str) else v) for k, v in updated.items()}
                        missing = [label for label, value in cleaned.items() if not value]

                        if missing:
                            st.error("필수 항목이 비어 있어 수정할 수 없어요.")
                            st.write("미입력 항목: " + ", ".join(missing))
                        else:
                            try:
                                update_place(edit_id, cleaned)
                                st.success("수정이 완료되었습니다.")
                                st.rerun()
                            except sqlite3.Error as error:
                                st.error(f"수정 중 오류가 발생했어요: {error}")


if __name__ == "__main__":
    main()
