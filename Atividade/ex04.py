"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

gabarito = ['C', 'A', 'D', 'B', 'E', 'A', 'C', 'D', 'B', 'E']
validas = ['A', 'B', 'C', 'D', 'E']
notas = []
acertos = 0

while True:
    acertos = 0
    for i in range(10):
        while True:
            respostas = input(f'Digite a resposta da {i+1}ª pergunta: ').upper()
            if respostas in validas:
                break
            else:
                print('Resposta inválida! Digita uma letra de A até E.')

        if respostas == gabarito[i]:
            acertos += 1

    notas.append(acertos)
    print(f'Você acertou {acertos} questões!')

    continuar = input('Outro aluno deseja fazer a prova (s/n): ').lower()
    if continuar != 's':
        break

print(f'Maior nota: {max(notas)}')
print(f'Menor nota: {min(notas)}')
print(f'Total de alunos que utilizaram o sistema: {len(notas)}')
print(f'Média das notas da turma: {sum(notas) / len(notas):.2f}')