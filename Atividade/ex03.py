"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

nota1 = float(input('Digite a nota 1: '))
nota2 = float(input('Digite a nota 2: '))

media = (nota1 + nota2) / 2

if 9.0 <= media <= 10.0:
  conceito = 'A'
elif 7.5 <= media < 9.0:
  conceito = 'B'
elif 6.0 <= media < 7.5:
  conceito = 'C'
elif 4.0 <= media < 6.0:
  conceito = 'D'
else:
  conceito = 'E'

if conceito in ['A', 'B', 'C']:
  situacao = 'APROVADO'
else:
  situacao = 'REPROVADO'

print('\nNotas: {:.1f} e {:.1f}'.format(nota1, nota2))
print('Média: {:.1f}'.format(media))
print('Conceito: ', conceito)
print('Situação: ', situacao)