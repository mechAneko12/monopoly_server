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

from . import schemas
from .manager import WebSocketManager

app = FastAPI()

ws_manager = WebSocketManager()


@app.post(
    '/buy_space',
    response_model=schemas.Message)
async def buy_space(user_name: str, room_name: str, info: schemas.BuySpace):
    # なんか処理

    # roomに通知
    info_name = 'buy_space'
    detail = {
        'user_name': user_name,
        'space_id': info.space_id
    }
    await ws_manager.broadcast_message_to_room(room_name, info_name, detail)

    return {'message': f'{user_name} bought {info.space_id}'}

@app.websocket('/ws')
async def websocket_endpoint(user_name: str, room_name: str, ws: WebSocket):  
    await ws_manager.connect(ws, user_name, room_name)
    print(ws_manager.active_connections)
    logger.info(f'connect to client "{user_name}"')
    
    # clientの初期化

    # roomがあるかどうか
    # roomがある時、状態はどうか
    # すでに途中の場合、状態をclientに反映

    try:
        # 特に何もしないが、websocketの接続の切断を確認するためにreceive_jsonを入れておく
        # 接続が切れるとWebsocketDisconnectがraiseされる
        while True:
            await ws.receive_json()
    
    except WebSocketDisconnect:
        logger.info(f'disconnect  client "{user_name}"')
        ws_manager.disconnect(user_name, room_name)
        print(ws_manager.active_connections)


########################## sample #########################
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <button type="button" onclick="buySpace()">buy space</button>
        
        <ul id='messages'>
        </ul>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.12.3/jquery.min.js"></script>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws?user_name=sample_user&room_name=sample_room");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };

            function buySpace() {
                $.ajax({
                    url: '/buy_space?user_name=sample_user&room_name=sample_room',
                    type: 'POST',
                    headers: {     'Accept': 'application/json',     'Content-Type': 'application/json',   },
                    data: JSON.stringify({space_id: 1})
                }).done(function(data, textStatus, jqXHR) {
                    console.log(data);
                }).fail(function (data, textStatus, errorThrown) {
                    console.log(data);
                });
            }
        </script>
    </body>
</html>
"""


@app.get('/')
async def get():
    return HTMLResponse(html)