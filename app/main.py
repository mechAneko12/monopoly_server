from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO

################### LOGGER ###################  
formatter = Formatter('%(levelname)s: %(asctime)s - %(message)s (%(name)s)')
logger = getLogger('app')
handler = StreamHandler()
handler.setLevel(DEBUG)
handler.setFormatter(formatter)

logger.setLevel(DEBUG)
logger.addHandler(handler)

################### app ###################  

from fastapi import (
    Depends, FastAPI, HTTPException, Request, BackgroundTasks, WebSocket, WebSocketDisconnect
)
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
    FileResponse,
    ORJSONResponse,
)

from sqlalchemy.orm import Session
import asyncio
import websockets

app = FastAPI()


@app.get("/something/{item_id}")
async def read_item(item_id):
    return {"something": item_id}