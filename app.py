from fastapi import FastAPI, WebSocket
from routers import users, team, result, tournament
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "Final project"}
@app.get("/chat", response_class=HTMLResponse)
async def chat():
    return templates.TemplateResponse("chat.html", {"request": {}})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")




app.include_router(users.router)
app.include_router(team.router)
app.include_router(result.router)
app.include_router(tournament.router)