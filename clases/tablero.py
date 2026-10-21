class Tablero:
    def __init__(self, id: int, dimension: int, barcos):
        self.id_jugador = id
        self.dimension = dimension
        self.barcos = barcos

    @staticmethod
    def crear_tablero():
        tablero = []
        for i in range(10):
            linea = []
            for j in range(10):
                linea.append("A")
            tablero.append(linea)
        return tablero
