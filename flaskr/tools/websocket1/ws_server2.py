import asyncio
import websockets

async def connect():
    async with websockets.connect(
        "ws://localhost:8765",
    ) as ws:

        print("Connected to the switch.")

        await ws.send("msg1")
        response = await ws.recv()

        print("Response from the server:", response)

        await ws.send("msg2")
        response = await ws.recv()

        print("Response from the server:", response)


if __name__ == "__main__":
    asyncio.run(connect())
