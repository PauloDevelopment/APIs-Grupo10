"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

sal_inicial = float(input("Digite o salário inicial: R$ "))

ano_contratacao = 1995
ano_atual = 2025

sal = sal_inicial
perc = 1.5

sal += sal_inicial * (perc / 100)

for ano in range(1997, ano_atual + 1):
    perc *= 2
    sal += sal * (perc / 100)

print(f"O salário atual em {ano_atual} é: R$ {sal:.2f}")