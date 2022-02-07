from fastapi import FastAPI

from .modules import auth, skills

app = FastAPI()
app.include_router(auth.router)
app.include_router(skills.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
