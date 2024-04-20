#!/usr/bin/env python
from action import Action
from client import Client
import engine
import asyncio
import websockets
from ujson import loads

from www.cv import SERVER_IP

async def handle_client(websocket):
    print("New connection from", websocket.remote_address)
    asyncio.create_task(keep_alive(websocket))

    meta = loads(await websocket.recv())

    client = Client(websocket, meta.get('id', None))
    if meta['display']:
        print('Is display.')
        await engine.add_new_display(client)
    else:
        engine.add_camera()
        print('Is camera only')
        try:
            while True:
                posture_txt = await websocket.recv()
                posture = loads(posture_txt)
                await engine.handle_posture(client, posture)
        except websockets.ConnectionClosedError:
            print('Connection closed')
            return
    await asyncio.Future()
        
async def keep_alive(websocket):
    try:
        while True:
            await websocket.ping()
            await asyncio.sleep(1)
    except:
        pass

async def start_websocket_server():
    async with websockets.serve(handle_client, SERVER_IP, 8001):
        await asyncio.Future()  # run forever