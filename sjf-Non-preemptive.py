# ----------------------------------------------------
# SJF NON-PREEMPTIVE CPU Scheduling
# ----------------------------------------------------

def sjf_non_preemptive(processes):
    n = len(processes)
    procs = [p.copy() for p in processes]
    time = 0
    completed = 0
    result = []

    while completed < n:

        ready = [p for p in procs if p['arrival'] <= time and 'done' not in p]

        if not ready:
            time += 1
            continue

        # Choose shortest burst time
        ready.sort(key=lambda x: x['burst'])
        p = ready[0]

        p['start'] = time
        time += p['burst']
        p['completion'] = time
        p['turnaround'] = p['completion'] - p['arrival']
        p['waiting'] = p['turnaround'] - p['burst']
        p['done'] = True

        result.append(p)
        completed += 1

    return result


if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 1, "burst": 3},
        {"pid": "P3", "arrival": 2, "burst": 8},
        {"pid": "P4", "arrival": 3, "burst": 6}
    ]

    result = sjf_non_preemptive(processes)
    for p in result:
        print(p)
