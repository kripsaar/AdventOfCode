import math

layers = []
xSize = 25
ySize = 6

def fillLayers(input):
    layer = {}
    i = 0
    x = 0
    y = 0
    while i < len(input):
        if x == 0 and y == 0:
            layer = {}
            layers.append(layer)
        if x not in layer.keys():
            layer[x] = {}
        layer[x][y] = input[i]
        i += 1
        x = i % xSize
        if x == 0:
            y = (y + 1) % ySize
        
def printLayer(layer):
    print("")
    x = 0
    y = 0
    for y in range(0, ySize):
        line = ""
        for x in range(0, xSize):
            char = " "
            if layer[x][y] != 0:
                char = "*"
            line += char
        print(line)

def printLayers():
    i = 1
    for layer in layers:
        print("Layer " + str(i) + ":")
        printLayer(layer)
        print("")
        i += 1

        

def countDigit(layer, digit):
    digitsInLayer = [item for subdict in layer.values() for item in subdict.values()]
    digit = list(filter(lambda x: x == digit, digitsInLayer))
    return len(digit)

def getLayerWithFewestZeroes():
    minLayer = layers[0]
    minZeroes = math.inf
    for layer in layers:
        zeroes = countDigit(layer, 0)
        if zeroes < minZeroes:
            minZeroes = zeroes
            minLayer = layer
    return minLayer

def calculateLayerScore(layer):
    onesCount = countDigit(layer, 1)
    twosCount = countDigit(layer, 2)
    return onesCount * twosCount

def calcPicture():
    picture = {}
    for y in range(0, ySize):
        for x in range(0, xSize):
            if x not in picture.keys():
                picture[x] = {}
            for layer in layers:
                pixel = layer[x][y]
                picture[x][y] = pixel
                if (pixel != 2):
                    break
    return picture

xSize = 25
ySize = 6
filename = "input"
# filename = "example2"
input = []
with open(filename, "r") as f:
    input = [int(n) for n in f.read()]

fillLayers(input)

# score = calculateLayerScore(getLayerWithFewestZeroes())
# print(score)

picture = calcPicture()
printLayer(picture)