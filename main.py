import time
import threading
from fastapi import FastAPI, HTTPException
from queue import Queue, Full, Empty

app = FastAPI()

# Constants
MAX_QUEUE_SIZE = 10   # Max items queue can hold
MIN_THREADS = 1       # Minimum number of worker threads
MAX_THREADS = 5       # Maximum number of worker threads
CHECK_INTERVAL = 60   # Supervisor checks every 60 seconds

task_queue = Queue(maxsize=MAX_QUEUE_SIZE)
worker_threads = []
thread_lock = threading.Lock()


def worker():
    """Worker function that continuously processes tasks when available."""
    while True:
        try:
            # Ask queue for somthing to do
            item = task_queue.get(timeout=10)  # Wait for task
            print(f"Processing: {item}")  # Simulate processing
            time.sleep(3)  # Simulate work time
            task_queue.task_done()  # Mark task complete
        except Empty:
            with thread_lock:
                if len(worker_threads) > MIN_THREADS:
                    print("Shutting down extra worker.")
                    worker_threads.remove(threading.current_thread())
                    break  # Exit thread if it's no longer needed
            time.sleep(1)  # Prevent CPU overuse


def supervisor():
    """Manages worker threads dynamically."""
    while True:
        time.sleep(CHECK_INTERVAL)  # Run every minute

        with thread_lock:
            queue_size = task_queue.qsize()
            active_threads = len(worker_threads)

            # Spin up new threads if queue is not empty and we're below max threads
            if queue_size > 0 and active_threads < MAX_THREADS:
                new_threads_needed = min(
                    queue_size, MAX_THREADS - active_threads)
                for _ in range(new_threads_needed):
                    thread = threading.Thread(target=worker, daemon=True)
                    thread.start()
                    worker_threads.append(thread)
                print(
                    f"Spawned {new_threads_needed} new worker(s). Total workers: {len(worker_threads)}")

            # Scale down if queue is empty and we have more than MIN_THREADS
            if queue_size == 0:
                # Iterate over a copy of the list
                for thread in worker_threads[:]:
                    if len(worker_threads) > MIN_THREADS:
                        if not thread.is_alive():
                            # Clean up dead threads
                            worker_threads.remove(thread)
                        else:
                            print("Stopping a worker due to inactivity.")
                            worker_threads.remove(thread)
                            break  # Kill only one thread per cycle


# Start the supervisor thread
supervisor_thread = threading.Thread(target=supervisor, daemon=True)
supervisor_thread.start()


# Request assigned to server worker
@app.post("/enqueue/")
def enqueue_task(item: str):
    """Add a task to the queue if space is available, otherwise return 429."""
    # Is the queue at max length?
    try:
        # If No
        # Add the request to the queue
        task_queue.put_nowait(item)
        return {"message": f"Task '{item}' added to queue", "queue_size": task_queue.qsize()}
    except Full:
        raise HTTPException(
            # If Yes
            # Too many requests! Queue is full.
            status_code=429, detail="Too many requests! Queue is full.")


@app.get("/queue_size/")
def get_queue_size():
    """Check current queue size."""
    return {"queue_size": task_queue.qsize(), "active_workers": len(worker_threads)}
