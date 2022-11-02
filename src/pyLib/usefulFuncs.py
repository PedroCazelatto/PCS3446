def toBin(integer: int, size: int) -> str:
    number = bin(integer)[2:]
    leadZeros = '0' * (size - len(number))
    return leadZeros + number

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