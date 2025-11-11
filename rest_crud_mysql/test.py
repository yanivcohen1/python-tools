digits = ['1','2','3', '4', '5'] # all used digits
numbersLen = 5 # Length of the digits in the number
totalSum = 0 # the total summ of all 5 digits numbers

def calcRecortion(currentNumbers: list[str]):
    global totalSum
    if len(currentNumbers) >= numbersLen: totalSum += int("".join(currentNumbers))
    else: [calcRecortion(currentNumbers + [j]) for j in digits if j not in currentNumbers]

calcRecortion([])
print(totalSum)
