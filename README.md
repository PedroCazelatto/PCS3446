# PCS3446
Projeto da disciplina PCS3446 - Sistemas Operacionais (2022), da graduação em Engenharia Elétrica da POLI-USP.

Consiste em uma aplicação que simule um sistema operacional e seus componentes.

# Instruções de Instalação

Primeiro, instale a biblioteca Textual com 
```
python3 -m pip install textual
```
Depois, na pasta do projeto, execute
```
cd src
python3 main.py
```

# Descrição Detalhada

A aplicação simula um sistema operacional executando em um processador de 32 bits baseado em acumulador, projetado na disciplina PCS3216 - Sistemas de Programação.

## Processador

O processador é baseado em um único registrador de propósito geral, o acumulador. Instruções e dados possuem 32 bits, sendo 14 bits de opcode e 18 bits de endereçamento direto (operando).

## Memória

O sistema possui uma memória principal de 256 KiB, particionada com alocação *First Fit* e sem *Garbage Collection*.

## Disco Virtual

A aplicação possui acesso apenas a pasta **./src/root/**, que é onde os arquivos **.qck** e **.fita** deverão ser armazenados. 