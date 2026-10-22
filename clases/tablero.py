try:
    from variables import DIMENSION_TABLERO
except ImportError:
    DIMENSION_TABLERO = 10


class Tablero:
    '''
        Clase para representar el tablero de juego.

        Attributes:
            id_jugador (int): Identificador del jugador propietario del tablero.
            dimension (int): Dimensión del tablero (número de filas y columnas).
            barcos (list): Lista de barcos asignados al tablero.
    '''
    def __init__(self, id: int, dimension: int, barcos):
        '''
            Inicializa una instancia de Tablero.

            Args:
                id (int): Identificador del jugador.
                dimension (int): Dimensión de la cuadrícula.
                barcos (list): Lista de barcos.

            Returns:
                None
        '''
        self.id_jugador = id
        self.dimension = dimension
        self.barcos = barcos

    @staticmethod
    def crear_tablero(dimension: int = DIMENSION_TABLERO):
        '''
            Crea e inicializa una matriz cuadrada con casillas de agua ('A').

            Args:
                dimension (int): Tamaño del tablero (por defecto DIMENSION_TABLERO).

            Returns:
                list[list[str]]: Matriz bidimensional inicializada con 'A'.
        '''
        return [["A" for _ in range(dimension)] for _ in range(dimension)]


