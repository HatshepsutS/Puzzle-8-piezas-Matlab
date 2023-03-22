
from collections import deque

class Nodo:
    def __init__(self, estado, padre, movimiento, profundidad, piezas_correctas):
        self.estado = estado
        self.padre = padre
        self.movimiento = movimiento
        self.profundidad = profundidad
        self.piezas_correctas = piezas_correctas

    def mover(self, direccion):
        estado = list(self.estado)
        ind = estado.index(0)

        if direccion == "arriba":
            if ind not in [6, 7, 8]:
                temp = estado[ind + 3]
                estado[ind + 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:
                return None

        elif direccion == "abajo":
            if ind not in [0, 1, 2]:
                temp = estado[ind - 3]
                estado[ind - 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:
                return None

        elif direccion == "derecha":
            if ind not in [0, 3, 6]:
                temp = estado[ind - 1]
                estado[ind - 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:
                return None

        elif direccion == "izquierda":
            if ind not in [2, 5, 8]:
                temp = estado[ind + 1]
                estado[ind + 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:
                return None

    def encontrar_sucesores(self):
        sucesores = []
        sucesorN = self.mover("arriba")
        sucesorS = self.mover("abajo")
        sucesorE = self.mover("derecha")
        sucesorO = self.mover("izquierda")

        sucesores.append(Nodo(sucesorN, self, "arriba", self.profundidad + 1, calcular_heurisitica(sucesorN)))
        sucesores.append(Nodo(sucesorS, self, "abajo", self.profundidad + 1, calcular_heurisitica(sucesorS)))
        sucesores.append(Nodo(sucesorE, self, "derecha", self.profundidad + 1, calcular_heurisitica(sucesorE)))
        sucesores.append(Nodo(sucesorO, self, "izquierda", self.profundidad + 1, calcular_heurisitica(sucesorO)))

        sucesores = [nodo for nodo in sucesores if nodo.estado != None]

        return sucesores


    def encontrar_camino(self, inicial):
        camino = []
        nodo_actual = self
        while nodo_actual.profundidad >= 1:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

    def imprimir_nodo(self, archivo):
        renglon = 0
        for pieza in self.estado:
            if pieza == 0:
                archivo.write(" ")
            else:
                archivo.write(str(pieza))
            archivo.write(" ")
            renglon += 1
            if renglon == 3:
                archivo.write("\n")
                renglon = 0



def calcular_heurisitica(estado):
    correcto = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    valor_correcto = 0
    piezas_correctas = 0
    if estado:
        for valor_pieza, valor_correcto in zip(estado, correcto):
            if valor_pieza == valor_correcto:
                piezas_correctas += 1
            valor_correcto += 1
    return piezas_correctas


def dfs(inicial, meta, profundidad_max):
    visitados = set()
    frontera = deque()
    frontera.append(Nodo(inicial, None, None, 0, calcular_heurisitica(inicial)))

    with open("salida.txt", "w") as archivo_salida:  # abre el archivo de salida en modo de escritura
        archivo_salida.write("--- analizando por profundidad con limite de 6 ---\n\n")
        while frontera:
            nodo = frontera.pop()
            if nodo.estado not in visitados:
                visitados.add(nodo.estado)
                archivo_salida.write("\n")
                for pieza in nodo.estado:
                    if pieza == 0:
                        archivo_salida.write("  ")
                    else:
                        archivo_salida.write(str(pieza) + " ")
                    if (nodo.estado.index(pieza) + 1) % 3 == 0:
                        archivo_salida.write("\n")
            else:
                continue

            if nodo.estado == meta:
                camino = nodo.encontrar_camino(inicial)
                archivo_salida.write("\nEncontrado camino: ")
                for nodo_camino in camino:
                    archivo_salida.write(nodo_camino.movimiento + " ")
                archivo_salida.write("\n")
                return camino
            else:
                if profundidad_max > 0:
                    if nodo.profundidad < profundidad_max:
                        frontera.extend(nodo.encontrar_sucesores())
                else:
                    frontera.extend(nodo.encontrar_sucesores())



def main():
    estado_final = (1, 2, 3, 8, 0, 4, 7, 6, 5)
    estado_inicial = (2, 8, 3, 1, 6, 4, 7, 0, 5)
    # Abrir el archivo en modo de escritura
    with open("camino.txt", "w") as archivo:
        archivo.write("Estado Raiz:\n")
        (Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial))).imprimir_nodo(archivo)
        nodos_camino = dfs(estado_inicial, estado_final, 5)
    
        archivo.write('\n--- Imprimiendo camino optimo a la solución ---\n')
        for nodo in nodos_camino:
            archivo.write(str(nodo.movimiento) + "\n")
            nodo.imprimir_nodo(archivo)



if __name__ == "__main__":
    main()