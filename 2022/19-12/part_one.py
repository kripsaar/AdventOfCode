from __future__ import annotations
import time

class ResourceBundle:
    def __init__(self, ore = 0, clay = 0, obsidian = 0, geodes = 0) -> None:
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geodes = geodes

    def __repr__(self) -> str:
        return f"ore: {self.ore}, clay: {self.clay}, obsidian: {self.obsidian}, geodes: {self.geodes}"

    def copy(self):
        return ResourceBundle(self.ore, self.clay, self.obsidian, self.geodes)

    def __add__(self, other):
        return ResourceBundle(self.ore + other.ore, self.clay + other.clay, self.obsidian + other.obsidian, self.geodes + other.geodes)

    def __iadd__(self, other):
        self.ore += other.ore
        self.clay += other.clay
        self.obsidian += other.obsidian
        self.geodes += other.geodes
        return self

    def __mul__(self, other):
        if isinstance(other, ResourceBundle):
            return ResourceBundle(self.ore * other.ore, self.clay * other.clay, self.obsidian * other.obsidian, self.geodes * other.geodes)
        elif isinstance(other, int):
            return ResourceBundle(self.ore * other, self.clay * other, self.obsidian * other, self.geodes * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def can_afford(self, other):
        return self.ore >= other.ore and self.clay >= other.clay and self.obsidian >= other.obsidian

    def __sub__(self, other):
        return ResourceBundle(self.ore - other.ore, self.clay - other.clay, self.obsidian - other.obsidian, self.geodes - other.geodes)

    def __isub__(self, other):
        self.ore -= other.ore
        self.clay -= other.clay
        self.obsidian -= other.obsidian
        self.geodes -= other.geodes
        return self

    def parse(self, string: str):
        resources = string.split(' and ')
        for resource in resources:
            amount = int(resource[:resource.find(' ')])
            if "ore" in resource:
                self.ore = amount
            elif "clay" in resource:
                self.clay = amount
            elif "obsidian" in resource:
                self.obsidian = amount

class Blueprint:
    def __init__(self, id: int, ore_robot_cost: ResourceBundle, clay_robot_cost: ResourceBundle, obsidian_robot_cost: ResourceBundle, geode_robot_cost: ResourceBundle) -> None:
        self.id = id
        self.ore_robot_cost = ore_robot_cost
        self.clay_robot_cost = clay_robot_cost
        self.obsidian_robot_cost = obsidian_robot_cost
        self.geode_robot_cost = geode_robot_cost

    def __repr__(self) -> str:
        return f"""
Blueprint {self.id}:
Ore: {self.ore_robot_cost}
Clay: {self.clay_robot_cost}
Obsidian: {self.obsidian_robot_cost}
Geode: {self.geode_robot_cost}"""

class GeodeFactory:
    def __init__(self, blueprint: Blueprint, remaining_minutes: int, resources: ResourceBundle, robots: ResourceBundle, skip: ResourceBundle = None) -> None:
        self.blueprint = blueprint
        self.remaining_minutes = remaining_minutes
        self.resources = resources
        self.robots = robots
        self.skip = ResourceBundle(0, 0, 0, 0)
        if skip is not None:
            self.skip = skip

    def __repr__(self) -> str:
        return f"Geode Factory:\nRemaining minutes: {self.remaining_minutes}{self.blueprint.__repr__()}\nResources: {self.resources}\nRobots: {self.robots}" 
        
    def copy(self):
        return GeodeFactory(self.blueprint, self.remaining_minutes, self.resources.copy(), self.robots.copy(), self.skip.copy())

    def get_score(self) -> int:
        return self.blueprint.id * self.resources.geodes

    def can_afford(self, cost: ResourceBundle) -> bool:
        return self.resources.can_afford(cost)

    def generate_resources(self):
        self.resources += self.robots
        self.remaining_minutes -= 1

    def need_ore_robot(self):
        max_ore_cost = max(self.blueprint.ore_robot_cost.ore, self.blueprint.clay_robot_cost.ore, self.blueprint.obsidian_robot_cost.ore, self.blueprint.geode_robot_cost.ore)
        if (self.remaining_minutes * self.robots.ore) + self.resources.ore >= self.remaining_minutes * max_ore_cost:
            return False
        return True

    def need_clay_robot(self):
        max_clay_cost = max(self.blueprint.ore_robot_cost.clay, self.blueprint.clay_robot_cost.clay, self.blueprint.obsidian_robot_cost.clay, self.blueprint.geode_robot_cost.clay)
        if (self.remaining_minutes * self.robots.clay) + self.resources.clay >= self.remaining_minutes * max_clay_cost:
            return False
        return True

    def need_obsidian_robot(self):
        max_obsidian_cost = max(self.blueprint.ore_robot_cost.obsidian, self.blueprint.clay_robot_cost.obsidian, self.blueprint.obsidian_robot_cost.obsidian, self.blueprint.geode_robot_cost.obsidian)
        if (self.remaining_minutes * self.robots.obsidian) + self.resources.obsidian >= self.remaining_minutes * max_obsidian_cost:
            return False
        return True

    def generate_possible_actions(self) -> list[GeodeFactory]:
        candidates = []

        if self.resources.can_afford(self.blueprint.ore_robot_cost) and self.need_ore_robot() and self.skip.ore < 1:
            buy_ore_robot = self.copy()
            buy_ore_robot.skip = ResourceBundle(0, 0, 0, 0)
            buy_ore_robot.generate_resources()
            buy_ore_robot.resources -= self.blueprint.ore_robot_cost
            buy_ore_robot.robots.ore += 1
            candidates.append(buy_ore_robot)
            self.skip.ore += 1

        if self.resources.can_afford(self.blueprint.clay_robot_cost) and self.need_clay_robot() and self.skip.clay < 1:
            buy_clay_robot = self.copy()
            buy_clay_robot.skip = ResourceBundle(0, 0, 0, 0)
            buy_clay_robot.generate_resources()
            buy_clay_robot.resources -= self.blueprint.clay_robot_cost
            buy_clay_robot.robots.clay += 1
            candidates.append(buy_clay_robot)
            self.skip.clay += 1

        if self.resources.can_afford(self.blueprint.obsidian_robot_cost) and self.need_obsidian_robot() and self.skip.obsidian < 1:
            buy_obsidian_robot = self.copy()
            buy_obsidian_robot.skip = ResourceBundle(0, 0, 0, 0)
            buy_obsidian_robot.generate_resources()
            buy_obsidian_robot.resources -= self.blueprint.obsidian_robot_cost
            buy_obsidian_robot.robots.obsidian += 1
            candidates.append(buy_obsidian_robot)
            self.skip.obsidian += 1

        if self.resources.can_afford(self.blueprint.geode_robot_cost) and self.skip.geodes < 1:
            buy_geode_robot = self.copy()
            buy_geode_robot.skip = ResourceBundle(0, 0, 0, 0)
            buy_geode_robot.generate_resources()
            buy_geode_robot.resources -= self.blueprint.geode_robot_cost
            buy_geode_robot.robots.geodes += 1
            candidates.append(buy_geode_robot)
            self.skip.geodes += 1

        do_nothing = self.copy()
        do_nothing.generate_resources()
        candidates.append(do_nothing)

        return candidates

    def run(self):
        if self.remaining_minutes <= 0:
            return self.get_score()

        candidates = self.generate_possible_actions()
        max_score = 0
        for candidate in candidates:
            max_score = max(max_score, candidate.run())

        return max_score
        

def parse_robot_cost(line: str, robot_cost_part: str):
    start = line.find(robot_cost_part)
    end = start + line[start:].find('.')
    cost_sheet = ResourceBundle()
    cost_sheet.parse(line[start + len(robot_cost_part):end])
    return cost_sheet


def parse_input(filename: str):
    blueprints = []
    with open(filename, mode = 'r') as file:
        for line in file.readlines():
            line = line.strip()
            id = int(line[len("Blueprint "):line.find(':')])
            ore_cost = parse_robot_cost(line, "Each ore robot costs ")
            clay_cost = parse_robot_cost(line, "Each clay robot costs ")
            obsidian_cost = parse_robot_cost(line, "Each obsidian robot costs ")
            geode_cost = parse_robot_cost(line, "Each geode robot costs ")
            blueprints.append(Blueprint(id, ore_cost, clay_cost, obsidian_cost, geode_cost))
    return blueprints

filename = 'input-19'
blueprints = parse_input(filename)


scores = []
start = time.time()
for blueprint in blueprints:
    factory = GeodeFactory(blueprint, 24, ResourceBundle(0, 0, 0, 0), ResourceBundle(1, 0, 0, 0))
    score = factory.run()
    scores.append(score)

print(sum(scores))
end = time.time()
print(f"Runtime: {int(((end - start) * 1000))}ms")