class Barco:
    '''
        Clase para representar a un barco del juego.

        Attributes:
            id (int): Identificador único del barco.
            tipo (str): Nombre o tipo de barco (Portaviones, Crucero, Destructor, etc.).
            longitud (int): Número de casillas que ocupa el barco.
            x (int): Coordenada X inicial en el tablero.
            y (int): Coordenada Y inicial en el tablero.
            orientacion (str): Orientación del barco ('H' para horizontal, 'V' para vertical).
            vidas (int): Puntos de vida restantes del barco.
    '''
    def __init__(self, id: int, tipo: str, longitud: int, x: int, y: int, orientacion: str, vidas: int):
        '''
            Inicializa una instancia de Barco.

            Args:
                id (int): Identificador único del barco.
                tipo (str): Nombre o tipo de barco.
                longitud (int): Número de casillas que ocupa.
                x (int): Coordenada X de origen.
                y (int): Coordenada Y de origen.
                orientacion (str): Orientación ('H' o 'V').
                vidas (int): Puntos de vida iniciales.

            Returns:
                None
        '''
        self.id = id
        self.tipo = tipo
        self.longitud = longitud
        self.x = x
        self.y = y
        self.orientacion = orientacion
        self.vidas = vidas

    def asignar_posicion(self, x: int, y: int, orientacion: str):
        '''
            Asigna una nueva posición y orientación al barco.

            Args:
                x (int): Nueva coordenada X.
                y (int): Nueva coordenada Y.
                orientacion (str): Nueva orientación ('H' o 'V').

            Returns:
                None
        '''
        self.x = x
        self.y = y
        self.orientacion = orientacion

    @classmethod
    def crear_desde_diccionario(cls, datos: dict) -> 'Barco':
        '''
            Crea una instancia de Barco a partir de un diccionario de configuración.

            Args:
                datos (dict): Diccionario con los datos del barco.

            Returns:
                Barco: Nueva instancia de la clase Barco.
        '''
        return cls(
            id=datos["ID"],
            tipo=datos["Nombre"],
            longitud=datos["Longitud"],
            x=datos.get("X", 0),
            y=datos.get("Y", 0),
            orientacion=datos.get("Orientacion", 'H'),
            vidas=datos["Vidas"]
        )

    @classmethod
    def crear_flota(cls, lista_datos: list[dict]) -> list['Barco']:
        '''
            Crea una lista de instancias de Barco a partir de una lista de diccionarios.

            Args:
                lista_datos (list[dict]): Lista de diccionarios con la información de los barcos.

            Returns:
                list[Barco]: Lista de objetos Barco creados.
        '''
        return [cls.crear_desde_diccionario(datos) for datos in lista_datos]

