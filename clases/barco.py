class Barco:
    def __init__(self, id: int, tipo: str, longitud: int, x: int, y: int, orientacion: str, vidas: int):
        self.id = id
        self.tipo = tipo
        self.longitud = longitud
        self.x = x
        self.y = y
        self.orientacion = orientacion
        self.vidas = vidas

    def asignar_posicion(self, x: int, y: int, orientacion: str):
        self.x = x
        self.y = y
        self.orientacion = orientacion
