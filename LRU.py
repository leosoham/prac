# -----------------------------------------------------------
# LRU Page Replacement Algorithm - Python Implementation
# -----------------------------------------------------------

def lru_page_replacement(pages, frames):
    memory = []
    page_faults = 0
    last_used = {}   # Track last used times for each page

    print("LRU Page Replacement:")

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
        print(f"Page: {p} --> Memory: {memory}")

    print("\nTotal Page Faults (LRU):", page_faults)
    return page_faults


# ------------------------------
# Example Execution
# ------------------------------
if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
    frames = 3

    lru_page_replacement(pages, frames)
