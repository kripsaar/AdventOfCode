import math
import itertools

class Pair:
    def __init__(self, content: list = None, depth: int = 0, parent: object = None) -> None:
        self.content = content
        self.depth = depth
        self.parent = parent

    def __repr__(self) -> str:
        string = "["
        string += ",".join(str(item) for item in self.content)
        string += "]"
        return string

    def __str__(self) -> str:
        string = "["
        string += ",".join(str(item) for item in self.content)
        string += "]"
        return string

    def increment_depth(self):
        self.depth += 1
        for child in self.content:
            if isinstance(child, int):
                continue
            else:
                child.increment_depth()

    def find_root(self):
        if self.parent is None:
            return self
        return self.parent.find_root()

    def add(self, other: object):
        depth = self.depth
        parent = self.parent
        self.increment_depth()
        other.increment_depth()
        content = [self, other]
        pair = Pair(content, depth, parent)
        self.parent = pair
        other.parent = pair
        root = pair.find_root()
        needs_reduction = True
        while needs_reduction:
            needs_reduction = root.reduce()
        return pair

    def find_explosion(self):
        if self.depth >= 4:
            return self
        left, right = self.content
        if not isinstance(left, int):
            left_res = left.find_explosion()
            if left_res is not None:
                return left_res
        if not isinstance(right, int):
            return right.find_explosion()
        return None

    def reduce(self) -> bool:
        # First find any potential explosions
        explosion_candidate = self.find_explosion()
        if explosion_candidate is not None:
            explosion_candidate.explode()
            return True

        # Only then try to find any splits
        return self.split()

    def set_left_neighbor(self, value: int):
        parent = self.parent
        if parent is None:
            return
        left, right = parent.content
        if left == self:
            parent.set_left_neighbor(value)
        if right == self:
            if isinstance(left, int):
                parent.content[0] += value
                return
            target = left
            while not isinstance(target.content[1], int):
                target = target.content[1]
            target.content[1] += value
            return

    def set_right_neighbor(self, value: int):
        parent = self.parent
        if parent is None:
            return
        left, right = parent.content
        if right == self:
            parent.set_right_neighbor(value)
        if left == self:
            if isinstance(right, int):
                parent.content[1] += value
                return
            target = right
            while not isinstance(target.content[0], int):
                target = target.content[0]
            target.content[0] += value
            return

    def explode(self):
        left, right = self.content
        self.set_left_neighbor(left)
        self.set_right_neighbor(right)
        parent = self.parent
        if parent.content[0] == self:
            parent.content[0] = 0
        elif parent.content[1] == self:
            parent.content[1] = 0

    def split(self):
        left, right = self.content
        if isinstance(left, int) and left >= 10:
            self.content[0] = self.split_value(left)
            return True
        if not isinstance(left, int) and left.split():
            return True
        if isinstance(right, int) and right >= 10:
            self.content[1] = self.split_value(right)
            return True
        if not isinstance(right, int) and right.split():
            return True
        
        return False

    def split_value(self, value: int):
        left = math.floor(value / 2)
        right = math.ceil(value / 2)
        return Pair([left, right], self.depth + 1, self)

    def calc_magnitude(self):
        magnitude = 0
        left, right = self.content
        left_value = 0
        right_value = 0
        if isinstance(left, int):
            left_value = left
        else:
            left_value = left.calc_magnitude()
        if isinstance(right, int):
            right_value = right
        else:
            right_value = right.calc_magnitude()
        magnitude = 3 * left_value + 2 * right_value
        return magnitude

def find_matching_closing_bracket(string: str, opening_index: int) -> int:
    open = 1
    index = opening_index
    while open > 0:
        index += 1
        if string[index] == "[":
            open += 1
        elif string[index] == "]":
            open -= 1
    return index

def parse_pair_string(pair_string: str, depth: int = 0) -> Pair:
    pair_string = pair_string[1:-1]
    left = None
    if pair_string[0].isnumeric():
        left = int(pair_string[0])
        pair_string = pair_string[2:]
    else:
        close = find_matching_closing_bracket(pair_string, 0)
        left = parse_pair_string(pair_string[0:close + 1], depth + 1)
        pair_string = pair_string[close + 2:]
    right = None
    if pair_string[0].isnumeric():
        right = int(pair_string[0])
    else:
        close = find_matching_closing_bracket(pair_string, 0)
        right = parse_pair_string(pair_string[0:close + 1], depth + 1)
    pair = Pair([left, right], depth)
    if not isinstance(left, int):
        left.parent = pair
    if not isinstance(right, int):
        right.parent = pair
    return pair

def parse_input(filename: str):
    with open(filename, mode="r") as input:
        pairs = []
        for line in input:
            line = line.strip()
            pairs.append(parse_pair_string(line, 0))
        return pairs

def parse_input_as_strings(filename: str):
    with open(filename, mode="r") as input:
        pairs = []
        for line in input:
            pairs.append(line.strip())
        return pairs

pairs = parse_input_as_strings("input-18")

permutations = list(itertools.permutations(pairs, 2))

result = None
magnitude = 0
pairs_count = 0
for pair in permutations:
    left = parse_pair_string(pair[0])
    right = parse_pair_string(pair[1])
    pair_sum = left.add(right)
    pair_magnitude = pair_sum.calc_magnitude()
    pairs_count += 1
    if pair_magnitude > magnitude:
        magnitude = pair_magnitude
        result = pair_sum
        print(f"New best magnitude: {magnitude}")
        print(f"New best snailfish: {result}")

print(f"Best snailfish: {result}")
print(f"Best magnitude: {magnitude}")

# [8,0] + [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
# pairs = [parse_pair_string("[8,0]"), parse_pair_string("[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]")]

# current = pairs[0]
# rest = pairs[1:]
# for pair in rest:
#     current = current.add(pair)

# print(f"Final pair: {current}")
# print(f"Magnitude: {current.calc_magnitude()}")

# [8,0] + [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]