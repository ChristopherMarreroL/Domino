import random
from queue import Queue

# Grafos para ordenar las fichas que se colocan en la mesa.
def find_odd_vertex(graph):
    odd_vertex = None
    for node, neighbors in graph.items():
        if odd_vertex is None:
            odd_vertex = node
        if len(neighbors) % 2 == 1:
            odd_vertex = node
            break
    return odd_vertex

def find_reachable_nodes(v, u, graph):
    if len(graph[v]) > 0:
        visited = set()
        queue = Queue()
        queue.put(v)
        visited.add(v)
        while not queue.empty():
            current_node = queue.get()
            for next_node in graph[current_node]:
                if next_node == u:
                    return True
                if next_node not in visited:
                    queue.put(next_node)
                    visited.add(next_node)
        return False
    else:
        return True

def get_graph(dominos):
    graph = {}
    for domino in dominos:
        a = domino[0]
        b = domino[1]
        if a not in graph.keys():
            graph[a] = [b]
        else:
            graph[a].append(b)
        if b not in graph.keys():
            graph[b] = [a]
        else:
            graph[b].append(a)
    return graph

def solve(dominos):
    graph = get_graph(dominos)
    number_of_nodes = len(dominos)
    start_node = find_odd_vertex(graph)
    v = start_node
    path = []
    for i in range(number_of_nodes):
        neighbors = graph[v]
        for u in neighbors:
            graph[v].remove(u)
            graph[u].remove(v)
            if find_reachable_nodes(v, u, graph):
                path.append((v, u))
                v = u
                break
            else:
                graph[v].append(u)
                graph[u].append(v)
    return path

def inicializar_fichas():
    # Crea una lista con todas las fichas posibles en el dominó
    fichas = [(i, j) for i in range(7) for j in range(i, 7)]
    # Baraja las fichas de manera aleatoria
    random.shuffle(fichas)
    return fichas

def repartir_fichas(fichas, num_jugadores):
    # Divide las fichas entre los jugadores y reparte una ficha para empezar la mesa
    manos = [fichas[i:i+7] for i in range(0, 7 * num_jugadores, 7)]
    mesa = []
    return manos, mesa

def imprimir_mesa(mesa):
    # Imprime el estado actual de la mesa
    print("Mesa:", solve(mesa))

def imprimir_jugador(nombre, fichas):
    # Imprime las fichas del jugador con sus respectivos números
    print(f"Fichas de {nombre}:")
    for i, ficha in enumerate(fichas, start=1):
        print(f"{i}: {ficha}")

def hay_ganador(jugador):
    return len(jugador) == 0

def es_jugada_valida(ficha, mesa):
    # Verifica si la ficha puede ser jugada en la mesa
    return len(mesa) == 0 or ficha[0] in mesa[-1] or ficha[1] in mesa[-1]

def obtener_nombres_jugadores(num_jugadores):
    # Solicita el nombre de cada jugador
    nombres = []
    for i in range(num_jugadores):
        nombre = input(f"Ingrese el nombre del Jugador {i + 1}: ")
        nombres.append(nombre)
    return nombres

def determinar_ganador_menos_fichas(jugadores):
    # Determina al ganador por tener menos fichas
    min_fichas = float('inf')
    ganador = None
    for jugador in jugadores:
        if len(jugador) < min_fichas:
            min_fichas = len(jugador)
            ganador = jugador
    return ganador

def main():
    # Solicita al usuario ingresar el número de jugadores (entre 2 y 4)
    num_jugadores = int(input("Ingresa el número de jugadores (entre 2 y 4): "))
    
    # Verifica que el número de jugadores sea válido
    if num_jugadores < 2 or num_jugadores > 4:
        print("Número de jugadores no válido. Elige un número entre 2 y 4.")
        return

    # Obtiene los nombres de los jugadores
    nombres_jugadores = obtener_nombres_jugadores(num_jugadores)

    # Inicializa las fichas y reparte entre los jugadores y la mesa
    fichas_disponibles = inicializar_fichas()
    jugadores, mesa = repartir_fichas(fichas_disponibles, num_jugadores)

    while True:
        # Itera a través de los jugadores para sus turnos
        for i in range(num_jugadores):
            nombre_jugador = nombres_jugadores[i]
            # Imprime la mesa y las fichas del jugador actual
            imprimir_mesa(mesa)
            imprimir_jugador(nombre_jugador, jugadores[i])

            # Turno del Jugador
            if len(mesa) == 0:
                # Si la mesa está vacía, el jugador debe colocar la primera ficha
                indice_ficha_jugador = int(input(f"Elige el número de la ficha que quieres jugar para iniciar la mesa, {nombre_jugador}: "))
                lado_jugador = "izquierda"
            else:
                # Si la mesa ya tiene fichas, el jugador sigue el turno normal
                indice_ficha_jugador = int(input(f"Elige el número de la ficha que quieres jugar (o 0 para pasar al próximo jugador), {nombre_jugador}: "))
                lado_jugador = input(f"¿En qué lado quieres jugar la ficha, {nombre_jugador}? (izquierda/derecha): ").lower()

            while True:
                if indice_ficha_jugador == 0:
                    print(f"{nombre_jugador} pasa al siguiente jugador.")
                    break
                elif 0 < indice_ficha_jugador <= len(jugadores[i]):

                    # Jugar una ficha y añadirla a la mesa si es válida
                    ficha_jugada = jugadores[i].pop(indice_ficha_jugador - 1)

                    if lado_jugador == "izquierda":
                        if es_jugada_valida(ficha_jugada, mesa):
                            mesa.insert(0, ficha_jugada)
                            print(f"Has jugado la ficha {ficha_jugada} en la izquierda.")
                            break
                        else:
                            print("Ladrón, esa ficha no va.")
                            jugadores[i].append(ficha_jugada)
                    elif lado_jugador == "derecha":
                        if es_jugada_valida(ficha_jugada, mesa):
                            mesa.append(ficha_jugada)
                            print(f"Has jugado la ficha {ficha_jugada} en la derecha.")
                            break
                        else:
                            print("Ladrón, esa ficha no va.")
                            print("Mesa:", mesa)
                            jugadores[i].append(ficha_jugada)
                    else:
                        print("Opción no válida. Introduce 'izquierda' o 'derecha'.")

                else:
                    print("Opción no válida. Intenta de nuevo.")

                # Si llega a este punto, es porque la jugada no fue válida y debe volver a preguntar
                indice_ficha_jugador = int(input(f"Elige el número de la ficha que quieres jugar, {nombre_jugador}: "))
                if indice_ficha_jugador != 0:
                    lado_jugador = input(f"¿En qué lado quieres jugar la ficha, {nombre_jugador}? (izquierda/derecha): ").lower()

            # Verificar si el jugador ha ganado
            if hay_ganador(jugadores[i]):
                print(f"{nombre_jugador} has hecho DOMINOOOOO ¡Felicidades!")
                return

            # Verificar si hay un ganador general o empate
            if len(fichas_disponibles) == 0 and all(len(jugador) == 0 for jugador in jugadores):
                print("¡El juego ha terminado en empate!")
                return

        # Verificar si el juego está trancao
        if all(not es_jugada_valida(ficha, mesa) for jugador in jugadores for ficha in jugador):
            # El juego está bloqueado, determinar al ganador por tener menos fichas
            ganador_menos_fichas = determinar_ganador_menos_fichas(jugadores)
            print("El juego está trancao")
            print(f"El ganador por tener menos fichas es: {ganador_menos_fichas}")
            return

if __name__ == "__main__":
    main()