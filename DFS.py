def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start])]
    
    while stack:
        node, path = stack.pop()
        
        if node == goal:
            return path
        
        if node not in visited:
            visited.add(node)
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    
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

path = dfs(graph, source, goal)

if path:
    print(f"Path found: {' -> '.join(path)}")
else:
    print("No path found")
