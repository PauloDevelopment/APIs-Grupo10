"""
Integrantes do grupo 10:

Gustavo Meirelles Festa
Paulo Henrique Pires Cordeiro
Paula Silveira e Silva
"""

cardapio = {
    100: {"item": "Cachorro Quente", "preco": 1.20},
    101: {"item": "Bauru Simples", "preco": 1.30},
    102: {"item": "Bauru com ovo", "preco": 1.50},
    103: {"item": "Hambúrguer", "preco": 1.20},
    104: {"item": "Cheeseburguer", "preco": 1.30},
    105: {"item": "Refrigerante", "preco": 1.00}
}

def fazer_pedido():
    
    total = 0.0
    pedido = []

    print("Bem-vindo(a) à Lanchonete!")
    print("--- Cardápio ---")
    print("Código | Especificação   | Preço")
    print("---------------------------------")
    for codigo, i in cardapio.items():
        print(f"{codigo: }  | {i['item']} | R$ {i['preco']:.2f}")
    print("---------------------------------")
    print("Digite 'pagar' para finalizar o pedido.")

    while True:
        try:
            codigo = input("Digite o código do item: ")
            
            if codigo.lower() == 'pagar':
                break

            codigo = int(codigo)

            if codigo not in cardapio:
                print(f"Código {codigo} não existe!.")
                continue

            quantidade =  int(input("Digite a quantidade do item: "))

            if quantidade <= 0:
                print("A quantidade deve ser um número inteiro positivo.")
                continue

            item = cardapio[codigo]
            preco_unitario = item["preco"]
            valor= preco_unitario * quantidade
            total += valor

            pedido.append({
                "item": item["item"],
                "quantidade": quantidade,
                "valor_item": valor
            })

        except ValueError:
            print("Entrada inválida.")
        
    mostrar_resumo(pedido, total)

def mostrar_resumo(pedido, total):
   
    print("\n--- Resumo do Pedido ---")
    if not pedido:
        print("Nenhum item foi pedido.")
    else:
        for item in pedido:
            print(f"{item['quantidade']}x {item['item']:<17} - R$ {item['valor_item']:.2f}")

        print("---------------------------------")
        print(f"Total: R$ {total:.2f}")

fazer_pedido()