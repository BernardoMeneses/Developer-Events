import math
import time
import matplotlib.pyplot as plt

"""
    Calcula a distância euclidiana entre dois pontos.
    
    Parâmetros:
    - p1: Um ponto representado como uma tupla (x, y).
    - p2: Outro ponto representado como uma tupla (x, y).
    
    Resultado:
    - Um número representando a distância euclidiana entre os dois pontos.
    """
def calcular_distancia(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

"""
    Encontra o vizinho mais próximo de um ponto em uma lista de pontos.
    
    Parâmetros:
    - ponto_atual: O ponto de referência para encontrar o vizinho mais próximo.
    - pontos: Uma lista de pontos a serem considerados.
    
    Resultado:
    - O ponto mais próximo de ponto_atual na lista de pontos.
    """
def encontrar_vizinho_mais_proximo(ponto_atual, pontos):
    pontos_restantes = [p for p in pontos if p != ponto_atual]
    return min(pontos_restantes, key=lambda p: calcular_distancia(ponto_atual, p))

"""
    Calcula a autonomia total gasta ao percorrer uma rota fechada.
    
    Parâmetros:
    - rota: Uma lista de pontos representando a rota fechada.
    
    Resultado:
    - Um número representando a autonomia total gasta ao percorrer a rota.
    """
def calcular_autonomia_gasta(rota):
    autonomia_gasta = 0
    for i in range(len(rota) - 1):
        autonomia_gasta += calcular_distancia(rota[i], rota[i + 1])
    autonomia_gasta += calcular_distancia(rota[-1], rota[0])  # Adiciona a distância de volta ao ponto inicial.
    return autonomia_gasta

"""
    Calcula a rota utilizando o algoritmo do vizinho mais próximo com uma autonomia máxima.
    
    Parâmetros:
    - pontos: Uma lista de pontos a serem visitados.
    - autonomia_max: A autonomia máxima do veículo.
    
    Resultado:
    - Uma lista de pontos representando a rota fechada.
    """
def calcular_rota_vizinho_mais_proximo_limitado(pontos, autonomia_max):
    rota = [pontos[0]]  # Começa no ponto inicial
    pontos_restantes = set(pontos[1:])
    autonomia_atual = 0

    while pontos_restantes:
        ponto_atual = rota[-1]
        vizinho_mais_proximo = encontrar_vizinho_mais_proximo(ponto_atual, pontos_restantes)

        distancia_ponto = calcular_distancia(ponto_atual, vizinho_mais_proximo)

        distancia_ao_inicio = calcular_distancia(vizinho_mais_proximo, rota[0])  # Distância para voltar ao ponto inicial

        if autonomia_atual + distancia_ponto <= autonomia_max and autonomia_atual + distancia_ponto + distancia_ao_inicio <= autonomia_max:
            rota.append(vizinho_mais_proximo)
            pontos_restantes.remove(vizinho_mais_proximo)
            autonomia_atual += distancia_ponto
        else:
            # Retorna ao ponto inicial se a autonomia não for suficiente para ir ao próximo ponto e voltar
            rota.append(rota[0])
            break

    return rota

"""
    Desenha a rota em um gráfico.

    Parâmetros:
    - rota: Uma lista de pontos representando a rota fechada.
    - I: O ponto inicial.

    Resultado:
    - Exibe o gráfico com a rota.
    """
def desenhar_rota(rota, I):
    plt.scatter(*zip(*rota), color='red')

    x1, y1 = I
    for x2, y2 in rota:
        plt.plot([x1, x2], [y1, y2], 'b-')
        x1, y1 = x2, y2

    plt.plot([x1, I[0]], [y1, I[1]], 'b-')  # Linha de volta ao ponto inicial.

    plt.show()

"""
    Lê os pontos de um arquivo.

    Parâmetros:
    - nome_arquivo: O nome do arquivo contendo os pontos.

    Resultado:
    - Uma lista de pontos lidos do arquivo.
    """
def ler_pontos_do_arquivo(nome_arquivo):
    with open(nome_arquivo, "r") as f:
        return [tuple(map(int, linha.split("\t"))) for linha in f.readlines()]

"""
    Mede o tempo de execução de uma função.

    Parâmetros:
    - funcao: A função a ser executada.
    - *args: Os argumentos a serem passados para a função.

    Resultado:
    - Uma tupla contendo o resultado da função e o tempo de execução.
    """
def medir_tempo_execucao(funcao, *args):
    inicio = time.time()
    resultado = funcao(*args)
    fim = time.time()
    tempo_execucao = fim - inicio
    return resultado, tempo_execucao

"""
    Salva a rota em um arquivo.

    Parâmetros:
    - nome_arquivo: O nome do arquivo de destino.
    - rota: Uma lista de pontos representando a rota a ser salva.

    Resultado:
    - O arquivo é criado e a rota é salva no arquivo.
    """
def salvar_rota_no_arquivo(nome_arquivo, rota):
    with open(nome_arquivo, "w") as f:
        f.write("\n".join("\t".join(map(str, p)) for p in rota))

"""
    Função principal para calcular e salvar a rota.

    Parâmetros:
    - nome_arquivo_entrada: O nome do arquivo de entrada contendo os pontos.
    - nome_arquivo_saida: O nome do arquivo de saída para salvar a rota.
    - autonomia_max: A autonomia máxima do veículo.
    """
def main(nome_arquivo_entrada, nome_arquivo_saida, autonomia_max):
    pontos = ler_pontos_do_arquivo(nome_arquivo_entrada)
    rota = calcular_rota_vizinho_mais_proximo_limitado(pontos, autonomia_max)
    salvar_rota_no_arquivo(nome_arquivo_saida, rota)

if __name__ == "__main__":
    autonomia_max = 2000
    
    # Para 100 pontos
    main("pontos100.txt", "resultados100.txt", autonomia_max)
    
    # Para 1k pontos
    main("pontos1k.txt", "resultados1k.txt", autonomia_max)
    
    # Para 10k pontos
    main("pontos10k.txt", "resultados10k.txt", autonomia_max)
    
    # Medição de tempo e exibição de resultados
    resultado_100, tempo_100 = medir_tempo_execucao(calcular_rota_vizinho_mais_proximo_limitado, ler_pontos_do_arquivo("pontos100.txt"), autonomia_max)
    resultado_1k, tempo_1k = medir_tempo_execucao(calcular_rota_vizinho_mais_proximo_limitado, ler_pontos_do_arquivo("pontos1k.txt"), autonomia_max)
    resultado_10k, tempo_10k = medir_tempo_execucao(calcular_rota_vizinho_mais_proximo_limitado, ler_pontos_do_arquivo("pontos10k.txt"), autonomia_max)

    print("\nPara 100 pontos:")
    print("Tempo de execução:", tempo_100, "segundos")
    print("Total de pontos visitados:", len(resultado_100))
    print("Autonomia total gasta:", calcular_autonomia_gasta(resultado_100))

    desenhar_rota(resultado_100, (500, 0))

    print("\nPara 1k pontos:")
    print("Tempo de execução:", tempo_1k, "segundos")
    print("Total de pontos visitados:", len(resultado_1k))
    print("Autonomia total gasta:", calcular_autonomia_gasta(resultado_1k))

    desenhar_rota(resultado_1k, (500, 0))

    print("\nPara 10k pontos:")
    print("Tempo de execução:", tempo_10k, "segundos")
    print("Total de pontos visitados:", len(resultado_10k))
    print("Autonomia total gasta:", calcular_autonomia_gasta(resultado_10k))

    desenhar_rota(resultado_10k, (500, 0))