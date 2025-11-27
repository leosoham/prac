# -------------------------------------------------------------------------
# Banker's Algorithm in Python
# Deadlock Avoidance for Multiple Processes & Resources
# -------------------------------------------------------------------------

def is_safe(processes, available, maximum, allocation, need):
    """
    Safety Algorithm:
    Check if the system is in a safe state.
    """
    work = available.copy()
    finish = [False] * processes
    safe_sequence = []

    while True:
        allocated_this_round = False

        for i in range(processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                # Pretend allocation
                for j in range(len(work)):
                    work[j] += allocation[i][j]  # Release resources after execution

                safe_sequence.append(f"P{i}")
                finish[i] = True
                allocated_this_round = True

        if not allocated_this_round:
            break

    if all(finish):
        return True, safe_sequence
    else:
        return False, []


def request_resources(process_id, request, available, allocation, need, maximum):
    """
    Resource Request Algorithm:
    1. Request <= Need?
    2. Request <= Available?
    3. Try allocation → check safety
    """

    print(f"\nProcess P{process_id} requesting: {request}")

    # Step 1: Check Request <= Need
    for i in range(len(request)):
        if request[i] > need[process_id][i]:
            print("Error: Process has exceeded its maximum claim.")
            return False

    # Step 2: Check Request <= Available
    for i in range(len(request)):
        if request[i] > available[i]:
            print("Resources not available. Process must wait.")
            return False

    # Step 3: Pretend to allocate
    temp_available = available.copy()
    temp_allocation = [row.copy() for row in allocation]
    temp_need = [row.copy() for row in need]

    for i in range(len(request)):
        temp_available[i] -= request[i]
        temp_allocation[process_id][i] += request[i]
        temp_need[process_id][i] -= request[i]

    # Step 4: Check Safety
    safe, seq = is_safe(len(allocation), temp_available, maximum, temp_allocation, temp_need)

    if safe:
        print("State after allocation is SAFE.")
        print("Safe sequence:", " → ".join(seq))

        # Commit allocation
        for i in range(len(request)):
            available[i] = temp_available[i]
            allocation[process_id][i] = temp_allocation[process_id][i]
            need[process_id][i] = temp_need[process_id][i]

        return True
    else:
        print("State would be UNSAFE. Request DENIED.")
        return False


# -------------------------------------------------------------------------
# Display function
# -------------------------------------------------------------------------
def print_state(available, maximum, allocation, need):
    print("\n--- CURRENT SYSTEM STATE ---")
    print("Available:", available)
    print("\nProcess | Max\t| Alloc\t| Need")
    print("--------------------------------------")
    for i in range(len(allocation)):
        print(f"P{i}\t {maximum[i]}\t {allocation[i]}\t {need[i]}")
    print("--------------------------------------")


# -------------------------------------------------------------------------
# Main Program (Sample values included, input not required)
# -------------------------------------------------------------------------
if __name__ == "__main__":

    # Number of processes & resources
    processes = 5
    resources = 3

    # Example matrices
    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]

    # Available resources
    available = [3, 3, 2]

    # Need = Max - Allocation
    need = [[maximum[i][j] - allocation[i][j] for j in range(resources)]
            for i in range(processes)]

    # Initial state
    print_state(available, maximum, allocation, need)
    safe, seq = is_safe(processes, available, maximum, allocation, need)

    if safe:
        print("\nSystem is in a SAFE state.")
        print("Safe sequence:", " → ".join(seq))
    else:
        print("\nSystem is in an UNSAFE state!")

    # Example: process requests resources
    request = [1, 0, 2]  # P1 requesting
    request_resources(1, request, available, allocation, need, maximum)

    # Print state again
    print_state(available, maximum, allocation, need)
