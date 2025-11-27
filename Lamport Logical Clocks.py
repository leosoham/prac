# --------------------------------------------------------------------
# Lamport Logical Clock + Distributed Mutual Exclusion Simulation
# --------------------------------------------------------------------
# Each process:
#   - has a logical clock
#   - sends REQUEST(timestamp)
#   - waits for REPLY messages
#   - executes critical section
#   - sends RELEASE to others
# Mutual exclusion maintained using Lamport timestamp ordering
# --------------------------------------------------------------------

import heapq
import threading
import time
import random


class Message:
    def __init__(self, msg_type, timestamp, sender):
        self.type = msg_type      # REQUEST, REPLY, RELEASE
        self.timestamp = timestamp
        self.sender = sender


class Process:
    def __init__(self, pid, total_processes):
        self.pid = pid
        self.clock = 0
        self.total = total_processes

        self.queue = []           # Priority queue (min-heap)
        self.replies = 0          # Replies received

        self.lock = threading.Lock()
        self.network = None       # Will be set later

    # ----------------- Update Logical Clock -------------------
    def update_clock(self, received_ts=None):
        with self.lock:
            if received_ts is not None:
                self.clock = max(self.clock, received_ts) + 1
            else:
                self.clock += 1

    # ----------------- Send Message ---------------------------
    def send(self, receiver, msg_type):
        self.update_clock()
        msg = Message(msg_type, self.clock, self.pid)
        self.network.deliver(receiver, msg)

    # ----------------- Broadcast Message ----------------------
    def broadcast(self, msg_type):
        for p in range(self.total):
            if p != self.pid:
                self.send(p, msg_type)

    # ----------------- Handle incoming message ----------------
    def receive(self, msg):
        self.update_clock(msg.timestamp)

        if msg.type == "REQUEST":
            heapq.heappush(self.queue, (msg.timestamp, msg.sender))
            self.send(msg.sender, "REPLY")

        elif msg.type == "REPLY":
            self.replies += 1

        elif msg.type == "RELEASE":
            # Remove sender from queue
            self.queue = [(t, s) for (t, s) in self.queue if s != msg.sender]
            heapq.heapify(self.queue)

    # ----------------- Request Critical Section ----------------
    def request_cs(self):
        print(f"Process {self.pid} REQUESTS CS")
        self.update_clock()
        heapq.heappush(self.queue, (self.clock, self.pid))
        self.broadcast("REQUEST")

        # Wait for replies
        while self.replies < self.total - 1:
            time.sleep(0.1)

        # Check if this request is at top of priority queue
        while True:
            if self.queue[0][1] == self.pid:
                break
            time.sleep(0.1)

        print(f">>> Process {self.pid} ENTERS CS")

    # ----------------- Release Critical Section ----------------
    def release_cs(self):
        print(f"<<< Process {self.pid} EXITS CS")

        # Remove itself from queue
        self.queue = [(t, s) for (t, s) in self.queue if s != self.pid]
        heapq.heapify(self.queue)

        self.replies = 0
        self.broadcast("RELEASE")


# ---------------- Network Simulation -------------------------
class Network:
    def __init__(self, processes):
        self.processes = processes
        for p in processes:
            p.network = self

    def deliver(self, receiver, msg):
        # Simulate random network delay
        time.sleep(random.uniform(0.1, 0.3))
        self.processes[receiver].receive(msg)


# ---------------- Simulation Driver -------------------------
def process_thread(process):
    time.sleep(random.uniform(0.5, 2))
    process.request_cs()

    # Critical Section Simulation
    time.sleep(random.uniform(1, 2))

    process.release_cs()


if __name__ == "__main__":
    NUM_PROCESSES = 3

    processes = [Process(i, NUM_PROCESSES) for i in range(NUM_PROCESSES)]
    network = Network(processes)

    threads = []

    for p in processes:
        t = threading.Thread(target=process_thread, args=(p,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\nSimulation Complete.")
