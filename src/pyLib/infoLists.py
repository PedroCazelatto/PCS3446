helpContents = [
    "Monta arquivo .qck em .fita",
    "Carrega .fita na memória",
    "Descarrega .fita da memória",
    "Adiciona processo",
    "Cria arquivo em disco",
    "Edita arquivo em disco",
    "Apaga arquivo em disco",
    "Limpa o terminal",
]

validCommands = [
    "assemble",
    "load",
    "unload",
    "run",
    "create",
    "edit",
    "delete",
    "clear",
]

keysToIgnore = [
    "ctrl+@",
    "ctrl+q",
    "ctrl+w",
    "ctrl+e",
    "ctrl+r",
    "ctrl+t",
    "ctrl+y",
    "ctrl+u",
    "ctrl+o",
    "ctrl+p",
    "ctrl+a",
    "ctrl+s",
    "ctrl+d",
    "ctrl+f",
    "ctrl+g",
    "ctrl+j",
    "ctrl+k",
    "ctrl+l",
    "ctrl+ç",
    "ctrl+z",
    "ctrl+x",
    "ctrl+c",
    "ctrl+v",
    "ctrl+b",
    "ctrl+n",
    "ctrl+m",
]

operations = [
    "HLT", #  0 Stop execution
    "LDA", #  1 ACC = MEM[oper]
    "STA", #  2 MEM[oper] = ACC
    "NEG", #  3 ACC = -ACC
    "ADD", #  4 ACC = ACC + MEM[oper]
    "SUB", #  5 ACC = ACC - MEM[oper]
    "MUL", #  6 ACC = ACC * MEM[oper]
    "DIV", #  7 ACC = ACC / MEM[oper]
    "REM", #  8 ACC = ACC % MEM[oper]
    "AND", #  9 ACC = ACC and MEM[oper]
    "ORR", # 10 ACC = ACC or MEM[oper]
    "NOT", # 11 ACC = not ACC
    "XOR", # 12 ACC = ACC xor MEM[oper]
    "TXT", # 13 MEM[oper] = ASCII(ACC) 
    "WRD", # 14 ACC = number(MEM[oper])
    "INP", # 15 To MEM[oper], first byte indicates how many ASCII chars
    "OUT", # 16 From MEM[oper], first byte indicates how many ASCII chars
    "CMP", # 17 N and Z acording to ACC - MEM[oper]
    "BEQ", # 18 PC = oper if Z = 1
    "BNE", # 19 PC = oper if Z = 0
    "JMP", # 20 PC = oper
    "SET", # 21 Flags (I N Z) = oper
    # "POW", # ACC = ACC ** oper
    # "MOV", # ACC = oper
]