from collections import deque

GOAL = ((1, 2, 3), (4, 5, 6), (7, 8, 0))

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    neighbors = []
    i, j = find_blank(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for di, dj in directions:
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = list(list(row) for row in state)
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            neighbors.append(tuple(tuple(row) for row in new_state))
    return neighbors

def is_solvable(state):
    flat = [tile for row in state for tile in row if tile != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i+1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

def dfs_solve(initial_state, max_depth=50):  
    if not is_solvable(initial_state):
        return None, "Unsolvable"
    
    visited = set()
    stack = [(initial_state, [], 0)] 
    visited.add(initial_state)
    
    while stack:
        state, path, depth = stack.pop()
        
        if state == GOAL:
            return path, "Solved"
        
        if depth < max_depth:
            for neighbor in reversed(get_neighbors(state)):
                if neighbor not in visited:
                    visited.add(neighbor)
                    blank_i, blank_j = find_blank(state)
                    new_blank_i, new_blank_j = find_blank(neighbor)
                    if new_blank_i < blank_i:
                        move = 'up'
                    elif new_blank_i > blank_i:
                        move = 'down'
                    elif new_blank_j < blank_j:
                        move = 'left'
                    else:
                        move = 'right'
                    stack.append((neighbor, path + [move], depth + 1))
    
    return None, "No solution found within depth limit"

initial = ((1, 2, 3), (0, 4, 6), (7, 5, 8)) 

path, status = dfs_solve(initial)
print(status)
if path:
    print("Moves:", path)
