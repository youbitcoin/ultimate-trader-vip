import random

def gerar_sinal(ativo):
    direcao = random.choice(["CALL", "PUT"])
    confianca = random.randint(80, 95)

    return f"{direcao} | Confiança: {confianca}% | Ativo: {ativo}"
