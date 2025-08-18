"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

numeros = []
acima_media = 0

def padrao():
    for i in numeros:
        print(i, end=" ")
    print()

def inverter():
    j = len(numeros)-1
    while j >= 0:
        print(numeros[j], end=" ")
        j -= 1
    print()

while True:
    numero = int(input('Digite um número: '))

    if numero == -1:
        break
    else:
        numeros.append(numero)

print(f'Quantidade de valores lidos: {len(numeros)}')
padrao()
inverter()
print(f'Soma dos números: {sum(numeros)}')

media = sum(numeros) / len(numeros)
print(f'Média dos números: {media}')

for k in numeros:
    if k > media:
        acima_media += 1

print(f'Quantidade de valores acima da média: {acima_media}')