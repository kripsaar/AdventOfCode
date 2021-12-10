import math

def moveUp(currPos):
    return (currPos[0], currPos[1] + 1)

def moveDown(currPos):
    return (currPos[0], currPos[1] - 1)

def moveLeft(currPos):
    return (currPos[0] - 1, currPos[1])

def moveRight(currPos):
    return (currPos[0] + 1, currPos[1])

intersections = []
positionDistances = {}

def addPathToGrid(grid, pathInput, gridId):
    global intersections
    global positionDistances
    positionDistances[gridId] = {}
    currPos = (0,0)
    distanceTraveled = 0
    distances = {}
    for move in pathInput:
        direction = move[0]
        distance = int(move[1:])
        action = moveUp
        if direction == 'U':
            action = moveUp
        elif direction == 'D':
            action = moveDown
        elif direction == 'L':
            action = moveLeft
        elif direction == 'R':
            action = moveRight

        while distance > 0:
            currPos = action(currPos)
            distanceTraveled += 1
            x = currPos[0]
            y = currPos[1]
            if x not in grid.keys():
                grid[x] = {}
            if y not in grid[x].keys():
                grid[x][y] = gridId
            elif grid[x][y] != gridId:
                intersections.append(currPos)
                grid[x][y] = "X"
            # else:
            #     distanceTraveled = positionDistances[gridId][currPos]
            if currPos not in positionDistances[gridId].keys():
                positionDistances[gridId][currPos] = distanceTraveled
            distance -= 1
    return grid

def drawGrid(grid):
    maxX = max(grid.keys()) + 1
    minX = min(grid.keys()) - 1
    maxY = max([max(i.keys()) for i in grid.values()]) + 1
    minY = min([min(i.keys()) for i in grid.values()]) - 1
    currY = maxY
    res = ""
    while currY >= minY:
        currX = minX
        while currX <= maxX:
            if currX not in grid.keys() or currY not in grid[currX].keys():
                res = res + "."
                currX += 1
                continue
            res = res + grid[currX][currY]
            currX += 1
        res = res + "\n"
        currY -= 1
    print(res)

def calculateIntersections(inputs):
    grid = { 0 : { 0 : "O"} }
    pathId = 1
    for path in inputs:
        grid = addPathToGrid(grid, path, str(pathId))
        pathId += 1
    # drawGrid(grid)
    

def distanceToClosestIntersection(intersections):
    minDistance = math.inf
    for intersection in intersections:
        distance = abs(intersection[0]) + abs(intersection[1])
        minDistance = min(minDistance, distance)
    return minDistance

def calcNearestIntersection():
    # print(positionDistances)
    intersectionDistances = [ sum([ distances[intersection] for distances in positionDistances.values()]) for intersection in intersections ]
    print(min(intersectionDistances))
    # print(intersectionDistances)

inputs = []
with open("input","r") as f:
    inputs = f.readlines()
# inputs = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
# inputs = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
# inputs = ["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]
inputs = [line.split(",") for line in inputs]
calculateIntersections(inputs)
print(intersections)
print(distanceToClosestIntersection(intersections))
calcNearestIntersection()