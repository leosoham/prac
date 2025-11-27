# ----------------------------------------------------
# ROUND ROBIN CPU Scheduling
# ----------------------------------------------------

def round_robin(processes, quantum):
    # Deep copy + initialize
    procs = [p.copy() for p in processes]
    for p in procs:
        p["remaining"] = p["burst"]

    time = 0
    queue = []
    completed = 0
    n = len(procs)

    # Sort by arrival
    procs.sort(key=lambda x: x["arrival"])

    # Start with first arrival
    i = 0
    while completed < n:
        # Add all arriving processes to queue
        while i < n and procs[i]["arrival"] <= time:
            queue.append(procs[i])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)

        # Execute current process
        exec_time = min(quantum, current["remaining"])
        current["remaining"] -= exec_time
        time += exec_time

        # Add newly arrived processes during execution
        while i < n and procs[i]["arrival"] <= time:
            queue.append(procs[i])
            i += 1

        if current["remaining"] > 0:
            queue.append(current)
        else:
            current["completion"] = time
            completed += 1

    # Calculate metrics
    for p in procs:
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]

    return procs


# -------------------------
# Example run
# -------------------------
if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 1, "burst": 4},
        {"pid": "P3", "arrival": 2, "burst": 2},
        {"pid": "P4", "arrival": 3, "burst": 1}
    ]

    quantum = 2
    result = round_robin(processes, quantum)

    for p in result:
        print(p)
