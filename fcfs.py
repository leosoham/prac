# -------------------------------------------
# FCFS CPU Scheduling (Non-preemptive)
# -------------------------------------------

def fcfs(processes):
    # Sort by arrival time
    processes.sort(key=lambda x: x['arrival'])

    current_time = 0
    for p in processes:
        if current_time < p['arrival']:
            current_time = p['arrival']

        p['start'] = current_time
        current_time += p['burst']
        p['completion'] = current_time
        p['turnaround'] = p['completion'] - p['arrival']
        p['waiting'] = p['turnaround'] - p['burst']

    return processes


if __name__ == "__main__":
    processes = [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 1, "burst": 3},
        {"pid": "P3", "arrival": 2, "burst": 8},
        {"pid": "P4", "arrival": 3, "burst": 6}
    ]

    result = fcfs(processes)
    for p in result:
        print(p)
