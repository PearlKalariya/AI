from collections import deque

def bfs(graph, start, goal):
    visited = set([start])
    queue = deque([(start, [start])])
    
    while queue:
        node, path = queue.popleft()
        
        if node == goal:
            return path
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

source = input("Enter source node: ").strip()
goal = input("Enter goal node: ").strip()

path = bfs(graph, source, goal)

if path:
    print(f"Path found: {' -> '.join(path)}")
else:
    print("No path found")
