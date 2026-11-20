import streamlit as st


@st.cache_resource
def load_ai_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )


def _get_place_description(place):
    name = place["area_name"]
    kind = (
        "강변 산책 휴식"
        if "한강" in name
        else "야외 자연 산책"
        if "공원" in name
        else "카페 휴식 대화"
        if "카페" in name
        else "쇼핑 관광"
        if "관광" in name
        else "도심 외출"
    )
    return f"{name}: {kind}. 현재 혼잡도는 {place['congestion_level']}입니다."


def recommend_place(request, places):
    model = load_ai_model()
    descriptions = [_get_place_description(place) for place in places]
    vectors = model.encode(
        [request] + descriptions,
        normalize_embeddings=True,
    )
    scores = vectors[1:] @ vectors[0]
    return places[int(scores.argmax())]
