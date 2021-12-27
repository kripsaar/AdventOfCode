region = []
east = []
south = []

def parse_input(filename: str):
    global region
    global east
    global south
    with open(filename, mode="r") as input:
        region = []
        east = []
        south = []
        lines = input.readlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line.strip()):
                if len(region) < x + 1:
                    region.append([])
                region[x].append(char)
                if char == ">":
                    east.append((x,y))
                elif char == "v":
                    south.append((x,y))
        return region, east, south
        
def print_region(region: list):
    x_len = len(region)
    y_len = len(region[0])
    string = ""
    for y in range(y_len):
        line = ""
        for x in range(x_len):
            line += region[x][y]
        string += line + "\n"
    string = string.strip()
    print(string)

def copy_region(region: list):
    new_region = []
    for line in region:
        new_region.append(line.copy())
    return new_region

def step():
    global region
    global east
    global south
    x_len = len(region)
    y_len = len(region[0])
    new_region = copy_region(region)
    new_east = []
    new_south = []
    moved_count = 0
    for x, y in east:
        new_x = (x + 1) % x_len
        if region[new_x][y] == ".":
            moved_count += 1
            new_region[x][y] = "."
            new_region[new_x][y] = ">"
            new_east.append((new_x, y))
        else:
            new_east.append((x, y))
    region = copy_region(new_region)
    for x, y in south:
        new_y = (y + 1) % y_len
        if region[x][new_y] == ".":
            moved_count += 1
            new_region[x][y] = "."
            new_region[x][new_y] = "v"
            new_south.append((x, new_y))
        else:
            new_south.append((x, y))
    region = new_region
    east = new_east
    south = new_south
    return moved_count


parse_input("input-25")
moved_count = 1
step_count = 0
while(moved_count > 0):
    step_count += 1
    moved_count = step()
print()
print(f"After {step_count} steps:")
print_region(region)