import asyncio
import sys
from action import Action
from engine import calibrate_new_displays, where_now
import ws_server

async def test():
    while True:
        client = where_now()
        if client:
            print(client.id)
            await client.send_action(Action.AIM)
            await asyncio.sleep(1)
            await client.send_action(Action.WELCOME)
        else:
            await asyncio.sleep(1)

async def main():
    asyncio.create_task(ws_server.start_websocket_server())
    asyncio.create_task(test())
    import aioconsole
    while True:
        line = await aioconsole.ainput('>>')
        if line == 'c':
            await calibrate_new_displays()
        if line == "exit":
            break


if __name__ == "__main__":
    asyncio.run(main())