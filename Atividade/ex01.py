"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

preco_alcool = 1.90
preco_gasolina = 2.50

litros = float(input('Digite a quantidade de litros: '))
tipo = input('Digite o tipo de combustível (A-alcool, G-gasolina): ').upper()

if tipo == 'A':
    if litros <= 20:
        desconto = 0.03
    else:
        desconto = 0.05
    preco_sem_desconto = litros * preco_alcool
    valor_a_pagar = preco_sem_desconto - (preco_sem_desconto * desconto)
    print(f'Valor a pagar: R${valor_a_pagar:.2f}')

elif tipo == 'G':
    if litros <= 20:
        desconto = 0.04
    else:
        desconto = 0.06
    preco_sem_desconto = litros * preco_gasolina
    valor_a_pagar = preco_sem_desconto - (preco_sem_desconto * desconto)
    print(f'Valor a pagar: R${valor_a_pagar:.2f}')

else:
    print('Tipo de combustível inválido!')