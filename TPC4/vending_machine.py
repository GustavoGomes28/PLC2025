import json
from datetime import datetime

# carrega stock do ficheiro
def carregar_stock():
    try:
        f = open('stock.json', 'r', encoding='utf-8')
        stock = json.load(f)
        f.close()
        print(f"maq: {datetime.now().strftime('%Y-%m-%d')}, Stock carregado, Estado atualizado.")
        return stock
    except:
        print("maq: Erro ao carregar stock.")
        return []

# guarda stock no ficheiro
def guardar_stock(stock):
    f = open('stock.json', 'w', encoding='utf-8')
    json.dump(stock, f, indent=2, ensure_ascii=False)
    f.close()

def listar(stock):
    print("maq:")
    print("cod | nome                | quantidade | preço")
    print("-" * 50)
    for p in stock:
        print(f"{p['cod']:4} {p['nome']:20} {p['quant']:10} {p['preco']:.2f}€")

def processar_moeda(m):
    # converte moeda tipo "1e" ou "20c" para centimos
    m = m.lower().strip()
    valor = 0
    
    if 'e' in m:
        euros = m.split('e')[0]
        if euros:
            valor = int(euros) * 100
    elif 'c' in m:
        cents = m.split('c')[0]
        if cents:
            valor = int(cents)
    
    return valor

def mostrar_saldo(saldo):
    e = saldo // 100
    c = saldo % 100
    if e > 0 and c > 0:
        print(f"maq: Saldo = {e}e{c}c")
    elif e > 0:
        print(f"maq: Saldo = {e}e")
    else:
        print(f"maq: Saldo = {c}c")

def selecionar(stock, codigo, saldo):
    # procura produto
    prod = None
    for p in stock:
        if p['cod'].upper() == codigo.upper():
            prod = p
            break
    
    if prod == None:
        print(f"maq: Produto com código '{codigo}' não encontrado.")
        return saldo
    
    if prod['quant'] == 0:
        print(f"maq: Produto '{prod['nome']}' esgotado.")
        return saldo
    
    preco = int(prod['preco'] * 100)
    
    if saldo < preco:
        print("maq: Saldo insufuciente para satisfazer o seu pedido")
        
        # mostra saldo e pedido
        se = saldo // 100
        sc = saldo % 100
        pe = preco // 100
        pc = preco % 100
        
        if se > 0:
            saldo_str = f"{se}e{sc}c"
        else:
            saldo_str = f"{sc}c"
        
        if pe > 0:
            pedido_str = f"{pe}e{pc}c"
        else:
            pedido_str = f"{pc}c"
        
        print(f"maq: Saldo = {saldo_str}; Pedido = {pedido_str}")
        return saldo
    
    # dispensa produto
    prod['quant'] = prod['quant'] - 1
    saldo = saldo - preco
    print(f"maq: Pode retirar o produto dispensado \"{prod['nome']}\"")
    mostrar_saldo(saldo)
    
    return saldo

def dar_troco(saldo):
    if saldo == 0:
        return
    
    moedas = [200, 100, 50, 20, 10, 5, 2, 1]
    troco = []
    resto = saldo
    
    for m in moedas:
        while resto >= m:
            troco.append(m)
            resto = resto - m
    
    # conta moedas
    contagem = {}
    for m in troco:
        if m in contagem:
            contagem[m] = contagem[m] + 1
        else:
            contagem[m] = 1
    
    # formata troco
    partes = []
    moedas_ord = sorted(contagem.keys(), reverse=True)
    for m in moedas_ord:
        q = contagem[m]
        if m >= 100:
            valor = f"{m // 100}e"
        else:
            valor = f"{m}c"
        partes.append(f"{q}x {valor}")
    
    texto = ", ".join(partes)
    print(f"maq: Pode retirar o troco: {texto}.")

# programa principal
stock = carregar_stock()
saldo = 0

print("maq: Bom dia. Estou disponível para atender o seu pedido.")

while True:
    cmd = input(">> ").strip()
    
    if not cmd:
        continue
    
    partes = cmd.split()
    acao = partes[0].upper()
    
    if acao == "LISTAR":
        listar(stock)
    
    elif acao == "MOEDA":
        # processa todas as moedas
        resto_cmd = " ".join(partes[1:])
        moedas = resto_cmd.split(',')
        for m in moedas:
            m = m.strip()
            if m:
                saldo = saldo + processar_moeda(m)
        mostrar_saldo(saldo)
    
    elif acao == "SELECIONAR":
        if len(partes) < 2:
            print("maq: Indique o código do produto.")
        else:
            saldo = selecionar(stock, partes[1], saldo)
    
    elif acao == "SAIR":
        dar_troco(saldo)
        saldo = 0
        print("maq: Até à próxima")
        guardar_stock(stock)
        break
    
    elif acao == "ADICIONAR":
        # comando extra para adicionar stock
        if len(partes) >= 4:
            cod = partes[1]
            quant = int(partes[-2])
            preco = float(partes[-1])
            nome = " ".join(partes[2:-2])
            
            # verifica se produto existe
            existe = False
            for p in stock:
                if p['cod'].upper() == cod.upper():
                    p['quant'] = p['quant'] + quant
                    print(f"maq: Stock atualizado para '{nome}'.")
                    existe = True
                    break
            
            if not existe:
                stock.append({"cod": cod, "nome": nome, "quant": quant, "preco": preco})
                print(f"maq: Produto '{nome}' adicionado.")
    
    else:
        print(f"maq: Comando desconhecido.")