helpContents = [
    "Monta arquivo .qck em .fita\n assemble [i]arquivo.qck",
    "Carrega .fita na memória\n load [i]arquivo.fita",
    "Descarrega .fita da memória\n unload [i]programa",
    "Mostra ocupação da memória\n dump\n dump [i]programa[/i]",
    "Inicia execução de programa\n run [i]programa",
    "Especifica arquivo para IO\n set [i]programa[/i] in  [i]file.txt[/i]\n set [i]programa[/i] out [i]file.txt",
    "Cria arquivo em disco\n create [i]file",
    # "Edita arquivo em disco",
    "Apaga arquivo em disco\n delete [i]file",
    "Limpa o terminal\n clear",
]

validCommands = [
    "assemble",
    "load",
    "unload",
    "dump",
    "run",
    "set",
    "create",
    # "edit",
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
    "BLT", # 22 PC = oper if N = 1 and Z = 0
    "BGT", # 23 PC = oper if N = 0 and Z = 0
    # "POW", # ACC = ACC ** oper
    # "MOV", # ACC = oper
]