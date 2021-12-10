def twoAdjacentDigitsSame(digitsList):
    doubleSet = set()
    failedSet = set()
    for i in range(0, len(digitsList) - 1):
        if (digitsList[i] == digitsList[i + 1]):
            if (digitsList[i] in doubleSet):
                failedSet.add(digitsList[i])
            doubleSet.add(digitsList[i])
    return len(doubleSet) > len(failedSet)

def neverDecrease(digitsList):
    for i in range(0, len(digitsList) - 1):
        if (digitsList[i + 1] < digitsList[i]):
            return False
    return True

def digitsListFromNumber(number):
    return [int(n) for n in str(number)]

def evaluate(number):
    digitsList = digitsListFromNumber(number)
    result = False
    result = twoAdjacentDigitsSame(digitsList)
    result = result and neverDecrease(digitsList)
    # for i in range(0, len(digitsList) - 1):
    #     if (digitsList[i + 1] < digitsList[i]):
    #         return False
    #     if (digitsList[i] == digitsList[i + 1]):
    #         result = True
    return result


input = {"low": 240298, "high": 784956}
# input = {"low": 112233, "high": 112233}
# input = {"low": 123444, "high": 123444}
# input = {"low": 111122, "high": 111122}
numbers = list(range(input["low"], input["high"] + 1))
filteredNumbers = list(filter(evaluate, numbers))
print(len(filteredNumbers))


