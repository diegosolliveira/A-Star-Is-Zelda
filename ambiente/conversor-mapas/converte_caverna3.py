def converte_caverna3(caverna3, converte_variavel):
    caverna3_convertido = []  # cria uma lista vazia que receberá o terreno convertido
    for linha in caverna3:  # para cada linha do terreno original
        linha_convertida = []  # cria uma lista vazia que receberá a linha convertida
        for item in linha:  # para cada item da linha
            linha_convertida.append(converte_variavel[item])  # adiciona o item convertido na nova linha
        caverna3_convertido .append(linha_convertida)  # adiciona a nova linha na lista do terreno convertido
    return caverna3_convertido   # retorna o terreno convertido
