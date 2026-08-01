from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers import users, team, result, tournament

app = FastAPI(
    title="Tournament API",
    description="REST API for managing tournaments, teams, players and results.",
    version="1.0.0",
)
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home():
    return {"message": "Final project"}


@app.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse(request, "chat.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        # Client closed the connection — nothing left to do.
        return


app.include_router(users.router)
app.include_router(team.router)
app.include_router(result.router)
app.include_router(tournament.router)
