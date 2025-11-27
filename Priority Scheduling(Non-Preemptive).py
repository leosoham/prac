# ----------------------------------------------------
# PRIORITY SCHEDULING (NON-PREEMPTIVE)
# ----------------------------------------------------

def priority_non_preemptive(processes):
    procs = [p.copy() for p in processes]
    n = len(procs)
    time = 0
    completed = 0
    result = []

    while completed < n:
        ready = [p for p in procs if p["arrival"] <= time and "done" not in p]

        if not ready:
            time += 1
            continue

        # Lowest number = highest priority
        ready.sort(key=lambda x: x["priority"])
        current = ready[0]

        current["start"] = time
        time += current["burst"]
        current["completion"] = time
        current["turnaround"] = current["completion"] - current["arrival"]
        current["waiting"] = current["turnaround"] - current["burst"]
        current["done"] = True

        result.append(current)
        completed += 1

    return result


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

    result = priority_non_preemptive(processes)
    for p in result:
        print(p)
