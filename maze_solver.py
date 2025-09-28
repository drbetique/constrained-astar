# -*- coding: utf-8 -*-
"""
Constrained A* Pathfinding: "Forward or Turn Right Only"

This implementation is a modified version of the A* pathfinding algorithm 
described in:

    "Easy A* (star) Pathfinding" by Nicholas W. Swift
    https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

Modifications include:
- Tracking direction as part of node state
- Restricting movement to only "forward" or "turn right" actions
- Using 4-directional (non-diagonal) movement
- Printing both path positions and movement directions

Original algorithm logic (f = g + h, open/closed lists, etc.) 
is used with full attribution.
"""

# Direction vectors: Up, Right, Down, Left
direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
start_direction = -1  # Special value for start node (no heading)


class Node():
    """A node class for A* Pathfinding with direction awareness"""

    def __init__(self, parent=None, position=None, direction=None):
        self.parent = parent
        self.position = position
        self.direction = direction  # -1 = start, 0=Up, 1=Right, 2=Down, 3=Left
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction


def astar(maze, start, end):
    """Returns path under 'forward or turn right only' constraint."""
    start_node = Node(None, start, start_direction)
    end_node = Node(None, end)

    open_list = []
    closed_list = []
    open_list.append(start_node)

    while open_list:
        # Find node with lowest f
        current_node = open_list[0]
        current_index = 0
        for i, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = i

        open_list.pop(current_index)
        closed_list.append(current_node)

        # Check if goal reached
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        # Determine allowed directions
        if current_node.direction == start_direction:
            allowed_dirs = [0, 1, 2, 3]  # First move: any direction
        else:
            forward = current_node.direction
            right_turn = (current_node.direction + 1) % 4
            allowed_dirs = [forward, right_turn]

        # Generate children
        children = []
        for d in allowed_dirs:
            dx, dy = direction[d]
            new_pos = (current_node.position[0] + dx, current_node.position[1] + dy)

            # Check bounds
            if not (0 <= new_pos[0] < len(maze) and 0 <= new_pos[1] < len(maze[0])):
                continue
            # Check wall
            if maze[new_pos[0]][new_pos[1]] != 0:
                continue

            children.append(Node(current_node, new_pos, d))

        # Process children
        for child in children:
            # Skip if in closed list
            if any(c == child for c in closed_list):
                continue

            # Calculate costs
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2 +
                       (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Check open list
            skip = False
            for open_node in open_list:
                if child == open_node and child.g >= open_node.g:
                    skip = True
                    break
            if not skip:
                open_list.append(child)

    return None


def main():
    maze1 = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
    ]

    start = (11, 10)
    end = (11, 2)

    path = astar(maze1, start, end)
    # print directions
    if path:
        print("Path found under 'forward or turn right only' constraint:")
        print("Positions:", path)

        # Convert path into directions
        directions = []
        for i in range(1, len(path)):
            dr = path[i][0] - path[i-1][0]
            dc = path[i][1] - path[i-1][1]
            if (dr, dc) == (-1, 0): directions.append("Up")
            elif (dr, dc) == (0, 1): directions.append("Right")
            elif (dr, dc) == (1, 0): directions.append("Down")
            elif (dr, dc) == (0, -1): directions.append("Left")
    print("Directions:", directions)


if __name__ == '__main__':
    main()