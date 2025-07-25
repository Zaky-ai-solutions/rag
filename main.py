from fastapi import FastAPI

app = FastAPI()

@app.get("/welcome")
def welcome():
    return {"message": "WELCOME TO OUR WORLD"}