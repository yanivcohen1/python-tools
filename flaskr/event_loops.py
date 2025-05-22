import asyncio
import threading
import janus
from concurrent.futures import Future

# Run in loop2
async def task_in_loop2_streaming(data, queue):
    for i in range(3):
        await asyncio.sleep(1)
        await queue.put(f"{data} chunk {i}")
    await queue.put(None)  # Sentinel value to indicate end

# Starts loop2, creates queue, runs async task, returns sync_q to main thread
def start_loop2_and_create_queue(data, result_future: Future):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def setup():
        queue = janus.Queue()
        result_future.set_result((loop, queue.sync_q, queue.async_q))
        await task_in_loop2_streaming(data, queue.async_q)
        # Wait until loop1 has consumed all items
        await loop.run_in_executor(None, queue.sync_q.join)
        queue.close()
        await queue.wait_closed()
        loop.stop()

    loop.create_task(setup())
    loop.run_forever()
    loop.close()

# In loop1 (main thread)
async def run_loop2_task_from_loop1(data):
    result_future = Future()

    # Start loop2 in a thread
    t = threading.Thread(target=start_loop2_and_create_queue, args=(data, result_future))
    t.start()

    # Wait for loop2 to give us the queues
    loop2, sync_q, async_q = result_future.result()

    async def result_stream():
        loop = asyncio.get_running_loop()
        try:
            while True:
                item = await loop.run_in_executor(None, sync_q.get)
                sync_q.task_done()  # Mark as consumed
                if item is None:
                    break
                # print("Loop1: got item from loop2:", item)
                yield item
        except janus.ShutDown:
            pass
        finally:
            t.join()

    return result_stream()

# Main
async def main():
    print("Loop1: awaiting streaming result from loop2")
    async for chunk in await run_loop2_task_from_loop1("DATA"):
        print("Loop1 received:", chunk)

asyncio.run(main())
