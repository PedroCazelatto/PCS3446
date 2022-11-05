import numpy as np

def toBin(integer: int, size: int) -> str:
    return np.binary_repr(integer, size)

def twoComp(binary: str, size: int) -> int:
    if binary[0] == '0':
        return int(binary, base= 2)
    return int(binary, base= 2) - 2**size

def toInt(integer: int, size: int) -> str:
    leadZeros = ' ' * (size - len(str(integer)))
    return leadZeros + str(integer)

def toHex(integer: int, size: int) -> str:
    number = hex(integer)[2:].upper()
    leadZeros = '0' * (size - len(number))
    expandedHex = leadZeros + number
    separetedHex = ''
    for i in range(len(expandedHex)-1, 0, -2):
        separetedHex = expandedHex[i-1] + expandedHex[i] + ' ' + separetedHex
    return separetedHex

def toASCII(phrase: str, size: int):
    wordsList = list()
    word = toBin(size, 8)
    for i in range(size):
        if i < len(phrase):
            word += toBin(ord(phrase[i]), 8)
        else:
            word += ('0' * 8)
        if i % 4 == 2:
            wordsList.append(int(word, base= 2))
            word = ''
    return wordsList