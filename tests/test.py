import asyncio
import threading
from asyncio import AbstractEventLoop

# create the queue in your main loop
shared_queue = asyncio.Queue()

# loop2: runs in a separate event loop/thread
async def loop2(n, queue: asyncio.Queue, main_loop: AbstractEventLoop):
    for i in range(n):
        await asyncio.sleep(0.5)  # Simulate work
        print(f"loop2: yielding {i}")
        # schedule a put on the main loop's queue
        main_loop.call_soon_threadsafe(queue.put_nowait, i)
    # send sentinel
    main_loop.call_soon_threadsafe(queue.put_nowait, None)

def run_loop2_in_thread(n: int, queue, main_loop):
    # New event loop for this thread
    new_loop: AbstractEventLoop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    new_loop.run_until_complete(loop2(n, queue, main_loop))
    new_loop.close()

# loop1: main async function awaiting data from loop2
async def loop1():
    print("loop1: started")
    while True:
        item = await shared_queue.get()
        if item is None:  # Sentinel value received
            break
        print(f"loop1: received {item}")
    print("loop1: done")

def main():
    # explicitly create and set the main loop
    main_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(main_loop)

    # fire up loop2 in its own thread
    t = threading.Thread(
        target=run_loop2_in_thread,
        args=(5, shared_queue, main_loop),
    )
    t.start()

    # run loop1 to consume everything
    main_loop.run_until_complete(loop1())

    # wait for the thread to finish
    t.join()

if __name__ == "__main__":
    main()
