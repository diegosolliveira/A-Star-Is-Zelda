tipo_terreno = {
    "g": "GRAMA",
    "a": "AREIA",
    "f": "FLORESTA",
    "m": "MONTANHA",
    "w": "AGUA",
    "p": "PAREDE",
    "c": "CAMINHO"
}

terreno = []
caverna1 = []
caverna2 = []
caverna3 = []

with open("./Zelda/docs/terreno.txt", "r") as arquivo:
    mapa = arquivo.readlines()
    for linha in mapa:
        temp = []
        for caracter in linha:
            if caracter != '\n':
                temp.append(tipo_terreno[caracter])
        terreno.append(temp)

with open("./Zelda/docs/caverna1.txt", "r") as arquivo:
    mapa = arquivo.readlines()
    for linha in mapa:
        temp = []
        for caracter in linha:
            if caracter != '\n':
                temp.append(tipo_terreno[caracter])
        caverna1.append(temp)

with open("./Zelda/docs/caverna2.txt", "r") as arquivo:
    mapa = arquivo.readlines()
    for linha in mapa:
        temp = []
        for caracter in linha:
            if caracter != '\n':
                temp.append(tipo_terreno[caracter])
        caverna2.append(temp)

with open("./Zelda/docs/caverna3.txt", "r") as arquivo:
    mapa = arquivo.readlines()
    for linha in mapa:
        temp = []
        for caracter in linha:
            if caracter != '\n':
                temp.append(tipo_terreno[caracter])
        caverna3.append(temp)

def retorna_terreno():
    return terreno

def retorna_caverna1():
    return caverna1

def retorna_caverna2():
    return caverna2

def retorna_caverna3():
    return caverna3