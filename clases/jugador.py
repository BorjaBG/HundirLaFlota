from clases import barco
import random
import pygame

try:
    from clases.barco import Barco
    from clases.tablero import Tablero
except ImportError:
    from barco import Barco
    from tablero import Tablero

try:
    from variables import (
        DIMENSION_TABLERO,
        TOTAL_CASILLAS_BARCOS,
        MAX_INTENTOS_COLOCACION,
        RUTA_CRUCERO_MP3,
        RUTA_PORTAVIONES_MP3,
        RUTA_ACORAZADO_MP3,
        RUTA_DESTRUCTOR_MP3,
        RUTA_AGUA_MP3,
    )
except ImportError:
    DIMENSION_TABLERO = 10
    TOTAL_CASILLAS_BARCOS = 20
    MAX_INTENTOS_COLOCACION = 1000
    RUTA_CRUCERO_MP3 = "assets/crucero.mp3"
    RUTA_PORTAVIONES_MP3 = "assets/portaviones.mp3"
    RUTA_ACORAZADO_MP3 = "assets/acorazado.mp3"
    RUTA_DESTRUCTOR_MP3 = "assets/destructor.mp3"
    RUTA_AGUA_MP3 = "assets/agua.mp3"

# 1. Inicializar el mixer ANTES de cargar cualquier sonido (con buffer de 512 para 0 delay)
if not pygame.mixer.get_init():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.init()

try:
    SONIDO_CRUCERO = pygame.mixer.Sound(RUTA_CRUCERO_MP3)
except Exception:
    SONIDO_CRUCERO = None

try:
    SONIDO_PORTAVIONES = pygame.mixer.Sound(RUTA_PORTAVIONES_MP3)
except Exception:
    SONIDO_PORTAVIONES = None

try:
    SONIDO_ACORAZADO = pygame.mixer.Sound(RUTA_ACORAZADO_MP3)
except Exception:
    SONIDO_ACORAZADO = None

try:
    SONIDO_DESTRUCTOR = pygame.mixer.Sound(RUTA_DESTRUCTOR_MP3)
except Exception:
    SONIDO_DESTRUCTOR = None

try:
    SONIDO_AGUA = pygame.mixer.Sound(RUTA_AGUA_MP3)
except Exception:
    SONIDO_AGUA = None


