from fastapi import FastAPI


app = FastAPI()


@app.get("/ping")
async def root():
    return {"ping": "pong v3!"}
