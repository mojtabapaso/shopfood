from typing import Dict

from fastapi import APIRouter, HTTPException, status
import json
import websockets
from websockets.exceptions import WebSocketException

router = APIRouter()
import requests




@router.get("/admin/show/users/")
async def show_users():
    async with websockets.connect('ws://127.0.0.1:1500/users/') as websocket:
        try:
            response = await websocket.recv()
            response_json = json.loads(response)["detail"]
            return response_json

        except WebSocketException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WebSocket connection problem")
        finally:
            websocket.close()


@router.post("/admin/deactivate/user/")
async def deactivate_user(data: Dict):
    async with websockets.connect('ws://127.0.0.1:1500/deactivate/user/') as websocket:
        try:
            data = {"id": data["id"]}
            json_data = json.dumps(data)
            await websocket.send(json_data)
            response = await websocket.recv()
            response_json = json.loads(response)
            raise HTTPException(status_code=response_json["status"], detail=response_json["message"])
        except WebSocketException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WebSocket connection problem")
        finally:
            websocket.close()


# import ssl
# ssl_context = ssl.create_default_context()
# ssl_context = ssl.create_default_context(min_version=ssl.TLSVersion.TLSv1_2,max_version=ssl.TLSVersion.TLSv1_2)
# import ssl
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

@router.post("/admin/activate/user/")
async def deactivate_user(data: Dict):
    async with websockets.connect('ws://127.0.0.1:1500/activate/user/') as websocket:
        try:
            data = {"id": data["id"]}
            json_data = json.dumps(data)
            await websocket.send(json_data)
            response = await websocket.recv()
            response_json = json.loads(response)
            raise HTTPException(status_code=response_json["status"], detail=response_json["message"])
        except WebSocketException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WebSocket connection problem")
        finally:
            websocket.close()


@router.get("/admin/delete/user/")
async def show_users():
    async with websockets.connect('ws://127.0.0.1:1500/users/') as websocket:
        try:
            response = await websocket.recv()
            response_json = json.loads(response)["detail"]
            return response_json

        except WebSocketException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WebSocket connection problem")
        finally:
            websocket.close()


@router.get("/admin/show/profiles/")
async def show_users():
    async with websockets.connect('ws://127.0.0.1:1500/profiles/') as websocket:
        try:
            response = await websocket.recv()
            response_json = json.loads(response)["detail"]
            return response_json

        except WebSocketException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WebSocket connection problem")
        finally:
            websocket.close()


@router.get("/admin/show/otp/")
async def show_otc_code():
    async with websockets.connect('ws://127.0.0.1:1500/otps/') as websocket:
        try:
            response = await websocket.recv()
            response_json = json.loads(response)
            return response_json

        except WebSocketException:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="WebSocket connection problem")
        finally:
            await websocket.close()
