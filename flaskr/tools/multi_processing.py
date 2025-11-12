from multiprocessing import Pool, cpu_count
import time
import random

def worker(task):
    print(f"Processing task {task}...")
    time.sleep(random.uniform(0.5, 2.0))  # simulate work
    return f"Task {task} done"

if __name__ == "__main__":
    # Limit concurrent processes to number of CPUs
    max_processes = cpu_count()
    print(f"Running up to {max_processes} processes at the same time.")

    # Create a pool with limited concurrency
    with Pool(processes=max_processes) as pool:
        # Here you can submit an "unlimited" stream of tasks
        # imap_unordered() is great for streaming large or infinite workloads
        tasks = (i for i in range(1000))  # generator = no memory blowup
        for result in pool.imap_unordered(worker, tasks, chunksize=1):
            print(result)
