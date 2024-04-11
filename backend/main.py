from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def root():
    return{"message": "Hello World12345"}

@app.get("/gg")
async def root():
    return{"message": "Hello World"}
