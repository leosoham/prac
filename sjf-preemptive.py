# ----------------------------------------------------
# SJF PREEMPTIVE (SRTF) CPU Scheduling
# ----------------------------------------------------

def sjf_preemptive(processes):
    procs = [p.copy() for p in processes]
    for p in procs:
        p['remaining'] = p['burst']

    time = 0
    completed = 0
    n = len(procs)
    last_pid = None
    gantt = []

    while completed < n:
        # Get ready processes
        ready = [p for p in procs if p['arrival'] <= time and p['remaining'] > 0]

        if not ready:
            time += 1
            continue

        # Choose process with smallest remaining burst
        ready.sort(key=lambda x: x['remaining'])
        current = ready[0]

        # Gantt chart tracking
        if last_pid != current['pid']:
            gantt.append({"pid": current['pid'], "start": time})
            last_pid = current['pid']

        # Execute process for 1 unit
        current['remaining'] -= 1
        time += 1

        if current['remaining'] == 0:
            current['completion'] = time
            completed += 1

    # Calculate metrics
    for p in procs:
        p['turnaround'] = p['completion'] - p['arrival']
        p['waiting'] = p['turnaround'] - p['burst']

    return procs, gantt


# -------------------------
# Example run
# -------------------------
if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 1, "burst": 3},
        {"pid": "P3", "arrival": 2, "burst": 8},
        {"pid": "P4", "arrival": 3, "burst": 6}
    ]

    result, gantt = sjf_preemptive(processes)

    print("Process Details:")
    for p in result:
        print(p)

    print("\nGantt Chart:")
    for g in gantt:
        print(g)
