from fastapi import FastAPI

from .modules.skills.routes import router as skills_router


app = FastAPI()
app.include_router(skills_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
