# Grid Search with persistent highlighting
# Current matches = yellow, previous matches = green

def load_grid(filename="input.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return lines

def search_all_directions(grid, word):
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]
    matches = set()
    rows, cols = len(grid), max(len(row) for row in grid)

    for r in range(rows):
        for c in range(len(grid[r])):
            for dr, dc in directions:
                rr, cc = r, c
                found = True
                for ch in word:
                    if rr < 0 or rr >= rows or cc < 0 or cc >= len(grid[rr]) or grid[rr][cc] != ch:
                        found = False
                        break
                    rr += dr
                    cc += dc
                if found:
                    # Record all positions of the match
                    rr, cc = r, c
                    for i in range(len(word)):
                        matches.add((rr, cc))
                        rr += dr
                        cc += dc
    return matches

def highlight_grid(grid, current_matches, previous_matches):
    highlighted = []
    for r, row in enumerate(grid):
        line = ""
        for c, ch in enumerate(row):
            if (r, c) in current_matches:
                line += f"\033[93m{ch}\033[0m"  # yellow
            elif (r, c) in previous_matches:
                line += f"\033[92m{ch}\033[0m"  # green
            else:
                line += ch
        highlighted.append(line)
    return highlighted

if __name__ == "__main__":
    grid = load_grid("input.txt")
    previous_matches = set()

    while True:
        word = input("Enter string to search in input.txt (or type 'quit' to exit): ").strip()
        if word.lower() == "quit":
            print("Exiting search session.")
            break

        current_matches = search_all_directions(grid, word)
        print(f"Found {len(current_matches)} matched characters")

        highlighted = highlight_grid(grid, current_matches, previous_matches)
        for line in highlighted:
            print(line)

        previous_matches.update(current_matches)
        print("-" * 60)