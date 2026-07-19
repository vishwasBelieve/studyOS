from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "your at home page"}
