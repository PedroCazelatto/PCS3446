import os

from pyLib.infoLists import operations

def toBin(integer: int, size: int) -> str:
    binary = bin(integer)[2:]
    leadZeros = '0' * (size - len(binary))
    return leadZeros + binary

def assemble(inputFile: str):
    if not os.path.exists("./root/" + inputFile):
        return [False, "Arquivo inexistente: " + inputFile]
    
    file = list()
    
    labels = list()
    labelValues = list()
    instructions = list()
    memoryPos = list()
    
    jumpLabels = 0
    
    began = False
    ended = False
    
    with open("./root/" + inputFile) as f:
        for line in f:
            line = line.replace('\n', '')
            file.append(line)

    for i in range(len(file)):
        file[i] = file[i].split()
        
    if file.count(["BEGIN"]) == 0:
        return [False, "File doesn't have BEGIN"]
    
    beginIndex = file.index(["BEGIN"])
    
    if file.count(["END"]) == 0:
        return [False, "File doesn't have END"]
    
    # First reading of file to get labels
    for idx, line in enumerate(file):
        if ended:
            return [False, "File didn't ended at END"]
        if line[0] == "BEGIN":
            began = True
            continue
        if line[0] == "END":
            ended = True
            continue
        if line[0][-1] == ':':
            if began:
                if len(line) != 1:
                    return [False, "Too much args on label at line " + str(idx + 1)]
                labels.append(line[0][:-1])
                labelValues.append(idx - beginIndex - 1 - jumpLabels)
                jumpLabels += 1
                continue
            if len(line) != 3:
                return [False, "Something is missing at line " + str(idx + 1)]
            if line[1] == ".word":
                labels.append(line[0][:-1])
                labelValues.append(line[2])
                continue
            if line[1] == ".text":
                labels.append(line[0][:-1])
                realText = ' '.join(line[2:])
                labelValues.append([len(realText) - 2, list(realText[1:-1].encode('ascii'))])
                continue
        if operations.count(line[0]) == 0:
            return [False, "Wrong instruction at line " + str(idx + 1)]
        instructions.append(line)
    
    dataStart = len(instructions)
    
    for value in labelValues:
        if isinstance(value, str):
            memoryPos.append(dataStart)
            dataStart += 1
            continue
        if isinstance(value, int):
            continue
        memoryPos.append(dataStart)
        dataStart += value[0]
        
    for idx, inst in enumerate(instructions):
        if inst[0] == "HLT" or inst[0] == "NEG" or inst[0] == "NOT":
            if len(inst) != 1:
                return [False, "Too few operands at line " + str(beginIndex + idx + 1)]
            instructions[idx].append(0)
        elif inst[0] == "SET":
            instructions[idx][1] = int(inst[1])
        else:
            if len(inst) != 2:
                return [False, "Too much args at " + str(inst)]
        instructions[idx][0] = operations.index(inst[0])
        if not isinstance(instructions[idx][1], int):
            if labels.count(inst[1]) == 0:
                return [False, "Couldn't find label " + inst[1]]
            labelIndex = labels.index(inst[1])
            value = labelValues[labelIndex]
            if isinstance(value, int):
                instructions[idx][1] = value
            else:
                instructions[idx][1] = memoryPos[labelIndex]
                
    outputFile = inputFile[:-4] + ".fita"
    
    with open("./root/" + outputFile, 'wt') as f:
        for inst in instructions:
            f.write(toBin(inst[0], 14) + toBin(inst[1], 18) + "\n")
        for value in labelValues:
            if isinstance(value, str):
                f.write(toBin(int(value), 32) + "\n")
                continue
            if isinstance(value, int):
                continue
            f.write(toBin(value[0], 8))
            for i in range(value[0]):
                f.write(toBin(value[1][i], 8))
                if (i+2) % 4 == 0:
                    f.write("\n")
            bytesToComplete = 3 - (value[0] % 4)
            if bytesToComplete > 0:
                f.write(toBin(0, bytesToComplete * 8) + "\n")
    
    return [True, "Assembled " + inputFile + " into " + outputFile]