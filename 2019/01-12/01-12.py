import math

f = open("input", "r")
lines = f.readlines()
# lines = [1969]
res = 0
for line in lines:
    value = int(line)
    lineRes = math.floor(value / 3) - 2
    while lineRes > 0:
        res += lineRes
        lineRes = math.floor(lineRes / 3) - 2

print(res)