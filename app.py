from fastapi import FastAPI
from routers import users, team, result, tournament


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Final project"}


app.include_router(users.router)
app.include_router(team.router)
app.include_router(result.router)
app.include_router(tournament.router)