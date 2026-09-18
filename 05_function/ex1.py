# 함수 1

# ===========================================================
# 1. 기본 함수
# ===========================================================
def add(a,b):
    """a+b 결과를 반환한다"""
    return a + b
print(add(3, 4))
print(add("hello", "python"))
print(add([1, 2], [3, 4]))
print(add((1, 2), (3, 4)))
print(add.__doc__)



# ===========================================================
# 2. 튜플을 리턴하는 함수
# ===========================================================
def add_sub(a, b):
    return a + b , a - b

print(add_sub(5,3))
print(*add_sub(5,3))

x,y = add_sub(5,3)
print(x,y)


# ===========================================================
# 3. 디폴트 매개변수 (Default Parameter)
# ===========================================================
# 매개변수에 기본값을 지정하면, 호출 시 해당 인자를 생략할 수 있다.
# 디폴트 매개변수는 항상 일반 매개변수 뒤에 위치해야 한다.

def greet(name, message="안녕하세요!"):
    return f"{name}님, {message}"

print(greet("민수"))
print(greet("민수", "좋은 아침입니다!"))


# ===========================================================
# 4. 키워드 인자 (Keyword Argument)
# ===========================================================
# 인자를 순서가 아니라 "매개변수명=값" 형태로 전달할 수 있다.
# 순서를 바꿔서 호출해도 이름만 맞으면 정확히 전달된다.

def introduce(name, age, city):
    return f"{name}은(는) {city}에 살고 있고, 나이는 {age}세입니다."

print(introduce("민수", 20, "서울"))
print(introduce(age=20, city="서울", name="민수"))


# ===========================================================
# 5. 가변 인자 (Variable-length Argument, *args)
# ===========================================================
# 몇 개의 인자가 들어올지 모를 때 *args를 사용한다. (관례적으로 사용)
# args라는 이름으로 입력값들을 모아 튜플로 만든다.

def total(*numbers):
    result = 0
    for n in numbers:
        result += n
    return result

print(total(1, 2, 3, 4))
print(total(10, 20, 30))


# ================================================================
# 6. 키워드 가변 인자 (Keyword Variable-length Argument, **kwargs)
# ================================================================
# 이름=값 형태로 몇 개가 들어올지 모를 때 **kwargs를 사용한다.
# kwargs라는 이름으로 입력값들을 모아 딕셔너리로 만든다.

def profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
    return kwargs


d = {"name": "크롱", "age": 4, "kind": "공룡"}
print(profile(**d))


# ===========================================================
# 7. *args와 **kwargs를 함께 사용하는 예시
# ===========================================================

# 디미가 현재 가진 돈 구하기
# - 지난 달 남은 돈 : 500원
# - 길 가다가 주운 돈 : 100원, 200원 => 가변인자 (튜플)
# - 아빠한테 받은 돈 : 10000원
# - 엄마한테 받은 돈 : 5000원 => 키워드 가변인자 (딕셔너리)

def pocket_money(start_money, *found_money, **received_money):
    total = start_money

    for money in found_money:
        total += money

    for who, money in received_money.items():
        total += money

    return total

print(pocket_money(500, 100, 200, 아빠=10000, 엄마=5000))