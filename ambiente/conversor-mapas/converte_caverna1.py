def converte_caverna1(caverna1, converte_variavel):
    caverna1_convertido = []  # cria uma lista vazia que receberá o terreno convertido
    for linha in caverna1:  # para cada linha do terreno original
        linha_convertida = []  # cria uma lista vazia que receberá a linha convertida
        for item in linha:  # para cada item da linha
            linha_convertida.append(converte_variavel[item])  # adiciona o item convertido na nova linha
        caverna1_convertido .append(linha_convertida)  # adiciona a nova linha na lista do terreno convertido
    return caverna1_convertido   # retorna o terreno convertido
