#입출력 처리

# 1개 입력
a=input()
print(a)
print(type(a))

#정수 변환
a=input()
a=int(a)
print(type(a))

# 한번에 쓰자
a= int(input())
print(type(a))

# 실수 입력1
b=float(input())
print(b, type(b))

# 정수 2개 입력
# 100
# 200
a=int(input())
b=int(input())
print(a,b)

# 100 200 입력
a=input().split()
print(a)

# map 사용하기
# map(함수, 리스트)
a, b, c=map(int, input().split())
print(a, b, c)

# 리스트로 변환
a=list(map(int, input().split()))
print(a)