import asyncio
from action import Action
from client import Client

new_clients = asyncio.Queue()
clients = []
ranges = []

postures = {} # client_id: posture

async def add_new_display(client: Client):
    new_clients.put_nowait(client)
    await client.send_action(Action.WELCOME)

async def calibrate_new_displays():
    print('Calibrating all new displays...')
    await asyncio.sleep(5)
    while not new_clients.empty():
        client = new_clients.get_nowait()
        print('Calibrating display #', client.id)
        await client.send_action(Action.CALIBRATE)
        await asyncio.sleep(5)
        client.set_postures(postures)
        await client.send_action(Action.WELCOME)
        clients.append(client)

async def handle_posture(client: Client, posture):
    postures[client.id] = posture

def where_now():
    dots = [(client, client.dot(postures)) for client in clients]
    if dots:
        return max(dots, key=lambda x: x[1])[0]
    return None
