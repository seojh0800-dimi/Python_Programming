# Open API 심화

import os
import pprint
import requests
import textwrap

from datetime import datetime, timedelta
from dotenv import load_dotenv

# ===========================================================
#  1. 날씨 조회하기
#  - 공공데이터 포털(https://www.data.go.kr/)
#  - 행정안전부에서 운영하는 공공데이터 통합제공 시스템
# ===========================================================

# .env 파일 로드
load_dotenv()

# 공공데이터포털 인증키 가져오기 (env 파일)
SERVICE_KEY = os.getenv("SERVICE_KEY")

# 기준일자, 기준시간 가져오기 ( 가장 최신으로 가져오기(최신 없으면 이전 시간) )
now = datetime.now()
one_hour_age = now - timedelta(hours=1)

base_date = now.strftime("%Y%m%d")
base_time = one_hour_age.strftime("%H00")
# print(f"기준일시: {base_date} {base_time}")


# 날씨 코드
WEATHER_CODE = {
    "T1H": "기온",
    "RN1": "1시간 강수량",
    "UUU": "동서바람성분",
    "VVV": "남북바람성분",
    "REH": "습도",
    "PTY": "강수형태",
    "VEC": "풍향",
    "WSD": "풍속"
}

def get_weather_info(SERVICE_KEY, base_date=base_date, base_time=base_time):
    try:
        # 초단기실황조회 API
        url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        params = {
            "ServiceKey": SERVICE_KEY,
            "pageNo": 1,
            "numOfRows": 100,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": 57,                   # 엑셀파일에서 찾기
            "ny": 122,
        }

        response = requests.get(url, timeout=10, params=params)

        if response.status_code != 200:
            print(f"요청 실패 (상태 코드: {response.status_code})")
            return
        
        data = response.json()
        pprint.pprint(data)

        # 응답코드 조회
        response_body = data.get("response", {})
        header = response_body.get("header", {})
        result_cd = header.get("resultCode")
        result_msg = header.get("resultMsg")

        if result_cd != "00":
            print(f"요청 실패 (Open API 결과 코드: {result_cd}, {result_msg})")
            return

        # 초단기실황조회 결과 출력
        items = response_body.get("body", {}).get("items", {}).get("item", [])
        if not items:
            print("조회된 날씨 정보가 없습니다.")
            return

        for item in items:
            category = item.get("category")
            if category in WEATHER_CODE:
                print(f"{WEATHER_CODE[category]}: {item.get('obsrValue')}")

    except requests.exceptions.Timeout as e:
        print(f"서버 응답시간 초과: {e}")
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")

# get_weather_info(SERVICE_KEY)


# ===========================================================
#  2. 급식 조회하기
#  - 나이스 교육정보 개방 포털(https://open.neis.go.kr/)
#  - 교육부에서 제공하는 나이스 교육정보 제공 서비스
# ===========================================================

def get_food_info(KEY, sc_code, schul_code, mlsv_ymd=base_date):
    try:
        url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
        params = {
            "KEY": KEY,
            "Type": "json",
            "pIndex": "1",
            "pSize": "100",
            "ATPT_OFCDC_SC_CODE": sc_code,      # 시도교육청구분코드
            "SD_SCHUL_CODE": schul_code,        # 행정표준코드
            "MLSV_YMD": mlsv_ymd,               # 급식일자
        }

        response = requests.get(url, timeout=10, params=params)

        if response.status_code != 200:
            print(f"요청 실패 (상태 코드: {response.status_code})")
            return
        
        data = response.json()
        # pprint.pprint(data)

        # 응답코드 조회
        if "RESULT" in data:
            result_cd = data["RESULT"]["CODE"]
            result_msg = data["RESULT"]["MESSAGE"]
            print(f"요청 실패 (Open API 결과 코드: {result_cd}, {result_msg})")
            return

        # 급식정보 출력
        meal_info = data.get("mealServiceDietInfo", [])
        rows = next(
            (section.get("row", []) for section in meal_info if "row" in section),
            [],
        )
        if not rows:
            print("조회된 급식 정보가 없습니다.")
            return

        # 급식 정보 출력
        # 기준일자: 
        # 메뉴: 
        # 열량:
        for meal in rows:
            meal_date = datetime.strptime(meal.get("MLSV_YMD", ""), "%Y%m%d")셔ㅛ
            print(f"날짜: {meal_date:%Y년%m월%d일}")

            if meal.get("CAL_INFO"):
                print(f"열량: {meal['CAL_INFO']}")

            print(f"급식: {meal.get('MMEAL_SC_NM', '정보 없음')}")

            menu = meal.get("DDISH_NM", "").replace("<br/>", "\n")

            print(f"메뉴\n{textwrap.indent(menu, ' | ')}")
            
            print()

    
    except requests.exceptions.Timeout as e:
        print(f"서버 응답시간 초과: {e}")
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"오류 발생: {e}")


# 나이스 인증키 가져오기
NEIS_API_KEY = os.getenv("NEIS_API_KEY")

get_food_info(NEIS_API_KEY, sc_code="J10", schul_code="7530560")
