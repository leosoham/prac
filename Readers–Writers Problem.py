# ---------------------------------------------------------
# Readers-Writers Problem using Python Threads
# Writer Priority Version
# ---------------------------------------------------------

import threading
import time
import random

class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.writer_active = False
        self.waiting_writers = 0

        self.lock = threading.Lock()
        self.read_ok = threading.Condition(self.lock)
        self.write_ok = threading.Condition(self.lock)

    # ----------------------- Reader Entry -----------------------
    def reader_enter(self, reader_id):
        with self.lock:
            while self.writer_active or self.waiting_writers > 0:
                self.read_ok.wait()

            self.readers += 1
            print(f"Reader {reader_id} STARTED reading. Active Readers = {self.readers}")

    # ----------------------- Reader Exit ------------------------
    def reader_exit(self, reader_id):
        with self.lock:
            self.readers -= 1
            print(f"Reader {reader_id} FINISHED reading. Active Readers = {self.readers}")

            if self.readers == 0:
                self.write_ok.notify()

    # ----------------------- Writer Entry -----------------------
    def writer_enter(self, writer_id):
        with self.lock:
            self.waiting_writers += 1

            while self.readers > 0 or self.writer_active:
                self.write_ok.wait()

            self.waiting_writers -= 1
            self.writer_active = True
            print(f"Writer {writer_id} STARTED writing.")

    # ----------------------- Writer Exit ------------------------
    def writer_exit(self, writer_id):
        with self.lock:
            self.writer_active = False
            print(f"Writer {writer_id} FINISHED writing.")

            # Writers get priority
            if self.waiting_writers > 0:
                self.write_ok.notify()
            else:
                self.read_ok.notify_all()


# ---------------------------------------------------------
# Reader Thread Function
# ---------------------------------------------------------
def reader(lock, reader_id):
    while True:
        time.sleep(random.uniform(0.5, 2))  # Simulate arrival
        lock.reader_enter(reader_id)
        time.sleep(random.uniform(0.5, 1.5))  # Simulate reading
        lock.reader_exit(reader_id)


# ---------------------------------------------------------
# Writer Thread Function
# ---------------------------------------------------------
def writer(lock, writer_id):
    while True:
        time.sleep(random.uniform(1, 3))  # Simulate arrival
        lock.writer_enter(writer_id)
        time.sleep(random.uniform(0.5, 1.5))  # Simulate writing
        lock.writer_exit(writer_id)


# ---------------------------------------------------------
# Main Driver Program
# ---------------------------------------------------------
if __name__ == "__main__":
    rw_lock = ReadWriteLock()

    # Create readers
    for i in range(3):
        threading.Thread(target=reader, args=(rw_lock, i+1), daemon=True).start()

    # Create writers
    for i in range(2):
        threading.Thread(target=writer, args=(rw_lock, i+1), daemon=True).start()

    # Keep main thread alive
    while True:
        time.sleep(1)
