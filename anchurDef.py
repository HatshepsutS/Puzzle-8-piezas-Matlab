import time
from collections import deque
from anytree import Node, RenderTree

initial_state = [[2, 8, 3], [1, 6, 4], [7, None, 5]]
goal_state = [[1, 2, 3], [8, None, 4], [7, 6, 5]]


def find_empty(state):
    for row in range(3):
        for col in range(3):
            if state[row][col] is None:
                return row, col


def successors(state):
    successors = []
    row, col = find_empty(state)
    for drow, dcol, action in [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]:
        new_row, new_col = row + drow, col + dcol
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [row[:] for row in state]
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            successors.append((new_state, action))
    return successors


def bfs(initial_state, goal_state):
    start_time = time.perf_counter()
    root = Node(str(initial_state))
    queue = deque([(initial_state, [], 0, root)])
    visited = set()
    while queue:
        state, path, depth, parent_node = queue.popleft()
        visited.add(tuple(map(tuple, state)))
        if state == goal_state:
            with open("solution.txt", "w", encoding="utf8") as f:
                f.write("Solución encontrada en %d pasos:\n" % len(path))
                for action in path:
                    f.write(action + '\n')
            with open("tree.txt", "w", encoding="utf8") as f:
                for pre, fill, node in RenderTree(root):
                    if node.name == str(goal_state):
                        f.write("%s%s <-- Solución encontrada\n" % (pre, node.name))
                    else:
                        f.write("%s%s\n" % (pre, node.name))
                f.write("Tiempo de ejecución: %.6f segundos" % ((time.perf_counter() - start_time) ))
            return path, root
        for child_state, action in successors(state):
            if tuple(map(tuple, child_state)) not in visited:
                child_node = Node(str(child_state), parent=parent_node)
                queue.append((child_state, path + [action], depth+1, child_node))
    print("No se encontró solución")
    return None, root

path, root = bfs(initial_state, goal_state)
