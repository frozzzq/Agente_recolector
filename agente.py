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

# ---------------------------------------------------------------
# DECISIONES (funcion del agente)
# ---------------------------------------------------------------
def decidir(percepcion):
    """Recibe la percepcion y regresa la accion a realizar."""
    pos = percepcion["posicion"]
    visitas[pos] = visitas.get(pos, 0) + 1          # memoria

    # Regla 1: si estoy sobre un paquete, lo recojo
    if percepcion["actual"] == "PAQUETE":
        return "RECOGER"

    # Regla 2: si hay un paquete en una celda de al lado, voy hacia el
    for d in DIRECCIONES:
        if percepcion[d.lower()] == "PAQUETE":
            return d

    # Regla 3 y 4: me muevo a una celda libre. Prefiero la que he
    # visitado menos veces (asi exploro y no me quedo dando vueltas)
    libres = [d for d in DIRECCIONES if percepcion[d.lower()] == "VACIA"]
    if libres:
        def veces_visitada(d):
            nueva = (pos[0] + CAMBIO[d][0], pos[1] + CAMBIO[d][1])
            return visitas.get(nueva, 0)
        return min(libres, key=veces_visitada)      # si empatan, gana el orden de DIRECCIONES

    # Regla 5: si estoy rodeado y no puedo moverme, me quedo quieto
    return "ESPERAR"


# ---------------------------------------------------------------
# ACCIONES (actuadores)
# ---------------------------------------------------------------
def actuar(accion):
    """Modifica el entorno o la posicion del agente."""
    global acciones
    acciones += 1
    f, c = posicion_agente

    if accion == "RECOGER":
        if entorno[f][c] == "P":
            entorno[f][c] = "."
            actualizar_rendimiento("RECOGER")

    elif accion in CAMBIO:
        nf = f + CAMBIO[accion][0]
        nc = c + CAMBIO[accion][1]
        destino = contenido(nf, nc)
        if destino == "FUERA_DEL_TABLERO":
            actualizar_rendimiento("FUERA")          # no se mueve
        elif destino == "OBSTACULO":
            actualizar_rendimiento("OBSTACULO")      # no se mueve
        else:
            posicion_agente[0] = nf
            posicion_agente[1] = nc
            actualizar_rendimiento("MOVER")


# ---------------------------------------------------------------
# MEDIDA DE RENDIMIENTO
# ---------------------------------------------------------------
def actualizar_rendimiento(evento):
    global puntuacion, movimientos, penalizaciones, paquetes_recogidos
    if evento == "RECOGER":
        puntuacion += 10
        paquetes_recogidos += 1
        if not quedan_paquetes():
            puntuacion += 20                         # bono por recoger todos
    elif evento == "MOVER":
        puntuacion -= 1
        movimientos += 1
    elif evento == "FUERA" or evento == "OBSTACULO":
        puntuacion -= 5
        penalizaciones += 1


# ---------------------------------------------------------------
# CICLO PRINCIPAL
# ---------------------------------------------------------------
def simular(numero):
    cargar_escenario(ESCENARIOS[numero])
    print("=== ESCENARIO", numero, "===")
    mostrar_entorno("inicio")
    while quedan_paquetes() and acciones < MAX_ACCIONES:
        percepcion = percibir()
        accion = decidir(percepcion)
        if accion == "ESPERAR":
            print("El agente no puede moverse, termina la simulacion.")
            break
        actuar(accion)
        mostrar_entorno(accion)
    return [numero, paquetes_recogidos, movimientos, penalizaciones, puntuacion]


resultados = []
for n in ESCENARIOS:
    resultados.append(simular(n))

print("=== RESULTADOS ===")
print("Escenario | Paquetes | Movimientos | Penalizaciones | Puntuacion")
for r in resultados:
    print(r[0], "|", r[1], "|", r[2], "|", r[3], "|", r[4])