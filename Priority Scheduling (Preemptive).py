# ----------------------------------------------------
# PRIORITY SCHEDULING (PREEMPTIVE)
# ----------------------------------------------------

def priority_preemptive(processes):
    procs = [p.copy() for p in processes]
    for p in procs:
        p["remaining"] = p["burst"]

    time = 0
    completed = 0
    n = len(procs)
    gantt = []
    last_pid = None

    while completed < n:
        ready = [p for p in procs if p["arrival"] <= time and p["remaining"] > 0]

        if not ready:
            time += 1
            continue

        # Lowest priority number first
        ready.sort(key=lambda x: x["priority"])
        current = ready[0]

        if last_pid != current["pid"]:
            gantt.append({"pid": current["pid"], "start": time})
            last_pid = current["pid"]

        current["remaining"] -= 1
        time += 1

        if current["remaining"] == 0:
            current["completion"] = time
            completed += 1

    # Calculate metrics
    for p in procs:
        p["turnaround"] = p["completion"] - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]

    return procs, gantt


# -------------------------
# Example run
# -------------------------
if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 4, "priority": 2},
        {"pid": "P2", "arrival": 1, "burst": 3, "priority": 1},
        {"pid": "P3", "arrival": 2, "burst": 1, "priority": 3},
        {"pid": "P4", "arrival": 3, "burst": 2, "priority": 2}
    ]

    result, gantt = priority_preemptive(processes)

    print("Process Table:")
    for p in result:
        print(p)

    print("\nGantt Chart:")
    for g in gantt:
        print(g)
