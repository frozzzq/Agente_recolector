import random

FILAS = 5
COLUMNAS = 5
AGENTE = 'A'
elementos = ['.', 'P', 'X']
pesos = [0.70, 0.15, 0.15]

map = [[random.choices(elementos, weights=pesos)[0] for i in range(COLUMNAS)] for i in range(FILAS)]

for fila in map:
    print(fila)