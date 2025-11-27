# -----------------------------------------------------------
# OPTIMAL Page Replacement Algorithm - Python Implementation
# -----------------------------------------------------------

def optimal_page_replacement(pages, frames):
    memory = []
    page_faults = 0

    print("Optimal Page Replacement:")

    for i, p in enumerate(pages):
        if p not in memory:
            page_faults += 1

            if len(memory) < frames:
                memory.append(p)
            else:
                # Find farthest future use
                future_index = {}

                for m in memory:
                    if m in pages[i+1:]:
                        future_index[m] = pages[i+1:].index(m)
                    else:
                        future_index[m] = float('inf')

                # Replace the page used farthest in future
                page_to_replace = max(future_index, key=future_index.get)
                memory[memory.index(page_to_replace)] = p

        print(f"Page: {p} --> Memory: {memory}")

    print("\nTotal Page Faults (Optimal):", page_faults)
    return page_faults


# ------------------------------
# Example Execution
# ------------------------------
if __name__ == "__main__":
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3]
    frames = 3

    optimal_page_replacement(pages, frames)
