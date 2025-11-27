# -----------------------------------------------------------
# FIFO Page Replacement Algorithm - Python Implementation
# -----------------------------------------------------------

def fifo_page_replacement(pages, frames):
    memory = []
    page_faults = 0
    pointer = 0   # Points to next frame to replace

    print("FIFO Page Replacement:")

    for p in pages:
        if p not in memory:
            page_faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                memory[pointer] = p
                pointer = (pointer + 1) % frames

        print(f"Page: {p} --> Memory: {memory}")

    print("\nTotal Page Faults (FIFO):", page_faults)
    return page_faults


# ------------------------------
# Example Execution
# ------------------------------
if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
    frames = 3

    fifo_page_replacement(pages, frames)
