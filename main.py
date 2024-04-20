import asyncio
import sys
import tty

import websockets
from action import Action
from engine import *
import ws_server

async def main():
    asyncio.create_task(ws_server.start_websocket_server())
    asyncio.create_task(game_loop())
    import aioconsole
    #tty.setraw(sys.stdin.fileno())
    stdin, _ = await aioconsole.stream.get_standard_streams()
    while True:
        ch = await stdin.read(1)
        if ch == b'\x03':  # ctrl-c
            break
        elif ch == b'c':
            await calibrate_new_displays()
        elif ch == b's':
            save_clients()
        elif ch == b'o':
            order_clients()
        elif ch == "\033[D": # left
            hunted_move_left()
            await asyncio.sleep(0.5)
        elif ch == "\033[C": # right
            hunted_move_right()
            await asyncio.sleep(0.5)

    #tty.setcbreak(sys.stdin.fileno())
    return
    while True:
        
        line = await aioconsole.ainput('>>')
        if line == 'c':
            await calibrate_new_displays()
        elif line == 's':
            save_clients()
        if line == "exit":
            break


if __name__ == "__main__":
    asyncio.run(main())