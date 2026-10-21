
실행 결과 예상해보기
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write("첫 번째 줄\n")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write("두번째 줄\n")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    print(f.read())

with open(FILE_PATH, "a", encoding="utf-8") as f:
    f.write("세번째 줄\n")

with open(FILE_PATH, "r", encoding="utf-8") as f:
    print(f.read())