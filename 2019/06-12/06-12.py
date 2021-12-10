import math

class OrbitObject:
    def __init__(self, name):
        self.name = name
        self.objectsInOrbit = []
        self.inOrbitAround = []
    def __str__(self):
        return self.name + ":\n   Parents: " + str([p.name for p in self.inOrbitAround]) + "\n   Children: " + str([c.name for c in self.objectsInOrbit])

def countOrbits(obj):
    count = 0
    for child in obj.objectsInOrbit:
        count += 1
        count += countOrbits(child)
    return count

def countTotalOrbits(objectsList):
    count = 0
    for obj in objectsList:
        count += countOrbits(obj)
    return count

def findAllOrbits(obj):
    orbits = set(obj.inOrbitAround)
    for parent in obj.inOrbitAround:
        orbits.update(findAllOrbits(parent))
    return orbits

def findCommonOrbits(obj1, obj2):
    orbits1 = findAllOrbits(obj1)
    orbits2 = findAllOrbits(obj2)
    commonOrbits = orbits1 & orbits2
    return commonOrbits

def distanceToAncestor(obj, parent):
    if obj == parent:
        return 0
    if len(obj.inOrbitAround) < 1:
        return math.inf
    if parent in obj.inOrbitAround:
        return 1
    dist = math.inf
    for immediateParent in obj.inOrbitAround:
        dist = min(dist, distanceToAncestor(immediateParent, parent))
    return dist + 1

def calcDistance(obj1, obj2):
    commonOrbits = findCommonOrbits(obj1, obj2)
    distance1 = math.inf
    distance2 = math.inf
    for orbit in commonOrbits:
        distance1 = min(distance1, distanceToAncestor(obj1, orbit))
        distance2 = min(distance2, distanceToAncestor(obj2, orbit))
    return distance1 + distance2

objects = {}
# with open("example2","r") as f:
with open("input","r") as f:
    for line in f.readlines():
        line = line.split(")")
        parentName = line[0]
        childName = line[1].rstrip()
        parent = OrbitObject(parentName)
        child = OrbitObject(childName)
        if parentName not in objects.keys():
            objects[parentName] = parent
        else:
            parent = objects[parentName]
        if childName not in objects.keys():
            objects[childName] = child
        else:
            child = objects[childName]
        if child not in parent.objectsInOrbit:
            parent.objectsInOrbit.append(child)
        if parent not in child.inOrbitAround:
            child.inOrbitAround.append(parent)

# orbits = 0
# roots = list(filter(lambda x: len(x.inOrbitAround) == 0, objects.values()))
# orbits = countTotalOrbits(list(objects.values()))
# print(orbits)

# print([obj.name for obj in findCommonOrbits(objects["L"], objects["I"])])
print(calcDistance(objects["YOU"], objects["SAN"]) - 2)
# print(distanceToAncestor(objects["L"], objects["E"]))