# -------------------------------------------------------------
# Producer–Consumer Problem using Python Threads & Semaphores
# Bounded Buffer Implementation
# -------------------------------------------------------------

import threading
import time
import random


BUFFER_SIZE = 5
buffer = []  # Shared buffer

# Semaphores
empty = threading.Semaphore(BUFFER_SIZE)  # Count of empty slots
full = threading.Semaphore(0)             # Count of filled slots

# Lock for mutual exclusion
mutex = threading.Lock()


# -------------------------------------------------------------
# Producer Function
# -------------------------------------------------------------
def producer(pid):
    item_number = 1
    while True:
        time.sleep(random.uniform(0.5, 2))  # Simulate item creation

        item = f"P{pid}_Item{item_number}"
        item_number += 1

        empty.acquire()      # Wait if buffer is full
        mutex.acquire()      # Enter critical section

        buffer.append(item)
        print(f"[Producer {pid}] Produced: {item} | Buffer: {buffer}")

        mutex.release()      # Exit critical section
        full.release()       # Signal that a new item is available


# -------------------------------------------------------------
# Consumer Function
# -------------------------------------------------------------
def consumer(cid):
    while True:
        time.sleep(random.uniform(1, 3))  # Simulate consumption delay

        full.acquire()        # Wait if buffer is empty
        mutex.acquire()       # Enter critical section

        item = buffer.pop(0)
        print(f"[Consumer {cid}] Consumed: {item} | Buffer: {buffer}")

        mutex.release()       # Exit critical section
        empty.release()       # Signal that a slot is now empty


# -------------------------------------------------------------
# Main Driver
# -------------------------------------------------------------
if __name__ == "__main__":
    # Start 2 producers
    for i in range(2):
        threading.Thread(target=producer, args=(i+1,), daemon=True).start()

    # Start 2 consumers
    for i in range(2):
        threading.Thread(target=consumer, args=(i+1,), daemon=True).start()

    # Keep the main program alive
    while True:
        time.sleep(1)
