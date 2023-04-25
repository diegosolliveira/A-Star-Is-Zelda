import pygame
import math
import sys
sys.path.append("./Zelda/functions")
import converte_terreno

# Definir as cores dos diferentes tipos de terreno
def cavernas(terreno, caverna):

    CAMINHO = (224, 224, 224)
    PAREDE = (139, 137, 137)

    converte_variavel = {
        "CAMINHO": CAMINHO,
        "PAREDE": PAREDE
    }

    # Definir o custo de cada tipo de terreno
    CUSTO = {
        CAMINHO: 10,
        PAREDE: 1000,
    }

    pygame.init()

    # Define as dimensões da tela e o tamanho dos tiles
    LARGURA_TELA = 756
    ALTURA_TELA = 756
    TAMANHO_TILE = 20

    # Criar a janela
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

    # Definir as dimensões da matriz do terreno
    LINHAS = 28
    COLUNAS = 28

    # Definir o terreno manualmente utilizando o arquivo para converter o terreno
    terreno_convertido = converte_terreno.converte_terreno(terreno, converte_variavel)

    # Adicionar as coordenadas do ponto de partida e destino das cavernas
    mago = pygame.image.load('./Zelda/icons/mago.png')
    
    if(caverna == 1):
        ponto_partida = (26, 14)
        ponto_destino = (3, 13)
        diamond = pygame.image.load('./Zelda/icons/diamond.png').convert()
        diamondoff = pygame.image.load('./Zelda/icons/diamondoff.png').convert()
        door = pygame.image.load('./Zelda/icons/doorcaverna.png').convert()
        posicao_diamond = (260, 61)
        posicao_door = ((281, 522))
    
    elif(caverna == 2):
        ponto_partida = (25, 13)
        ponto_destino = (2, 13)
        diamond = pygame.image.load('./Zelda/icons/diamond.png').convert()
        diamondoff = pygame.image.load('./Zelda/icons/diamondoff.png').convert()
        door = pygame.image.load('./Zelda/icons/doorcaverna.png').convert()
        posicao_diamond = (261, 42)
        posicao_door = ((261, 502))

    else:
        ponto_partida = (25, 14)
        ponto_destino = (19, 15)
        diamond = pygame.image.load('./Zelda/icons/diamond.png').convert()
        diamondoff = pygame.image.load('./Zelda/icons/diamondoff.png').convert()
        door = pygame.image.load('./Zelda/icons/doorcaverna.png').convert()
        posicao_diamond = (302, 383)
        posicao_door = ((281, 522))

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

    diamante_coletado = False

    def desenhar_caminho(caminho_recente, diamante_coletado):

        clock = pygame.time.Clock()
        # Desenhar o caminho na nova superfície
        for i, celula in enumerate(caminho_recente):
            x, y = celula

            # Para impedir que o "rastro" do mago fique salvo no caminho que ele já passou porem deixa uma cor um pouco diferente
            # para saber que ele percorreu aquele caminho
            if i > 0:
                pygame.draw.rect(screen, (224, 224, 200), (caminho_recente[i-1][1]*TAMANHO_TILE, caminho_recente[i-1][0]*TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))
           
            # Desenha o mago na posição atual do caminho
            screen.blit(mago, (y * TAMANHO_TILE, x * TAMANHO_TILE))

            # Verificar se o jogador chegou à espada para remover imagem da espada
            if celula == ponto_destino:
                diamante_coletado = True

            if diamante_coletado:
                screen.blit(diamondoff, posicao_diamond) # Remove a espada da tela caso ela já tenha sido coletada

            else:
                screen.blit(diamond, posicao_diamond) # Adiciona a espada na tela caso ainda não tenha sido coletada

            # Adicionando os png para a espada portas e portal
            screen.blit(door, posicao_door)

            # Desenhar a nova superfície na janela do Pygame
            screen.blit(screen, (0, 0))
            pygame.display.update()
            clock.tick(28)    

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
        CAMINHO: (224, 224, 224),
        PAREDE: (179, 179, 179),
    }

    # Desenhar o terreno_convertido na tela
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            # Define a cor da célula com base no valor de custo
            cor = cores_terreno[terreno_convertido[linha][coluna]]

            # Desenhar o tile na tela
            pygame.draw.rect(screen, cor, (coluna * TAMANHO_TILE, linha * TAMANHO_TILE, TAMANHO_TILE-1, TAMANHO_TILE-1))

    # Obter o caminho encontrado pelo algoritmo A*
    celulas = criar_celulas(terreno_convertido)
    caminho, custo_total = algoritmo_a_estrela(celulas, ponto_partida, ponto_destino)

    desenhar_caminho(caminho, diamante_coletado)
    caminho_inverso = caminho[::-1]
    desenhar_caminho(caminho_inverso, diamante_coletado)

    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
