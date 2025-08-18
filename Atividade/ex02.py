"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

notas = [100, 50, 10, 5, 1]
resultado = {}

saque = int(input('Digite o valor do seu saque: '))

while True:
    if saque < 10 or saque > 600:
        saque = int(input('Digite um valor válido! (Mínimo: 10 | Máximo: 600): '))
    else:
        break

for nota in notas:
    valor = saque // nota

    if valor > 0:
        resultado[nota] = valor
        saque = saque % nota

for nota, qtd in resultado.items():
    print(f'R$ {nota}: {qtd} nota(s).')