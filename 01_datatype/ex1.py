# 변수
a = 2
b = 3
print(a,end="")
print(b)
print(a, b, sep="")

a,b = 2,3

print (a,b)

a = b = c = 0

# 값 swap
a,b = 2,3
a,b = b,a

print(a,b)

# 변수명 규칙 (C와 동일)
# 알파벳, 숫자, 특수문자 (_)만 가능
# 숫자로 시작 불가
# 예약어 사용 불가
# snake_case
# camelCase
# strHungarianCase
# !name = "pororo"
# 2name = "pororo"
#class = "test"