# -------------------------------------------------------------------
# Page Replacement Algorithms in Python
# FIFO, LRU, Optimal
# Compare page faults
# -------------------------------------------------------------------

def fifo(pages, frames):
    memory = []
    page_faults = 0
    pointer = 0  # Points to next frame to replace

    for p in pages:
        if p not in memory:
            page_faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                memory[pointer] = p
                pointer = (pointer + 1) % frames

        # Debug printing (optional)
        print(f"Page: {p} -> Memory: {memory}")

    return page_faults


def lru(pages, frames):
    memory = []
    page_faults = 0

    last_used = {}  # Track usage time

    for time, p in enumerate(pages):
        if p not in memory:
            page_faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                # Find least recently used page
                lru_page = min(last_used, key=last_used.get)
                memory[memory.index(lru_page)] = p
                del last_used[lru_page]

        last_used[p] = time

        print(f"Page: {p} -> Memory: {memory}")

    return page_faults


def optimal(pages, frames):
    memory = []
    page_faults = 0

    for i, p in enumerate(pages):
        if p not in memory:
            page_faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                # Find page with farthest next use
                future_use = {}

                for m in memory:
                    if m in pages[i+1:]:
                        future_use[m] = pages[i+1:].index(m)
                    else:
                        future_use[m] = float('inf')

                page_to_replace = max(future_use, key=future_use.get)
                memory[memory.index(page_to_replace)] = p

        print(f"Page: {p} -> Memory: {memory}")

    return page_faults


# -------------------------------------------------------------------
# Compare algorithms
# -------------------------------------------------------------------
def compare_algorithms(pages, frames):
    print("\n--- FIFO ---")
    fifo_faults = fifo(pages, frames)

    print("\n--- LRU ---")
    lru_faults = lru(pages, frames)

    print("\n--- OPTIMAL ---")
    opt_faults = optimal(pages, frames)

    print("\n==================== RESULTS ====================")
    print(f"Total Page Faults (FIFO):    {fifo_faults}")
    print(f"Total Page Faults (LRU):     {lru_faults}")
    print(f"Total Page Faults (Optimal): {opt_faults}")
    print("=================================================")


# -------------------------------------------------------------------
# Main Program (Sample run)
# -------------------------------------------------------------------
if __name__ == "__main__":
    # Example input (you can modify)
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
    frames = 3

    print("Pages:", pages)
    print("Frames:", frames)
    compare_algorithms(pages, frames)
