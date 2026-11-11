import streamlit as st

from api import get_rest_api_data
import city_db
from city_api import API_KEY, AREAS, get_city_info

st.title("NOWHERE.")

st.subheader("장소 비교")
selected = st.multiselect(
    "비교할 장소를 선택하세요",
    AREAS,
    max_selections=3,
)

if st.button("실시간 정보 조회", type="primary", use_container_width=True):
    if len(selected) == 0:
        st.warning("장소를 하나 이상 선택해 주세요.")
    else:
        results = []
        errors = []

        with st.spinner("로딩중..."):
            for area_name in selected:
                try:
                    result = get_city_info(area_name)
                    results.append(result)
                except RuntimeError as error:
                    errors.append(f"{area_name}: {error}")

        st.session_state["results"] = results

        if len(results) > 0:
            city_db.save_history(results)

        for error in errors:
            st.error(error)

results = st.session_state.get("results", [])

if len(results) > 0:
    st.subheader("실시간 혼잡도")

    rows = []
    for item in results:
        people = "정보 없음"
        if item["min_people"] is not None and item["max_people"] is not None:
            people = f"{item['min_people']:,}~{item['max_people']:,}명"

        temperature = "정보 없음"
        if item["temperature"] is not None:
            temperature = f"{item['temperature']}°C"

        pm10 = "정보 없음"
        if item["pm10"] is not None:
            pm10 = f"{item['pm10']} ㎍/㎥"

        rows.append({
            "장소": item["area_name"],
            "혼잡도": item["congestion_level"],
            "추정 인구": people,
            "기온": temperature,
            "미세먼지": pm10,
            "데이터 기준시각": item["updated_at"],
        })

    st.dataframe(rows, hide_index=True, use_container_width=True)

    order = {
        "여유": 1,
        "보통": 2,
        "약간 붐빔": 3,
        "붐빔": 4,
    }

    best = None
    for item in results:
        level = item["congestion_level"]

        if level in order:
            if best is None:
                best = item
            elif order[level] < order[best["congestion_level"]]:
                best = item

    st.subheader("방문 장소 추천")
    if best is None:
        st.info("조회된 혼잡도 정보가 없어 추천할 수 없습니다.")
    else:
        st.success(f"{best['area_name']}가 비교한 장소 중 가장 여유롭습니다. (혼잡도: {best['congestion_level']})")

st.divider()
favorite_tab, history_tab = st.tabs(["즐겨찾기", "조회 기록"])

with favorite_tab:
    area_to_save = st.selectbox("즐겨찾기에 추가할 장소", AREAS)

    if st.button("즐겨찾기 추가"):
        city_db.add_favorite(area_to_save)
        st.rerun()

    favorites = city_db.load_favorites()
    if len(favorites) == 0:
        st.info("저장된 장소가 없습니다.")
    else:
        st.write("저장된 장소: " + ", ".join(favorites))
        area_to_delete = st.selectbox("삭제할 장소", favorites)

        if st.button("즐겨찾기 삭제"):
            city_db.delete_favorite(area_to_delete)
            st.rerun()

with history_tab:
    history = city_db.load_history()
    if len(history) == 0:
        st.info("조회 기록이 없습니다.")
    else:
        history_rows = []
        for checked_at, area_name, congestion in history:
            history_rows.append({
                "조회 시각": checked_at,
                "장소": area_name,
                "혼잡도": congestion,
            })
        st.dataframe(history_rows, hide_index=True, use_container_width=True)


st.divider()

st.title("수행평가")
st.dataframe(get_rest_api_data(), hide_index=True)