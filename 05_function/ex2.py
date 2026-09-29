# 함수 2

# ===========================================================
# 1. 지역변수와 전역변수
# ===========================================================
# 함수 안에서 만든 변수는 지역변수로, 함수 밖에서는 사용할 수 없다.
# 함수 밖에서 선언된 변수는 전역변수이며, 함수 안에서는 기본적으로
# "읽기"만 가능하고, 값을 바꾸려면 global 키워드가 필요하다.

a = 1

def func():
    a = 10
    print("func 내부 a:", a)


func()
print("전역 a:", a)

# global 키워드 사용 예시
b = 5


def change_global():
    global b
    b = 20
    print("change_global 내부 b:", b)


change_global()
print("전역 b:", b)

# ===========================================================
# 2. 함수 인자 전달 방식
# ===========================================================
# 1) call-by-value: 값 자체가 복사되어 전달, 원본과 별도의 메모리 공간을 할당, 함수 내부에서 수정 시 원본 불변
# 2) call-by-reference: 변수의 주소가 전달, 원본과 같은 메모리 공간을 가리킴, 함수 내부에서 수정 시 원본 변경
# 3) call-by-assignment: 파이썬은 객체를 가리키는 참조 전달, 원본과 같은 객체를 가리킴(재할당 전까지)
#                        immutable 객체인 경우 call-by-value처럼 동작 -> 함수 내부에서 수정 시 원본 불변
#                        mutable 객체인 경우 call-by-reference처럼 동작 -> 함수 내부에서 수정 시 원본 변경
#                        mutable 객체라도 재할당을 하면 원본과 연결이 끊기고 새로운 객체 할당


# immutable 예시: 정수는 값이 바뀌면 새 객체를 생성함

def add_ten(num):
    num += 10
    print("함수 내부 num:", num)


x = 5
add_ten(x)
print("원본 x:", x) 

# mutable 예시: 리스트는 내부 요소를 수정하면 원본도 변경됨

def add_item(lst):
    lst.append(99)
    print("함수 내부 lst:", lst)


y = [1, 2, 3]
add_item(y)
print("원본 y:", y)

# ===========================================================
# 3. 재귀함수
# ===========================================================

# 팩토리얼 계산하기 (1, 1, 2, 6, 24, ..)

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


print("factorial(5):", factorial(5))
print("factorial(7):", factorial(7))

# 피보나치 계산하기 (0, 1, 1, 2, 3, 5, 8, ..)

def fibo(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibo(n - 1) + fibo(n - 2)


for i in range(10):
    print(f"fibo({i}) = {fibo(i)}")

# ===========================================================
# 4. 람다함수
# ===========================================================

# 람다함수 : 이름 없는(익명) 한 줄짜리 함수를 만듦
# lambda a, b, ...: 표현식

# 간단한 람다 함수 예시
add = lambda a, b: a + b
print("add(3, 5):", add(3, 5))

# 학생 목록 정렬 예시
students = [
    {"name": "뽀로로", "score": 85},
    {"name": "크롱", "score": 92},
    {"name": "포비", "score": 78},
]

# 이름 순으로 정렬
print(sorted(students, key=lambda s: s["name"]))

# 점수 기준 오름차순 정렬
sorted_students = sorted(students, key=lambda s: s["score"])
print(sorted_students)

# 점수 기준 내림차순 정렬
sorted_students_desc = sorted(students, key=lambda s: s["score"], reverse=True)
print(sorted_students_desc)

# =========================================================
#  🔥 실습 문제
# =========================================================

# 1️⃣ n이 짝수면 True, 홀수면 False를 반환하는 함수 작성하기

def is_even(n):
    return n % 2 == 0


print(is_even(4))
print(is_even(7))

# 2️⃣ 가변 인자로 여러 숫자를 받아 (최소값, 최대값, 합계, 평균) 튜플 리턴하기

def num_info(*numbers):
    if not numbers:
        return (0, 0, 0, 0.0)
    minimum = min(numbers)
    maximum = max(numbers)
    total = sum(numbers)
    average = total / len(numbers)
    return (minimum, maximum, total, average)

print(num_info(4, 8, 1, 9, 3))

# 3️⃣ 이름과 키워드 가변 인자로 받은 정보로 아래와 같이 문자열을 만들어 리턴하기

def introduce(name, **info):
    result = [name]
    for key, value in info.items():
        result.append(f"{key}: {value}")
    return " / ".join(result)


print(introduce("카리나", age=26, team="에스파", hometown="수원"))
print(introduce("장원영", age=22, team="아이브", bloodtype="O형"))
print(introduce("성현", age=17, team="코르티스"))

# 4️⃣ 5부터 카운트다운하여 로켓 발사시키기 (재귀함수)
# time.sleep(1)                     # 1초 동안 stop

import time


def countdown(n):
    if n == 0:
        print("로켓 발사!")
        return

    print(n)
    time.sleep(1)
    countdown(n - 1)


countdown(5)