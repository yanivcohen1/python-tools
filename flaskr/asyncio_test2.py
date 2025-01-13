import asyncio
import time

def blocking_function():
    time.sleep(3)
    return time.time()

async def unblock_function():
    return await asyncio.to_thread(blocking_function)

async def main():
    print("Starting blocking function")
    start = time.time()
    end1 = await unblock_function()
    end2 = await asyncio.gather(unblock_function(), unblock_function())
    print(f'run 1 fun took {end1-start:.2f} seconds')
    print(f'run 2 funs took {max(end2)-end1:.2f} seconds')

asyncio.run(main())
