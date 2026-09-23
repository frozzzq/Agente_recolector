#AGENTE RECOLECTOR

# ---------------------------------------------------------------
# ESCENARIOS (A = agente, P = paquete, X = obstaculo, . = libre)
# ---------------------------------------------------------------
ESCENARIOS = {
    1: """
A . . P .
. X . . .
. . . X P
. . P . .
. X . . .
""",
    2: """
P . X . .
. . X . P
. . A . .
X . . . .
P . X . .
""",
    3: """
. X . . P
. X . X .
. . A . .
P X . X .
. . . . P
""",
}

import random

FILAS = 5
COLUMNAS = 5
AGENTE = 'A'
elementos = ['.', 'P', 'X']
pesos = [0.70, 0.15, 0.15]

map = [[random.choices(elementos, weights=pesos)[0] for i in range(COLUMNAS)] for i in range(FILAS)]

for fila in map:
    print(fila)