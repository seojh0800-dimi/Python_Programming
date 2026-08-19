# 입출력 처리

## 1개 입력 ##
a= input()
print(a)
print(type(a))

## 정수변환 ##
a = input()
a = int(a)
print(a)
print(type(a))

## 한번에 쓰자 ##
a = int(input())
print(a)
print(type(a))

## 실수 입력 ##
a = float(input())
print(a)
print(a, type(a))


## 정수 2개 입력
a, b = map(int, input().split())
print(a, b)