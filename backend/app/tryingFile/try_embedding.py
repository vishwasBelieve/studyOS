from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-small-en-v1.5',local_files_only=True)


sentence = "Why does a recommendation need to reference the author's profile?"
embedding = model.encode(sentence).tolist()
print(embedding)