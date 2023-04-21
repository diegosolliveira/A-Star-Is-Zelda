def converte_terreno(terreno, converte_variavel):
    terreno_convertido = []  # cria uma lista vazia que receberá o terreno convertido
    for linha in terreno:  # para cada linha do terreno original
        linha_convertida = []  # cria uma lista vazia que receberá a linha convertida
        for item in linha:  # para cada item da linha
            linha_convertida.append(converte_variavel[item])  # adiciona o item convertido na nova linha
        terreno_convertido.append(linha_convertida)  # adiciona a nova linha na lista do terreno convertido
    return terreno_convertido  # retorna o terreno convertido
