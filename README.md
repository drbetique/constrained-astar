# Constrained A* Pathfinding

This project solves a maze with the movement constraint:  
**"Only move forward or turn right (relative to current heading)."**

It is a **modified version** of the A* pathfinding algorithm from:

> **"Easy A* Pathfinding" by Nicholas W. Swift**  
> https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2

## Modifications
- Added directional state (`Up`, `Right`, `Down`, `Left`) to each node.
- Restricted movement to **forward or right turn only**.
- Used 4-directional (non-diagonal) movement.
- Prints both path positions and movement directions.

## How to Run
```bash
python maze_solver.py

## 🖨️ Sample Output

Path found under 'forward or turn right only' constraint:
Positions: [(11, 10), (10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10), (4, 10), (3, 10), (2, 10), (2, 11), (2, 12), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (10, 11), (10, 10), (10, 9), (10, 8), (10, 7), (10, 6), (10, 5), (10, 4), (10, 3), (10, 2), (9, 2), (8, 2), (7, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (8, 9), (8, 8), (8, 7), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (4, 7), (4, 8), (5, 8), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2)]
Directions: ['Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down', 'Down']
