from __future__ import annotations

import sys
import collections
from typing import List

# Константы для символов ключей и дверей
keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]

class Point:
    def __init__(self, x: int, y: int, char: str, prev_point: Point = None, is_start_point: bool = False):
        self.cord_x = x
        self.cord_y = y
        self.char = char
        self.is_start_point = is_start_point
        self.prev_point = prev_point

    @property
    def current_steps(self) -> int:
        steps = 0
        current = self
        while current.prev_point is not None and (not current.is_start_point or current == self):
            steps += 1
            current = current.prev_point
        return steps

    def __hash__(self):
        return hash((self.cord_x, self.cord_y))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point): return False
        return self.cord_x == other.cord_x and self.cord_y == other.cord_y

    def __str__(self):
        return f"{self.cord_x}_{self.cord_y}, '{self.char}'"

    def __repr__(self):
        return f"{self.cord_x}-{self.cord_y}-'{self.char}'"


def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]
#     #TODO remove
#     input = """###############
# #..AB..#.....a#
# #C####@#@######
# #d.E...########
# ######@#@######
# #b.....#.....c#
# ###############
# """
#     return [list(line.strip()) for line in input.splitlines()]

def min_steps_to_collect_all_keys(grid: List[List[str]]) -> int:
    all_available_chars_to_move = keys_char + doors_char + ['.', '@']
    all_keys = set()
    collected_keys = set()
    points_with_keys = set()
    visited_points = {}
    queue = collections.deque()
    for step_y, arr in enumerate(grid):
        for step_x, char in enumerate(arr):
            if char in keys_char:
                all_keys.add(char)
            elif char == '@':
                point = Point(step_x, step_y, char=char, is_start_point=True)
                queue.append(point)
                visited_points[(step_x, step_y)] = point

    while queue or collected_keys != all_keys:
        current_point = queue.popleft()
        if current_point.char in doors_char and current_point.char.lower() not in collected_keys:
            # TODO возможно бесконечный цикл
            queue.append(current_point)
            continue

        height = len(grid)
        width = len(grid[0])
        for step_x, step_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_point_x = current_point.cord_x + step_x
            new_point_y = current_point.cord_y + step_y
            if new_point_x >= width or new_point_y >= height: continue

            new_point_char = grid[current_point.cord_y + step_y][current_point.cord_x + step_x]

            match new_point_char:
                case '#':
                    continue
                case char if char in all_available_chars_to_move:
                    is_point_with_key = new_point_char in all_keys

                    new_point = visited_points.get((new_point_x, new_point_y))
                    if new_point is None:
                        # предусмотреть что на карте может быть несколько одинаковых ключей
                        new_point = Point(new_point_x, new_point_y, char=new_point_char, prev_point=current_point,
                                          is_start_point=is_point_with_key)
                        visited_points[(new_point_x, new_point_y)] = new_point
                        queue.append(new_point)
                    elif (current_point.prev_point != new_point and
                          current_point.current_steps + 1 < new_point.current_steps):
                        new_point.prev_point = current_point

                    if is_point_with_key:
                        collected_keys.add(char)
                        points_with_keys.add(new_point)

                case _:
                    raise Exception(f'Unknown character {new_point_char}')

    return sum(point.current_steps for point in points_with_keys)

def main():
    data = get_input()
    result = min_steps_to_collect_all_keys(data)
    print(result)


if __name__ == '__main__':
    main()
