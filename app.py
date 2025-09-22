from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Added healts"}

@app.get("/health")
def health():
    return {"message": "OK"}
