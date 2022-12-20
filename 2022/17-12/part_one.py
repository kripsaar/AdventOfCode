from collections import deque

class Rock:
    def __init__(self, shape, left, right, top, bottom) -> None:
        self.shape = shape
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def copy(self, x_offset = 0, y_offset = 0):
        return Rock(self.shape, self.left + x_offset, self.right + x_offset, self.top + y_offset, self.bottom + y_offset)

    def __repr__(self) -> str:
        string = f"pos = ({self.left}, {self.bottom})\n"
        for y in range(self.top - self.bottom, -1, -1):
            line = ""
            for x in range(0, self.right - self.left + 1):
                if (x, y) in self.shape:
                    line += '#'
                else:
                    line += ' '
            line += "\n"
            string += line
        return string

class Cave:
    def __init__(self, jet_pattern: deque, rock_patterns: deque) -> None:
        self.jet_pattern = jet_pattern
        self.rock_patterns = rock_patterns
        self.cave = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)}
        self.max_y = 0
        self.max_x = 6
        self.rock_count = 0

    def __repr__(self) -> str:
        string = ""
        for y in range(self.max_y, -1, -1):
            line = '|'
            for x in range(0, self.max_x + 1):
                if (x, y) in self.cave:
                    line += '#'
                else:
                    line += '.'
            line += '|\n'
            string += line
        return string

    def intersects_position(self, rock: Rock, x_offset = 0, y_offset = 0):
        if rock.bottom + y_offset > self.max_y:
            # Above highest point, no complex intersection possible
            return False
        for part in rock.shape:
            x, y = part
            pos = (x + rock.left + x_offset, y + rock.bottom + y_offset)
            if pos in self.cave:
                return True
        return False

    def stop_the_rock(self, rock: Rock):
        for part in rock.shape:
            x, y = part
            pos = (x + rock.left, y + rock.bottom)
            self.cave.add(pos)
        self.max_y = max(self.max_y, rock.top)
        self.rock_count += 1
        # print(self)

    def move_rock(self, rock: Rock):
        # print(f"Moving rock: {rock}")
        next_jet = self.jet_pattern.popleft()
        self.jet_pattern.append(next_jet)
        if next_jet == '<' and rock.left - 1 >= 0:
            if not self.intersects_position(rock, -1, 0):
                rock.left -= 1
                rock.right -= 1
        elif next_jet == '>' and rock.right + 1 <= self.max_x:
            if not self.intersects_position(rock, +1, 0):
                rock.left += 1
                rock.right += 1
        if not self.intersects_position(rock, 0, -1):
            rock.top -= 1
            rock.bottom -= 1
            return True
        else:
            self.stop_the_rock(rock)
            return False

    def rock_falls(self):
        rock_pattern = self.rock_patterns.popleft()
        rock = rock_pattern.copy(2, self.max_y + 4)
        self.rock_patterns.append(rock_pattern)

        while self.move_rock(rock):
            pass

    def rocks_fall_everybody_dies(self, max_rocks: int):
        while self.rock_count < max_rocks:
            self.rock_falls()


def parse_input(filename: str):
    with open(filename, mode = 'r') as file:
        return deque([*file.read().strip()])

filename = 'input-17'
max_rocks = 2022
jets = parse_input(filename)

rock_shapes = deque()
rock_shapes.append(Rock({(0, 0), (1, 0), (2, 0), (3, 0)}, 0, 3, 0, 0))
rock_shapes.append(Rock({(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}, 0, 2, 2, 0))
rock_shapes.append(Rock({(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}, 0, 2, 2, 0))
rock_shapes.append(Rock({(0, 0), (0, 1), (0, 2), (0, 3)}, 0, 0, 3, 0))
rock_shapes.append(Rock({(0, 0), (1, 0), (0, 1), (1, 1)}, 0, 1, 1, 0))

cave = Cave(jets, rock_shapes)
cave.rocks_fall_everybody_dies(max_rocks)
print(f"Cave height: {cave.max_y}")