class Jugador:
    '''
        Clase para representar a un jugador.

        Attributes:
            nombre (str): Nombre del jugador.
            barcos (list[Barco]): Lista de barcos del jugador.
            es_maquina (bool): Indica si el jugador es la maquina.
            tablero (list[list[str]]): Tablero del jugador.
            mapa_barcos (dict): Diccionario con los barcos del jugador.
            barcos_hundidos (int): Numero de barcos hundidos.
    '''
    def __init__(self, nombre: str, barcos: list[Barco], es_maquina: bool = False):
        '''
            Inicializa un jugador.

            Args:
                nombre (str): Nombre del jugador.
                barcos (list[Barco]): Lista de barcos del jugador.
                es_maquina (bool): Indica si el jugador es la maquina.

            Returns:
                None
        '''
        self.nombre = nombre
        self.barcos = barcos
        self.es_maquina = es_maquina
        self.tablero = Tablero.crear_tablero()
        self.mapa_barcos = {}
        self.barcos_hundidos = 0
        self.colocar_barcos_aleatoriamente()

    def colocar_barcos_aleatoriamente(self, dimension=DIMENSION_TABLERO, max_intentos=MAX_INTENTOS_COLOCACION):
        '''
            Funcion para colocar los barcos de forma aleatoria en el tablero.
            Asigna una posicion y orientacion a cada barco.
            Si un barco no se puede colocar, se reinicia el tablero.

            Args:
                dimension (int): Dimension del tablero.
                max_intentos (int): Numero maximo de intentos para colocar los barcos.
            
            Returns:
                None
        '''
        while True:
            self.tablero = Tablero.crear_tablero()
            self.mapa_barcos = {}
            ocupado = [[False for _ in range(dimension + 2)] for _ in range(dimension + 2)]
            barcos_ordenados = sorted(self.barcos, key=lambda b: b.longitud, reverse=True)
            hubo_fallo = False
            for barco in barcos_ordenados:
                colocado = False
                intentos = 0
                while not colocado and intentos < max_intentos:
                    barco.orientacion = random.choice(['H', 'V'])
                    longitud = barco.longitud
                    if barco.orientacion == 'H':
                        x = random.randint(0, dimension - 1)
                        y = random.randint(0, dimension - longitud)
                    else:
                        x = random.randint(0, dimension - longitud)
                        y = random.randint(0, dimension - 1)
                    puede_colocar = True
                    for i in range(longitud):
                        cx, cy = (x, y + i) if barco.orientacion == 'H' else (x + i, y)
                        for dx in [-1, 0, 1]:
                            for dy in [-1, 0, 1]:
                                nx, ny = cx + dx, cy + dy
                                if 0 <= nx < dimension and 0 <= ny < dimension:
                                    if ocupado[nx + 1][ny + 1]:
                                        puede_colocar = False
                                        break
                            if not puede_colocar:
                                break
                        if not puede_colocar:
                            break
                    if puede_colocar:
                        barco.asignar_posicion(x, y, barco.orientacion)
                        for i in range(longitud):
                            cx, cy = (x, y + i) if barco.orientacion == 'H' else (x + i, y)
                            self.mapa_barcos[(cx, cy)] = barco

                            if not self.es_maquina:
                                self.tablero[cx][cy] = 'B'

                            for dx in [-1, 0, 1]:
                                for dy in [-1, 0, 1]:
                                    nx, ny = cx + dx, cy + dy
                                    if 0 <= nx < dimension and 0 <= ny < dimension:
                                        ocupado[nx + 1][ny + 1] = True
                        colocado = True
                    intentos += 1
                # Si este barco no pudo colocarse, abortamos el for para reiniciar el tablero entero
                if not colocado:
                    hubo_fallo = True
                    break
            # Si ningún barco falló y tenemos todas las casillas completas, terminamos con éxito
            if not hubo_fallo and len(self.mapa_barcos) == TOTAL_CASILLAS_BARCOS:
                break

    def disparar(self, rival: 'Jugador', coordenada_x: int = None, coordenada_y: int = None):
        '''
            Funcion para disparar a un barco.
            Args:
                rival (Jugador): Jugador rival.
                coordenada_x (int): Coordenada X del disparo.
                coordenada_y (int): Coordenada Y del disparo.
            
            Returns:
                tuple: Tupla con las coordenadas del disparo y el barco afectado.
        '''
        if coordenada_x is None or coordenada_y is None:
            while True:
                coordenada_x = random.randint(0, DIMENSION_TABLERO - 1)
                coordenada_y = random.randint(0, DIMENSION_TABLERO - 1)

                if rival.tablero[coordenada_x][coordenada_y] not in ['D', 'X']:
                    break

        if (coordenada_x, coordenada_y) in rival.mapa_barcos:
            barco = rival.mapa_barcos[(coordenada_x, coordenada_y)]
            if not self.es_maquina:
                match barco.tipo:
                    case "Portaviones":
                        SONIDO_PORTAVIONES.play()
                    case "Crucero":
                        SONIDO_CRUCERO.play()
                    case "Destructor":
                        SONIDO_DESTRUCTOR.play()
                    case "Acorazado":
                        SONIDO_ACORAZADO.play()

            barco.vidas -= 1
            rival.tablero[coordenada_x][coordenada_y] = 'X'

            if barco.vidas == 0:
                self.barcos_hundidos += 1

            return coordenada_x, coordenada_y, barco.vidas, barco
        else:
            if not self.es_maquina:
                SONIDO_AGUA.play()
            rival.tablero[coordenada_x][coordenada_y] = 'D'
            return coordenada_x, coordenada_y, -1, None
