#!/usr/bin/env python3
"""
A* solver for the 8-puzzle.

Usage:
  python3 8_puzzle_astar.py            # runs a default example
  python3 8_puzzle_astar.py manhattan 1 2 3 4 5 6 7 8 0

Heuristics: 'manhattan' (default) or 'misplaced'
"""
import heapq
import sys
import time
from typing import List, Tuple, Optional


Goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def misplaced_tiles(state: Tuple[int, ...]) -> int:
    return sum(1 for i, v in enumerate(state) if v != 0 and v != Goal[i])


def manhattan_distance(state: Tuple[int, ...]) -> int:
    dist = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        goal_idx = val - 1
        cur_r, cur_c = divmod(idx, 3)
        goal_r, goal_c = divmod(goal_idx, 3)
        dist += abs(cur_r - goal_r) + abs(cur_c - goal_c)
    return dist


class Node:
    __slots__ = ("state", "parent", "g", "h")

    def __init__(self, state: Tuple[int, ...], parent: Optional["Node"], g: int, h: int):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h

    def f(self) -> int:
        return self.g + self.h


def neighbors(state: Tuple[int, ...]) -> List[Tuple[int, ...]]:
    zero = state.index(0)
    r, c = divmod(zero, 3)
    results = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nidx = nr * 3 + nc
            new_state = list(state)
            new_state[zero], new_state[nidx] = new_state[nidx], new_state[zero]
            results.append(tuple(new_state))
    return results


def reconstruct_path(node: Node) -> List[Tuple[int, ...]]:
    path = []
    cur = node
    while cur:
        path.append(cur.state)
        cur = cur.parent
    return list(reversed(path))


def astar(start: Tuple[int, ...], heuristic: str = "manhattan", max_expansions: int = 200000) -> Tuple[Optional[List[Tuple[int, ...]]], dict]:
    if heuristic == "manhattan":
        h_fn = manhattan_distance
    elif heuristic == "misplaced":
        h_fn = misplaced_tiles
    else:
        raise ValueError("Unknown heuristic: " + heuristic)

    start_h = h_fn(start)
    start_node = Node(start, None, 0, start_h)

    open_heap = []
    counter = 0
    heapq.heappush(open_heap, (start_node.f(), start_node.h, counter, start_node))
    counter += 1
    open_count = 1
    closed = {}
    expansions = 0
    max_frontier = 1

    while open_heap:
        _, _, _, current = heapq.heappop(open_heap)
        if current.state in closed:
            continue
        closed[current.state] = current.g

        if current.state == Goal:
            info = {"expansions": expansions, "max_frontier": max_frontier, "open_count": open_count}
            return reconstruct_path(current), info

        expansions += 1
        if expansions > max_expansions:
            break

        for nb in neighbors(current.state):
            if nb in closed:
                continue
            g = current.g + 1
            h = h_fn(nb)
            node = Node(nb, current, g, h)
            heapq.heappush(open_heap, (node.f(), node.h, counter, node))
            counter += 1

        max_frontier = max(max_frontier, len(open_heap))

    return None, {"expansions": expansions, "max_frontier": max_frontier, "open_count": open_count}


def pretty_print(state: Tuple[int, ...]) -> None:
    for i in range(0, 9, 3):
        print(" ".join(str(x) if x != 0 else "_" for x in state[i : i + 3]))
    print()


def parse_args(argv: List[str]) -> Tuple[str, Tuple[int, ...]]:
    if not argv:
        return "manhattan", (1, 2, 3, 4, 0, 6, 7, 5, 8)
    heur = argv[0]
    if heur not in ("manhattan", "misplaced"):
        # treat all args as puzzle
        vals = [int(x) for x in argv]
        if len(vals) != 9:
            raise SystemExit("Provide 9 integers for the puzzle")
        return "manhattan", tuple(vals)
    if len(argv) == 1:
        return heur, (1, 2, 3, 4, 0, 6, 7, 5, 8)
    vals = [int(x) for x in argv[1:]]
    if len(vals) != 9:
        raise SystemExit("Provide 9 integers for the puzzle")
    return heur, tuple(vals)


if __name__ == "__main__":
    heur, start = parse_args(sys.argv[1:])
    print("Start state:")
    pretty_print(start)
    print("Heuristic:", heur)
    t0 = time.time()
    path, info = astar(start, heuristic=heur)
    t1 = time.time()
    if path is None:
        print("No solution found (expansions={})".format(info.get("expansions")))
        sys.exit(1)

    print("Solved in {} moves".format(len(path) - 1))
    print("Time: {:.3f}s".format(t1 - t0))
    print("Expansions:", info.get("expansions"))
    print("Max frontier size:", info.get("max_frontier"))
    print()
    for step, s in enumerate(path):
        print(f"Step {step}:")
        pretty_print(s)
