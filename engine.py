import asyncio

import websockets
from action import Action
from client import Client
from utils import *
import pickle

def load_clients():
    try:
        with open('state.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

new_clients = asyncio.Queue()
clients = load_clients()
ranges = []

postures = {} # client_id: posture

order_buffer = []

hunted_idx = 0

aimed_client = None
async def game_loop():
    global aimed_client
    while True:
        try:
            state = where_now()
            print(state)
            for client, shooting in state:
                if client:
                    print('Aiming at', client.id)
                    aimed_client = client
                    await client.send_action(Action.AIM)
            await asyncio.sleep(1)
            for client, shooting in state:
                if client:
                    await client.send_action(Action.WELCOME)
        except websockets.ConnectionClosedError:
            print("Error in game loop:", sys.exc_info()[0])
            print('restarting')
            await asyncio.sleep(1)

async def add_new_display(client: Client):
    new_clients.put_nowait(client)
    await client.send_action(Action.WELCOME)
    status()

def add_camera():
    status()

def status():
    print('Clients:', len(clients) + new_clients.qsize(), 'Cameras:', len(postures))

async def calibrate_new_displays():
    print('Calibrating all new displays...')
    await asyncio.sleep(5)
    while not new_clients.empty():
        client = new_clients.get_nowait()
        while True:
            print('Calibrating display #', client.id)
            await client.send_action(Action.CALIBRATE)
            await asyncio.sleep(5)
            ok = client.set_postures(postures)
            await client.send_action(Action.WELCOME)
            if ok:
                break
            else:
                print('Missing required info in frame, retrying')
        clients.append(client)
        print('asdasdsad', len(clients))

async def handle_posture(client: Client, posture):
    postures[client.id] = posture

def where_now():
    # Returns client, is_shot, client, is_shot
    return [(where_hand_now(i), False) for i in range(1, 2)]

def where_hand_now(hand_idx):
    directions_by_camera = {}
    for camera_id in postures.keys():
        hand = posture_to_hands(postures[camera_id])[hand_idx]
        directions_by_camera[camera_id] = pointing_direction(hand)
    dots = [(client, client.dot(directions_by_camera)) for client in clients]

    if dots:
        return max(dots, key=lambda x: x[1])[0]
    return None

def save_clients():
    with open('state.pickle', 'wb') as f:
        pickle.dump(clients, f)

async def hunted_move_left():
    await hunted_move(-1)

async def hunted_move_right():
    await hunted_move(1)

async def order_clients():
    order_buffer.append(aimed_client)
    if len(order_buffer) == len(clients):
        clients.clear()
        clients.extend(order_buffer)
        print('Clients order fixed!')
    else:
        print(len(clients) - len(order_buffer), 'clients left to order')
    

async def hunted_move(d):
    global hunted_idx
    client = clients[hunted_idx]
    client.enemy = False
    await client.send_action(Action.EMPTY)
    hunted_idx = (hunted_idx + d) % len(clients)
    client = clients[hunted_idx]
    client.enemy = True
    await client.send_action(Action.ENEMY)