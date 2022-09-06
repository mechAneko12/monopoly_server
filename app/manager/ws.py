from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.active_connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(self, ws: WebSocket, user_name: str, room_name: str):
        await ws.accept()
        if not(room_name in list(self.active_connections.keys())):
            self.active_connections[room_name] = {}
        self.active_connections[room_name][user_name] = ws

    def disconnect(self, user_name: str, room_name: str):
        self.active_connections[room_name].pop(user_name)
    
    @staticmethod
    def _create_message(info_name: str, detail: dict):
        message = {
            'info': info_name,
            'detail': detail
        }
        return message

    async def send_message_to_user(self, user_name: str, room_name: str, info_name: str, detail: dict):
        message = self._create_message(info_name, detail)
        await self.active_connections[room_name][user_name].send_json(message)
    
    async def broadcast_message_to_room(self, room_name: str, info_name: str, detail: dict):
        message = self._create_message(info_name, detail)
        for connection in self.active_connections[room_name].values():
            await connection.send_json(message)
