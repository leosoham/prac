# -------------------------------------------------------------------------
# Readers–Writers Problem using MONITORS in Python
# -------------------------------------------------------------------------
# A Monitor is represented using:
# - a shared class
# - internal lock for mutual exclusion
# - condition variables for synchronization
# - methods that act as monitor procedures
# -------------------------------------------------------------------------

import threading
import time
import random


class ReadersWritersMonitor:
    def __init__(self):
        self.readers = 0                 # Number of active readers
        self.writer_active = False       # Is a writer currently writing?
        self.waiting_writers = 0         # Writers waiting (writers priority)

        # Internal monitor lock
        self.monitor_lock = threading.Lock()

        # Condition variables inside the monitor
        self.can_read = threading.Condition(self.monitor_lock)
        self.can_write = threading.Condition(self.monitor_lock)

    # ---------------------- Monitor Procedure: Reader Enter ----------------------
    def reader_enter(self, rid):
        with self.monitor_lock:
            while self.writer_active or self.waiting_writers > 0:
                self.can_read.wait()

            self.readers += 1
            print(f"Reader {rid} STARTED reading | Readers Active = {self.readers}")

    # ---------------------- Monitor Procedure: Reader Exit -----------------------
    def reader_exit(self, rid):
        with self.monitor_lock:
            self.readers -= 1
            print(f"Reader {rid} FINISHED reading | Readers Active = {self.readers}")

            if self.readers == 0:
                # Last reader wakes up writers
                self.can_write.notify()

    # ---------------------- Monitor Procedure: Writer Enter ----------------------
    def writer_enter(self, wid):
        with self.monitor_lock:
            self.waiting_writers += 1

            while self.readers > 0 or self.writer_active:
                self.can_write.wait()

            self.waiting_writers -= 1
            self.writer_active = True
            print(f"Writer {wid} STARTED writing")

    # ---------------------- Monitor Procedure: Writer Exit -----------------------
    def writer_exit(self, wid):
        with self.monitor_lock:
            self.writer_active = False
            print(f"Writer {wid} FINISHED writing")

            # Writers get priority
            if self.waiting_writers > 0:
                self.can_write.notify()
            else:
                self.can_read.notify_all()


# -------------------------------------------------------------------------
# Reader Thread Function
# -------------------------------------------------------------------------
def reader(monitor, rid):
    while True:
        time.sleep(random.uniform(0.5, 2.0))  # Delay before reading
        monitor.reader_enter(rid)

        time.sleep(random.uniform(0.5, 1.5))  # Reading process
        monitor.reader_exit(rid)


# -------------------------------------------------------------------------
# Writer Thread Function
# -------------------------------------------------------------------------
def writer(monitor, wid):
    while True:
        time.sleep(random.uniform(1.0, 3.0))  # Delay before writing
        monitor.writer_enter(wid)

        time.sleep(random.uniform(0.5, 1.5))  # Writing process
        monitor.writer_exit(wid)


# -------------------------------------------------------------------------
# Main Driver
# -------------------------------------------------------------------------
if __name__ == "__main__":
    monitor = ReadersWritersMonitor()

    # Start Readers
    for i in range(3):
        threading.Thread(target=reader, args=(monitor, i+1), daemon=True).start()

    # Start Writers
    for i in range(2):
        threading.Thread(target=writer, args=(monitor, i+1), daemon=True).start()

    # Keep program alive
    while True:
        time.sleep(1)
