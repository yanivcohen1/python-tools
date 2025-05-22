import asyncio
import threading

def start_loop(loop, name):
    asyncio.set_event_loop(loop)
    print(f"Starting loop in thread: {name}")
    loop.run_forever()

async def hello(name):
    while True:
        print(f"Hello from {name}")
        await asyncio.sleep(1)

# Create two event loops
loop1 = asyncio.new_event_loop()
loop2 = asyncio.new_event_loop()

# Schedule coroutines on each loop
loop1.call_soon_threadsafe(asyncio.create_task, hello("loop1"))# run async hello in tread async loop1
loop2.call_soon_threadsafe(asyncio.create_task, hello("loop2"))# run asynchello in tread async loop2

# Start loops in separate threads
t1 = threading.Thread(target=start_loop, args=(loop1, "Thread-1"))# tread for async loop1
t2 = threading.Thread(target=start_loop, args=(loop2, "Thread-2"))# tread for async loop2

t1.start()
t2.start()
