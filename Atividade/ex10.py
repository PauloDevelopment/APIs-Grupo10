"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

import requests
from json.decoder import JSONDecodeError

zonas_sp = {
    'Norte': [
        'Santana', 'Tucuruvi', 'Jaçanã', 'Tremembé', 'Casa Verde', 'Mandaqui', 'Vila Maria Alta',
        'Vila Maria', 'Vila Guilherme', 'Freguesia do Ó', 'Brasilândia', 'Cachoeirinha', 'Limão',
        'Perus', 'Jaraguá', 'Pirituba'
    ],
    'Sul': [
        'Jabaquara', 'Santo Amaro', 'Campo Limpo', 'Capão Redondo', 'Vila Andrade', 'Capela do Socorro',
        'Cidade Dutra', 'Grajaú', 'Socorro', 'Cidade Ademar', 'Pedreira', 'Ipiranga', 'Sacomã', 
        'M’Boi Mirim', 'Jardim Ângela', 'Jardim São Luís', 'Parelheiros', 'Marsilac', 'Moema', 'Saúde',
        'Vila Mariana', 'Campo Belo', 'Campo Grande'
    ],
    'Leste': [
        'Tatuapé', 'Penha', 'Mooca', 'Itaquera', 'Vila Prudente', 'São Mateus', 'São Miguel Paulista',
        'São Rafael', 'São Lucas', 'Vila Jacuí', 'Sapopemba', 'Vila Matilde', 'Artur Alvim', 'Cangaíba',
        'Vila Formosa', 'Ermelino Matarazzo', 'Guaianases', 'Lajeado', 'Itaim Paulista', 'Vila Curuçá',
        'Cidade Líder', 'José Bonifácio', 'Parque do Carmo', 'Belém', 'Brás', 'Pari'
    ],
    'Oeste': [
        'Pinheiros', 'Lapa', 'Butantã', 'Perdizes', 'Alto de Pinheiros', 'Vila Madalena', 'Vila Leopoldina',
        'Barra Funda', 'Jaguara', 'Jaguaré', 'Vila Sônia', 'Morumbi', 'Raposo Tavares', 'Rio Pequeno',
        'Itaim Bibi', 'Jardim Paulista'
    ],
    'Centro': [
        'Sé', 'Consolação', 'Liberdade', 'República', 'Bela Vista', 'Bom Retiro', 'Cambuci', 'Campos Elíseos',
        'Santa Cecília', 'Santa Efigênia', 'Aclimação', 'Vila Buarque'
    ]
}

cep = input('Digite o CEP: ')
url = f'https://viacep.com.br/ws/{cep}/json/'

try:
    response = requests.get(url)
    
    if not response.text.strip():
        print("CEP inválido ou não encontrado!")
    else:
        data = response.json()
        
        if 'erro' in data:
            print("CEP não encontrado!")
        else:
            bairro = data['bairro']
            cidade = data['localidade']
            uf = data['uf']

            if uf == 'SP' and cidade.lower() == 'são paulo':
                zona = 'Fora da Grande São Paulo'
                for z, bairros in zonas_sp.items():
                    if bairro in bairros:
                        zona = z
                        break
                print(f"Bairro: {bairro}, Zona {zona} de São Paulo.")
            else:
                print(f"Bairro: {bairro}, Fora da Grande São Paulo.")

except JSONDecodeError:
    print('Erro ao decodificar o JSON!')
except requests.RequestException:
    print('Erro ao acessar o serviço de CEP!')