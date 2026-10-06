# 1. 모듈
import math as m

print(m.factorial(5))

# 자주 사용하는 기능을 모아놓은 파이썬 파일 한 개
# 모듈에는 함수, 클래스, 변수를 정의할 수 있다.

from math import sqrt

print(sqrt(25))
# 모듈(패키지)의 종류
# 1. 표준 라이브러리 모듈(패키지): 파이썬 제공
# 2. 써드 파티 모듈(패키지): 외부에서 만들어서 배포
# 3. 사용자 정의 모듈(패키지)
from math import ceil, floor

print(ceil(3.2))
print(floor(3.8))

# =====================================================================
# 1. 파이썬 표준 라이브러리 불러오기 (https://docs.python.org/3/library)
import sys
#  - import 모듈명
#  - from 모듈명 import 함수명
print(sys.version)       # 현재 실행 중인 파이썬 인터프리터의 버전
print(sys.platform)      # 현재 실행 중인 운영체제 플랫폼 식별자
print(sys.path)          # 파이썬 라이브러리 검색 디렉토리 목록
# math 모듈: 수학 계산에 필요한 함수와 상수를 제공하는 표준 라이브러리
import math

print(dir(math))
print(math.sqrt(16))
print(math.pi)



# 별칭 만들기



# 모듈명 없이 바로 함수명으로 불러오기



# 여러 함수 불러오기



# sys 모듈: 파이썬 인터프리터의 실행 환경과 관련된 정보를 제공하는 표준 라이브러리


                  # 현재 실행 중인 파이썬 인터프리터의 버전
                 # 현재 실행 중인 운영체제 플랫폼 식별자
                     # 파이썬 라이브러리 검색 디렉토리 목록

# 표준 라이브러리 설치 경로: C:\Users\<user_name>\AppData\Local\Programs\Python\Python314\Lib
# 써드 파티 설치 경로: C:\Users\<user_name>\AppData\Local\Programs\Python\Python314\Lib\site-packages


# ===========================================================
# 2. 써드 파티 모듈 불러오기 (https://pypi.org/)
#  - 패키지 목록 보기: pip list
#  - 패키지 설치 하기: pip install 패키지명
# ===========================================================

# requests 모듈: HTTP 요청과 응답을 처리하기 위한 써드 파티 모듈


url = "https://httpbin.org/get?user_id=crong"

try:
    import requests
except ImportError:
    print("requests가 설치되어 있지 않습니다. pip install requests로 설치하세요.")
else:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(response.status_code)
        print(response.json())
    except requests.RequestException as error:
        print("HTTP 요청에 실패했습니다:", error)



# ===========================================================
# 3. 사용자 정의 모듈 만들기
# ===========================================================

from my_module import add, introduce
import mymath

print(add(10, 20))
print(introduce("파이썬"))


# __pycache__ 디렉토리란?
# Python이 실행 속도를 높이기 위해 컴파일된 바이트코드(.pyc)를 캐시로 저장하는 디렉터리
# 모듈을 import할 때만 생성되고, 직접 실행할 때에는 바이트코드까지만 생성하고 저장하지는 않음


# Python 모듈 실행 방식
# 1. CPython에 있는 컴파일러가 Python 소스 코드를 바이트코드(.pyc)로 컴파일
# 2. Python 가상 머신(PVM)이 바이트코드를 실행
# 3. 다음 실행 시에는 .pyc를 바로 읽어 실행
# 4. 모듈이 변경된 경우 .pyc 파일을 재생성하여 실행