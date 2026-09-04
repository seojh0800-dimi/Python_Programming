# 반복문 : while문, for문

# while문
# 1 ~ 10 까지 반복 출력
i = 1
while i <= 10:
    print(i)
    i += 1
    if i == 6:
        break
nums = [1, 2, 3, 4, 5]
target = 3
i = 0

while i < len(nums):
    if nums[i] == target:
        print(f"{target} 찾음")
        break
    i += 1
else:
    print(f"{target} 없음")

# if not found:
#     print(f"{target} 없음")

# 1 ~ 10 까지 합
i = 1
tot = 0
while i <= 10:
    tot += i
    i += 1
else:
    print(f"합 : {tot}")

# 1 ~ 10 중에 짝수만 더해지도록
i = 1
tot = 0
while i <= 10:
    if i % 2 == 0: 
        tot += i
    i += 1
else:
    print(f"합 : {tot}")