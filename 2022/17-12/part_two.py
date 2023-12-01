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
        self.input_patterns = dict()

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

    def rock_falls(self, goal):
        starting_patterns = tuple(self.rock_patterns.copy())
        rock_pattern = self.rock_patterns.popleft()
        rock_start_y = self.max_y + 4
        rock = rock_pattern.copy(2, rock_start_y)
        self.rock_patterns.append(rock_pattern)

        starting_max_y = self.max_y
        jet_pattern = tuple(self.jet_pattern)

        while self.move_rock(rock):
            pass

        move_vector = (rock.left - 2, rock.bottom - rock_start_y)

        y_delta = self.max_y - starting_max_y
        input_pattern = (starting_patterns, jet_pattern, move_vector, y_delta)
        if input_pattern in self.input_patterns and len(self.input_patterns[input_pattern]) > 5:
            pattern_y_delta = self.max_y - self.input_patterns[input_pattern][-1][1]
            pattern_rock_delta = self.rock_count - self.input_patterns[input_pattern][-1][0]
            multiplier = int((goal - self.rock_count) / pattern_rock_delta)
            if multiplier > 0:
                print(f"Found pattern at distance rock = {pattern_rock_delta}, y = {pattern_y_delta}")
                print(f"Pattern: {input_pattern}")
                print(f"Fast forwarding to goal")
                self.rock_count += pattern_rock_delta * multiplier
                print(f"New rock count: {self.rock_count}")
                pre_skip_y = self.max_y 
                self.max_y += pattern_y_delta * multiplier
                print(f"New max y: {self.max_y}")
                # Copy top pattern_rock_delta rows of cave up to max_y
                for y_offset in range(0, pattern_rock_delta * 2 + 1):
                    old_y = pre_skip_y - y_offset
                    new_y = self.max_y - y_offset
                    for x in range(0, self.max_x + 1):
                        if (x, old_y) in self.cave:
                            self.cave.add((x, new_y))

        if input_pattern not in self.input_patterns:
            self.input_patterns[input_pattern] = []
        self.input_patterns[input_pattern].append((self.rock_count, self.max_y))

    def rocks_fall_everybody_dies(self, max_rocks: int):
        while self.rock_count < max_rocks:
            if self.rock_count % 100 == 0:
                print(f"Progress: {self.rock_count}/{max_rocks} ({'{:.3f}'.format(int((self.rock_count/max_rocks) * 100))}%)")
            self.rock_falls(max_rocks)


def parse_input(filename: str):
    with open(filename, mode = 'r') as file:
        return deque([*file.read().strip()])

filename = 'input-17'
# max_rocks = 2022
max_rocks = 1_000_000_000_000
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