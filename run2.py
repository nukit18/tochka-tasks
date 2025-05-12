from __future__ import annotations

import sys
import collections
from typing import List, Set, Tuple

# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


class State:
    def __init__(self, robot_positions: List[Tuple[int, int]], keys: Set[str]):
        self.robot_positions = robot_positions
        self.keys = keys

    def __str__(self):
        return f"RPos: {self.robot_positions}, Keys: {self.keys}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((*self.robot_positions, *self.keys))

    def __eq__(self, other):
        return (self.robot_positions == other.robot_positions and
                self.keys == other.keys)


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]


def min_steps_to_collect_all_keys(grid: List[List[str]]) -> int:
    robots = []
    all_keys = set()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == '@':
                robots.append((x, y))
            elif grid[y][x] in keys_char:
                all_keys.add(grid[y][x])

    if not all_keys:
        return 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited_states = set()
    queue = collections.deque()

    initial_state = State(robots, set())
    queue.append((initial_state, 0))
    visited_states.add(initial_state)

    while queue:
        current_state, steps = queue.popleft()

        if len(current_state.keys) == len(all_keys):
            return steps

        for robot_idx, (x, y) in enumerate(current_state.robot_positions):
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                    cell = grid[ny][nx]

                    if cell == '#': continue
                    if cell in doors_char and cell.lower() not in current_state.keys: continue

                    new_keys = set(current_state.keys)
                    if cell in keys_char:
                        new_keys.add(cell)

                    new_positions = list(current_state.robot_positions)
                    new_positions[robot_idx] = (nx, ny)

                    new_state = State(new_positions, set(new_keys))

                    if new_state not in visited_states:
                        visited_states.add(new_state)
                        queue.append((new_state, steps + 1))

    return -1


def main():
    data = get_input()
    result = min_steps_to_collect_all_keys(data)
    print(result)


if __name__ == '__main__':
    main()