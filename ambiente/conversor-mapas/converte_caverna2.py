def converte_caverna2(caverna2, converte_variavel):
    caverna2_convertido = []  # cria uma lista vazia que receberá o terreno convertido
    for linha in caverna2:  # para cada linha do terreno original
        linha_convertida = []  # cria uma lista vazia que receberá a linha convertida
        for item in linha:  # para cada item da linha
            linha_convertida.append(converte_variavel[item])  # adiciona o item convertido na nova linha
        caverna2_convertido .append(linha_convertida)  # adiciona a nova linha na lista do terreno convertido
    return caverna2_convertido   # retorna o terreno convertido
