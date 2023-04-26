import pygame
import math
import cavernas
import sys
sys.path.append("./Zelda/functions")
import converte_terreno
sys.path.append("./Zelda/functions")
import cria_terreno

# Definir as cores dos diferentes tipos de terreno
GRAMA = (124, 252, 0)
AREIA = (244, 164, 96)
FLORESTA = (34, 139, 34)
MONTANHA = (139, 137, 137)
AGUA = (30, 144, 255)
CAMINHO = (224, 224, 224)
PAREDE = (139, 137, 137)

# Dicionário que pega a string e transforma em uma variável correspondente e para poder ser utilizado na definição do CUSTO
converte_variavel = {
    "GRAMA": GRAMA,
    "AREIA": AREIA,
    "FLORESTA": FLORESTA,
    "MONTANHA": MONTANHA,
    "AGUA": AGUA,
    "CAMINHO": CAMINHO,
    "PAREDE": PAREDE
}

# Definir o custo de cada tipo de terreno
CUSTO = {
    GRAMA: 10,
    AREIA: 20,
    FLORESTA: 100,
    MONTANHA: 150,
    AGUA: 180
}

pygame.init()

# Define as dimensões da tela e o tamanho dos tiles
LARGURA_TELA = 756
ALTURA_TELA = 756
TAMANHO_TILE = 18

# Criar a janela
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

# Definir as dimensões da matriz do terreno
LINHAS = 42
COLUNAS = 42

# Definir o terreno manualmente
caverna1 = cria_terreno.retorna_caverna1()
caverna2 = cria_terreno.retorna_caverna2()
caverna3 = cria_terreno.retorna_caverna3()
terreno = cria_terreno.retorna_terreno()
terreno_convertido = converte_terreno.converte_terreno(terreno, converte_variavel)

# Adicionar as coordenadas do ponto de partida e destino do terreno principal
ponto_partida = (28, 25)
ponto_destino1 = (32, 5)
ponto_destino2 = (17, 39)
ponto_destino3 = (1, 24)
ponto_espada = (1, 2)
chegada = (6, 7)

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

# Calcula o custo entre a celula atual e o vizinho para saber se está acima, embaixo ou ao lado direito ou esquero.
# Se for o caso retorna o valor do custo atual mais o valor do vizinho, caso contrário retorna um valor infinito indicando que não há caminho direto
def custo(celula_atual, vizinho):
    if vizinho in celula_atual.vizinhos:
        return celula_atual.custo + vizinho.custo
    else:
        return float('inf')
    
sword = pygame.image.load('./Zelda/icons/sword.png')
swordoff = pygame.image.load('./Zelda/icons/swordoff.png')
door1 = pygame.image.load('./Zelda/icons/door.png')
door2 = pygame.image.load('./Zelda/icons/door.png')
door3 = pygame.image.load('./Zelda/icons/door.png')
portal = pygame.image.load('./Zelda/icons/portal.png')
mago = pygame.image.load('./Zelda/icons/mago.png')

espada_coletada = False

def desenhar_caminho(caminho_recente, espada_coletada):

    clock = pygame.time.Clock()
    # Desenhar o caminho na nova superfície
    for i, celula in enumerate(caminho_recente):
        x, y = celula
        
        # Para impedir que o "rastro" do mago fique salvo no caminho que ele já passou porem deixa uma cor um pouco diferente
        # para saber que ele percorreu aquele caminho
        if i > 0:
            pygame.draw.rect(screen, (174, 242, 200), (caminho_recente[i-1][1]*TAMANHO_TILE, caminho_recente[i-1][0]*TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))

        # Desenha o mago na posição atual do caminho
        screen.blit(mago, (y * TAMANHO_TILE, x * TAMANHO_TILE))

        # Adicionando os png para portas e portal
        screen.blit(door1, (90, 576))
        screen.blit(door2, (702, 307))
        screen.blit(door3, (433, 18))
        screen.blit(portal, (126, 108))
        
        # Verificar se o jogador chegou à espada para remover imagem da espada
        if celula == ponto_espada:
            espada_coletada = True

        if espada_coletada:
            screen.blit(swordoff, (36, 18)) # Remove a espada da tela caso ela já tenha sido coletada

        else:
            screen.blit(sword, (36, 18)) # Adiciona a espada na tela caso ainda não tenha sido coletada

        # Desenhar a nova superfície na janela do Pygame
        screen.blit(screen, (0, 0))
        pygame.display.update()
        clock.tick(12)

# Essa função cria uma lista 2D, onde cada célula representa uma posição (linha, coluna) no terreno do jogo.
# Além de que ele adiciona a lista de vizinhos a cada celula e armazena sua posição e custo utilizando o terreno convertido
def criar_celulas(terreno_convertido):
    celulas = [[Celula((linha, coluna), CUSTO[terreno_convertido[linha][coluna]]) for coluna in range(COLUNAS)] for linha in range(LINHAS)]
    
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
    GRAMA: (140, 211, 70),
    AREIA: (196, 188, 148),
    FLORESTA: (1, 115, 53),
    MONTANHA: (82, 70, 44),
    AGUA: (45, 72, 181)
}

# Desenhar o terreno_convertido na tela
def desenhar_terreno():
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            # Define a cor da célula com base no valor de custo
            cor = cores_terreno[terreno_convertido[linha][coluna]]

            # Desenhar o tile na tela
            pygame.draw.rect(screen, cor, (coluna * TAMANHO_TILE, linha * TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))

destinos = [ponto_destino1, ponto_destino2, ponto_destino3]
partida = ponto_partida
total = 0

#Loop para realizar os testes com todos os destinos
while destinos:
    menor_custo = float('inf')
    melhor_caminho = None
    proximo_destino = None

    for i in destinos:
        celulas = criar_celulas(terreno_convertido)
        caminho, custo_total = algoritmo_a_estrela(celulas, partida, i)

        if custo_total < menor_custo:
            menor_custo = custo_total
            melhor_caminho = caminho
            proximo_destino = i

    desenhar_terreno()
    desenhar_caminho(melhor_caminho, espada_coletada)

    if proximo_destino == ponto_destino1:
        cavernas.cavernas(caverna1, 1)
        total = total + custo_total
        print("Custo total do percurso na Caverna 1: " + str(custo_total))

    elif proximo_destino == ponto_destino2:
        cavernas.cavernas(caverna2, 2)
        total = total + custo_total
        print("Custo total do percurso na Caverna 2: " + str(custo_total))

    elif proximo_destino == ponto_destino3:
        cavernas.cavernas(caverna3, 3)
        total = total + custo_total
        print("Custo total do percurso na Caverna 3: " + str(custo_total))

        # Adiciona o ponto de espada no final da lista, apos a ultima caverna ser acessada
        destinos.append(ponto_espada)
    
    elif proximo_destino == ponto_espada:
        # Adiciona a chegada ao final da lista assim que a espada é capturada
        total = total + custo_total
        print("Custo total do percurso até a Espada: " + str(custo_total))
        destinos.append(chegada)

    elif proximo_destino == chegada:
        # Adiciona a chegada ao final da lista assim que a espada é capturada
        total = total + custo_total
        print("Custo total do percurso até a Chegada: " + str(custo_total))

    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    partida = proximo_destino
    destinos.remove(proximo_destino)

print("Custo total de todo percurso: " + str(total))