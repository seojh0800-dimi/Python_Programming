# 연산자

# 산술 연산자

a = 10
b = 3

print(a + b)
print(a - b)
print(a * b)
print(a / b)
print(a // b)
print(a % b)
print(a ** b)

# 복합 대입 연산자
a= 0
a += 4
print(a)  # 4

a -= 2
print(a)  # 2

# 증감 연산자 => 없음
# b = a++
# a += 1

# 비교 연산자
print(3 == 3)  # True
print(3 == 3.0)  # True
print(3 != 4)  # True
print(3 > 2)  # True
print(3 < 4)  # True
print(3 >= 3)  # True
print(3 <= 4)  # True
print("apple" == "apple")  # True
print("apple" == "apble")  # False
print(1 < 2 < 3)  # True

# 논리 연산자 (and , or , not)
a = True
b = False

print(a and b)  # False
print(a or b)  # True
print(not b)  # True

# Short-circuit 테스트
a = 10
b = 0

#print(a/b)

if a > 0 or a / b:
    print("Yes")
else:
    print("No")

