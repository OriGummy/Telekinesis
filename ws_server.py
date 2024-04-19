#!/usr/bin/env python
from action import Action
from client import Client
import engine
import asyncio
import websockets
from ujson import loads

async def handle_client(websocket):
    print("New connection from", websocket.remote_address)
    asyncio.create_task(keep_alive(websocket))

    meta = loads(await websocket.recv())

    client = Client(websocket, meta.get('id', None))
    if meta['display']:
        print('Is display.')
        await engine.add_new_display(client)
    else:
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
    while True:
        await websocket.ping()
        await asyncio.sleep(1)

async def start_websocket_server():
    async with websockets.serve(handle_client, "172.30.154.163", 8001):
        await asyncio.Future()  # run forever