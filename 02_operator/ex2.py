# 비트 연산자 
a = 5                # 0000 0101
b = 3                # 0000 0011
print(a & b)         # 0000 0001
print(a | b)         # 0000 0111
print(a ^ b)         # 0000 0110
print(a << 1)        # 5 -> 10 -> 20 -> 40
print(40 >> b)       # 5
print(~a)            # 1111 1010 -> 1111 1010 (-6)


# 멤버십 연산자
print("a" in "apple")  # True
print(3 in [1, 2, 3])  # True

# 삼항 연산자
# int max = a > b ? a : b ( C언어 )
# 파이썬에서는 아래와 같이 표현
a = 10
b = 20
max = a if a > b else b
print(max)  # 20

# a가 짝수면 "짝" , 홀수면 "홀" 출력
print("짝") if a % 2 == 0 else print("홀")

 
# 90점 이상이면 A, 80점 이상이면 B, 70점 이상이면 C, 70점 미만이면 F
score = 85
# if score >= 90:
#     print("A")
# elif score >= 80:
#     print("B")
# elif score >= 70:
#     print("C")
# else:
#     print("F")

grade = "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(grade)


