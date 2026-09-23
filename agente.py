#AGENTE RECOLECTOR

# ---------------------------------------------------------------
# ESCENARIOS (A = agente, P = paquete, X = obstaculo, . = libre)
# ---------------------------------------------------------------
ESCENARIOS = {
    1: """
. . . P .
. X . . .
A . . X P
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

MAX_ACCIONES = 50
DIRECCIONES = ["ARRIBA", "DERECHA", "ABAJO", "IZQUIERDA"] 
CAMBIO = {"ARRIBA": (-1, 0), "DERECHA": (0, 1), "ABAJO": (1, 0), "IZQUIERDA": (0, -1)}

entorno = []
posicion_agente = [0, 0]
puntuacion = 0
acciones = 0
movimientos = 0
penalizaciones = 0
paquetes_recogidos = 0
visitas = {}         

def cargar_escenario(texto):
    global entorno, posicion_agente, puntuacion, acciones, movimientos
    global penalizaciones, paquetes_recogidos, visitas
    entorno = [linea.split() for linea in texto.strip().split("\n")]
    for f in range(len(entorno)):
        for c in range(len(entorno[f])):
            if entorno[f][c] == "A":
                posicion_agente = [f, c]
                entorno[f][c] = "."    
    puntuacion = 0
    acciones = 0
    movimientos = 0
    penalizaciones = 0
    paquetes_recogidos = 0
    visitas = {}

def quedan_paquetes():
    for fila in entorno:
        if "P" in fila:
            return True
    return False

def mostrar_entorno(accion):
    print("Accion", acciones, "->", accion,
          "| posicion:", tuple(posicion_agente), "| puntuacion:", puntuacion)
    for f in range(len(entorno)):
        linea = ""
        for c in range(len(entorno[f])):
            if [f, c] == posicion_agente:
                linea += "A "
            else:
                linea += entorno[f][c] + " "
        print(linea)
    print()

def contenido(f, c):
    """Sensor de una celda: dice que hay en (f, c)."""
    if f < 0 or f >= len(entorno) or c < 0 or c >= len(entorno[0]):
        return "FUERA_DEL_TABLERO"
    if entorno[f][c] == "P":
        return "PAQUETE"
    if entorno[f][c] == "X":
        return "OBSTACULO"
    return "VACIA"


def percibir():
    """Obtiene lo que el agente puede sentir en este turno."""
    f, c = posicion_agente
    return {
        "posicion": (f, c),
        "actual": contenido(f, c),
        "arriba": contenido(f - 1, c),
        "abajo": contenido(f + 1, c),
        "izquierda": contenido(f, c - 1),
        "derecha": contenido(f, c + 1),
    }

