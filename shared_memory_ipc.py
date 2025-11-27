# -----------------------------------------------------------
# IPC Using Shared Memory in Python (multiprocessing)
# Two processes communicating via Value & Array
# -----------------------------------------------------------

from multiprocessing import Process, Value, Array, Lock
import time
import random

# ------------------------ Writer Process ------------------------
def writer(shared_value, shared_array, lock):
    for i in range(5):
        time.sleep(1)

        with lock:  # Enter critical section
            shared_value.value += 10                   # Update shared integer
            shared_array[i] = random.randint(1, 100)  # Update shared array

            print(f"[Writer] Updated value = {shared_value.value}, "
                  f"Array = {list(shared_array)}")

# ------------------------ Reader Process ------------------------
def reader(shared_value, shared_array, lock):
    for _ in range(5):
        time.sleep(1.5)

        with lock:  # Enter critical section
            print(f"[Reader] Read value = {shared_value.value}, "
                  f"Array = {list(shared_array)}")

# ------------------------ Main Program ------------------------
if __name__ == "__main__":
    # Shared memory
    shared_value = Value('i', 0)      # integer (initial value = 0)
    shared_array = Array('i', 5)      # array of 5 integers

    # Lock for synchronization
    lock = Lock()

    # Create two processes
    p1 = Process(target=writer, args=(shared_value, shared_array, lock))
    p2 = Process(target=reader, args=(shared_value, shared_array, lock))

    # Start processes
    p1.start()
    p2.start()

    # Wait for both to finish
    p1.join()
    p2.join()

    print("Shared Memory IPC completed.")
