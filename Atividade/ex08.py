"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

import requests

pais = input('Digite o nome do País: ').lower()
url = f'https://restcountries.com/v3.1/name/{pais}'

def info_pais(name_data):
    if 'nativeName' in name_data:
        chave = list(name_data['nativeName'].keys())[0]
        return name_data['nativeName'][chave]['common']
    return name_data['common']

def info_moeda(currencies_data):
    chave = list(currencies_data.keys())[0]
    nome = currencies_data[chave]['name']
    simbolo = currencies_data[chave]['symbol']
    return nome, simbolo, chave

def info_linguagem(languages_data):
    return ', '.join(languages_data.values())

def info_fronteira(borders_data):
    return ', '.join(borders_data) if borders_data else "Nenhuma fronteira encontrada!"

response = requests.get(url)
data = response.json()[0]

nome_moeda, simbolo, sigla = info_moeda(data['currencies'])

print(f"Nome do país ({info_pais(data['name'])}), Linguagem(s) ({info_linguagem(data['languages'])}), região ({data['region']}), subregião ({data['subregion']}) com a capital ({data['capital'][0]})")
print(f"Sigla da moeda ({sigla}), nome ({nome_moeda}) e símbolo da moeda ({simbolo})")
print(f"Países que fazem fronteira com {info_pais(data['name'])}: {info_fronteira(data.get('borders', []))}")