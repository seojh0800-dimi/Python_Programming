import os
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("SEOUL_API_KEY", "").strip()

AREAS = [
    "강남역",
    "홍대 관광특구",
    "성수카페거리",
    "명동 관광특구",
    "이태원 관광특구",
    "잠실 관광특구",
    "광화문·덕수궁",
    "광화문광장",
    "경복궁",
    "서울숲공원",
    "여의도한강공원",
    "반포한강공원",
    "동대문 관광특구",
    "종로·청계 관광특구",
]


def read_number(value, number_type):
    if value is None or value.strip() == "" or value == "-":
        return None

    try:
        return number_type(value.replace(",", ""))
    except ValueError:
        return None


def parse_city_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        raise RuntimeError("서울시 API 응답을 읽을 수 없습니다.")

    result_code = root.findtext(".//RESULT/CODE")
    if result_code is None:
        result_code = root.findtext("./CODE")

    if result_code is not None and result_code != "INFO-000":
        result_message = root.findtext(".//RESULT/MESSAGE")
        if result_message is None:
            result_message = root.findtext("./MESSAGE")
        raise RuntimeError(f"서울시 API 오류: {result_code} / {result_message}")

    city = root.find(".//CITYDATA")
    if city is None:
        city = root

    area_name = city.findtext(".//AREA_NM")
    congestion = city.findtext(".//LIVE_PPLTN_STTS//AREA_CONGEST_LVL")

    if congestion is None:
        congestion = city.findtext(".//AREA_CONGEST_LVL")

    if area_name is None or area_name.strip() == "":
        raise RuntimeError("응답에서 장소 정보를 찾지 못했습니다.")

    if congestion is None or congestion.strip() == "":
        congestion = "정보 없음"

    return {
        "area_name": area_name,
        "congestion_level": congestion,
        "min_people": read_number(city.findtext(".//LIVE_PPLTN_STTS//AREA_PPLTN_MIN"), int),
        "max_people": read_number(city.findtext(".//LIVE_PPLTN_STTS//AREA_PPLTN_MAX"), int),
        "temperature": read_number(city.findtext(".//WEATHER_STTS//TEMP"), float),
        "pm10": read_number(city.findtext(".//WEATHER_STTS//PM10"), float),
        "updated_at": city.findtext(".//LIVE_PPLTN_STTS//PPLTN_TIME"),
    }


def get_city_info(area_name):
    area = quote(area_name, safe="")
    url = f"http://openapi.seoul.go.kr:8088/{API_KEY}/xml/citydata/1/5/{area}"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("서울시 API 응답 시간이 초과되었습니다.")
    except requests.exceptions.RequestException:
        raise RuntimeError("서울시 API에 연결하지 못했습니다. 인터넷 연결을 확인해 주세요.")

    return parse_city_xml(response.content)