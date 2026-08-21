#파이썬 자료형
#1. 기본 자료형: 숫자형 (정수형, 실수형), 불리언, 문자열
#2. 컬렉션 자료형: 리스트, 튜플, 딕셔너리, 집합

# 숫자형 (정수형)
#C언어: char short int long long long int
# int

a = 10
print(a, type(a))

#2진수, 8진수, 16진수
print(bin(a),oct(a),hex(a));
print(ord("A"),chr(65))

#정수형의 데이터 표현 범위
x = pow(10,pow(10,2))
print(x)

#int 자료형의 표현 범위는 제한이 없음
#오버플로우 테스트
a = pow(2,31)-1
a+=1
print(a)

# 실수형(float)
b = 3.14
print(b, type(b))

#실수형의 표현 범위 제한
# 부동소수점 방식: 64비트 = 부호 1비트 + 지수부 11비트 = 가수부 52비트

import sys
print(sys.float_info.min)
print(sys.float_info.max)


a = 1.7*pow(10,308)
b = 1.8*pow(10,308)

print(a,b)

#실수의 오차
print(0.1+0.2)
print(0.1+0.2 == 0.3)
print(f"{0.1:.20f}")
print(f"{0.2:.20f}")

# 형변환
print(float(10))
print(int(3.14))
print(int("100"))
print(float("3.14"))
