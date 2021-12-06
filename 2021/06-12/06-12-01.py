from typing import List


class Lanternfish:
    def __init__(self, initial_timer = 8):
        self.timer = initial_timer
    
    def step(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            return True
        return False
        
def parse_input(filename: str):
    with open(filename, mode="r") as input:
        input = [int(item) for item in input.readline().split(",")]
        return [Lanternfish(item) for item in input]

def step(fish_list: List[Lanternfish]):
    next_list = fish_list.copy()
    for lanternfish in fish_list:
        fish_born = lanternfish.step()
        if fish_born:
            next_list.append(Lanternfish())
    return next_list

def simulate(filename: str):
    fish_list = parse_input(filename)
    for day in range(80):
        fish_list = step(fish_list)
    print(f"Population: {len(fish_list)}")

simulate("input-06")