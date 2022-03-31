"""Main module."""

import fastapi

from .modules import skills, users

app = fastapi.FastAPI()
app.include_router(users.controller)
app.include_router(skills.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
