import pygame
import math
import sys
sys.path.append("./ambiente/conversor-mapas")
import converte_caverna1
import cria_terreno

# Definir as cores dos diferentes tipos de terreno
AREIA = (244, 164, 96)
MONTANHA = (139, 137, 137)

converte_variavel = {
    "AREIA": AREIA,
    "MONTANHA": MONTANHA,
}

# Definir o custo de cada tipo de terreno
CUSTO = {
    AREIA: 10,
    MONTANHA: 1000,

}

pygame.init()

# Define as dimensões da tela e o tamanho dos tiles
LARGURA_TELA = 756
ALTURA_TELA = 756
TAMANHO_TILE = 18

# Criar a janela
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# Definir as dimensões da matriz do terreno
LINHAS = 28
COLUNAS = 28

# Definir o terreno manualmente
caverna1 = cria_terreno.retorna_caverna1()
caverna1_convertido = converte_caverna1.converte_caverna1(caverna1, converte_variavel)

# Adicionar as coordenadas do ponto de partida e destino
ponto_partida = (3, 13)
ponto_destino1 = (26, 14)

# Classe utilizada para representar cada célula do terreno, sabendo a posição e custo, além de criar/resetar g, h e f 
# que são utilizados pelo algoritmo A*
class Celula:
    def __init__(self, posicao, custo):
        self.posicao = posicao
        self.custo = custo
        self.vizinhos = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.pai = None
        self.visitada = False

    def reset(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.pai = None
        self.visitada = False

# Define a função para calcular a heurística
def heuristica(celula_atual, ponto_destino1):
    # Extrai as coordenadas x e y dos pontos
    x1, y1 = celula_atual.posicao
    x2, y2 = ponto_destino1
    
    # Calcula e retorna a distância Euclidiana entre os pontos e multiplica por 10
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 10

def custo(celula_atual, vizinho):
    if vizinho in celula_atual.vizinhos:
        return celula_atual.custo + vizinho.custo
    else:
        return float('inf')

def desenhar_caminho(caminho_recente, ponto_dest):
    # Desenhar o ponto de destino na nova superfície
    pygame.draw.rect(screen, (79, 79, 79), (ponto_dest[1] * TAMANHO_TILE, ponto_dest[0]*TAMANHO_TILE, TAMANHO_TILE, TAMANHO_TILE))

    # Desenhar o caminho na nova superfície
    for celula in caminho_recente:
        x, y = celula
        rect = pygame.Rect(y * TAMANHO_TILE, x * TAMANHO_TILE, TAMANHO_TILE, TAMANHO_TILE)
        pygame.draw.rect(screen, (255, 0, 0), rect)

        # Desenhar a nova superfície na janela do Pygame
        screen.blit(screen, (0, 0))
        pygame.display.flip()
        pygame.time.wait(70)


def criar_celulas(caverna1_convertido):
    celulas = [[Celula((linha, coluna), CUSTO[caverna1_convertido[linha][coluna]]) for coluna in range(COLUNAS)] for linha in range(LINHAS)]
    
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if linha > 0:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha-1][coluna])
            if linha < LINHAS-1:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha+1][coluna])
            if coluna > 0:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha][coluna-1])
            if coluna < COLUNAS-1:
                celulas[linha][coluna].vizinhos.append(
                    celulas[linha][coluna+1])
    
    return celulas

celulas = criar_celulas(caverna1_convertido)

def algoritmo_a_estrela(celulas, ponto_start, ponto_destino1):
    # Inicializar as listas aberta e fechada
    aberta = []
    fechada = []

    # Adicionar o ponto de partida à lista aberta
    celula_atual = celulas[ponto_start[0]][ponto_start[1]]
    aberta.append(celula_atual)

    # Loop principal do algoritmo A*
    while aberta:
        # Encontrar a célula na lista aberta com o menor valor de f + h
        celula_atual = min(aberta, key=lambda celula: celula.f + celula.h)

        # Se a célula atual for o ponto de destino, retornar o caminho encontrado
        if celula_atual.posicao == ponto_destino1:
            caminho = []
            custo_total = 0
            while celula_atual:
                caminho.append(celula_atual.posicao)
                celula_atual = celula_atual.pai
                if celula_atual:
                    custo_total += celula_atual.custo
            return (caminho[::-1], custo_total)

        # Remover a célula atual da lista aberta e adicioná-la à lista fechada
        aberta.remove(celula_atual)
        fechada.append(celula_atual)

        # Verificar todos os vizinhos da célula atual
        for vizinho in celula_atual.vizinhos:
            # Se o vizinho estiver na lista fechada, ignorá-lo
            if vizinho in fechada:
                continue

            # Calcular o custo do caminho da célula atual até o vizinho
            novo_g = celula_atual.g + custo(celula_atual, vizinho)

            # Se o vizinho não estiver na lista aberta, adicioná-lo
            if vizinho not in aberta:
                aberta.append(vizinho)
            # Se o novo caminho para o vizinho for mais longo do que o já calculado, ignorá-lo
            elif novo_g >= vizinho.g:
                continue

            # Atualizar os valores de g, h e f do vizinho
            vizinho.g = novo_g
            vizinho.h = heuristica(vizinho, ponto_destino1)
            vizinho.f = vizinho.g + vizinho.h
            vizinho.pai = celula_atual

    return None

# Loop principal do jogo

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

# Desenhar o terreno_convertido na tela
# Mapeamento de tipos de terreno para cores
cores_terreno = {
    AREIA: (224, 224, 224),
    MONTANHA: (179, 179, 179),
}

# Desenhar o terreno_convertido na tela
for linha in range(LINHAS):
    for coluna in range(COLUNAS):
        # Define a cor da célula com base no valor de custo
        cor = cores_terreno[caverna1_convertido[linha][coluna]]

        # Desenhar o tile na tela
        pygame.draw.rect(screen, cor, (coluna * TAMANHO_TILE, linha * TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))

destinos = [ponto_destino1]
partida = ponto_partida

#Loop para realizar os testes com todos os destinos
while destinos:
    menor_custo = float('inf')
    melhor_caminho = None
    proximo_destino = None

    for destino in destinos:
        celulas = criar_celulas(caverna1_convertido)
        caminho, custo_total = algoritmo_a_estrela(celulas, partida, destino)

        if custo_total < menor_custo:
            menor_custo = custo_total
            melhor_caminho = caminho
            proximo_destino = destino

    desenhar_caminho(melhor_caminho, proximo_destino)
    partida = proximo_destino
    destinos.remove(proximo_destino)
