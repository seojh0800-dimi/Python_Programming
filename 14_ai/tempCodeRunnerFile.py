pipeline(
    "fill-mask",
    model="distilbert/distilbert-base-uncased",
    token=token
)

result = unmasker("Python is a popular [MASK] language.")

for item in result:
    print(f"{item['token_str']} ({item['score']:.2f}) : {item['sequence']}")
