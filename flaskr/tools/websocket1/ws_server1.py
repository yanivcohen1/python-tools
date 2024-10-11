import asyncio
import websockets

async def runServer():
    server = await websockets.serve(onConnect, "localhost", port=8765)
    print("Server started listening to new connections...")
    await server.wait_closed()


async def onConnect(ws):
    try:
        while True:
            message = await ws.recv()

            if message == "msg1":
                await ws.send("response from server 1")
            elif message == "msg2":
                await ws.send("response from server 2")
    except websockets.exceptions.ConnectionClosedOK:
        print("Client closed...")


if __name__ == "__main__":
    asyncio.run(runServer())
