
save_dir = os.path.join(BASE_DIR, "model", "my_sentiment_model")

model.save_pretrained(save_dir)         # 학습한 모델 저장 (고쳐진 가중치 + 설정)
tokenizer.save_pretrained(save_dir)     # 토크나이저 저장 (모델과 같은 폴더에)
