NOWHERE AI 간단 추천 기능

1. pip install -r requirements.txt
2. .env.example을 .env로 복사하고 서울시 OpenAPI 인증키 입력
3. streamlit run app.py
4. 장소를 1~3개 선택해 실시간 정보 조회 후, AI 맞춤 장소 추천 사용

최초 AI 실행 시 허깅페이스에서 모델을 자동으로 다운로드합니다.
AI 추천은 조회한 장소의 의미 유사도를 기반으로 합니다. 실제 혼잡도는 서울시 API 데이터를 사용합니다.
