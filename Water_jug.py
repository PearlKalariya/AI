from collections import deque

def water_jug(m, n, d):
    visited = set()
    queue = deque([((0, 0), [])])
    
    while queue:
        (a, b), path = queue.popleft()
        
        if a == d or b == d:
            return path + [(a, b)]
        
        if (a, b) in visited:
            continue
        
        visited.add((a, b))
        
        moves = [
            (m, b),
            (a, n),
            (0, b),
            (a, 0),
            (max(0, a - (n - b)), min(n, b + a)),
            (min(m, a + b), max(0, b - (m - a)))
        ]
        
        for move in moves:
            if move not in visited:
                queue.append((move, path + [(a, b)]))
    
    return None

m = int(input("Enter jug 1 capacity (m): "))
n = int(input("Enter jug 2 capacity (n): "))
d = int(input("Enter target volume (d): "))

result = water_jug(m, n, d)

if result:
    print("\nSolution:")
    for i, (a, b) in enumerate(result):
        print(f"Step {i}: Jug1 = {a}L, Jug2 = {b}L")
else:
    print("No solution found")
