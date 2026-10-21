from clases import barco
import random
import pygame

try:
    from clases.barco import Barco
    from clases.tablero import Tablero
except ImportError:
    from barco import Barco
    from tablero import Tablero

# 1. Inicializar el mixer ANTES de cargar cualquier sonido (con buffer de 512 para 0 delay)
if not pygame.mixer.get_init():
    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.init()

try:
    SONIDO_CRUCERO = pygame.mixer.Sound("assets/crucero.mp3")
except Exception:
    SONIDO_CRUCERO = None

try:
    SONIDO_PORTAVIONES = pygame.mixer.Sound("assets/portaviones.mp3")
except Exception:
    SONIDO_PORTAVIONES = None

try:
    SONIDO_ACORAZADO = pygame.mixer.Sound("assets/acorazado.mp3")
except Exception:
    SONIDO_ACORAZADO = None

try:
    SONIDO_DESTRUCTOR = pygame.mixer.Sound("assets/destructor.mp3")
except Exception:
    SONIDO_DESTRUCTOR = None

try:
    SONIDO_AGUA = pygame.mixer.Sound("assets/agua.mp3")
except Exception:
    SONIDO_AGUA = None


class Jugador:
    def __init__(self, nombre: str, barcos: list[Barco], es_maquina: bool = False):
        self.nombre = nombre
        self.barcos = barcos
        self.es_maquina = es_maquina
        self.tablero = Tablero.crear_tablero()
        self.mapa_barcos = {}
        self.barcos_hundidos = 0
        self.colocar_barcos_aleatoriamente()

    
    '''def colocar_barcos(self):
        for barco in self.barcos:
            #cont = 0
            x, y = barco.x, barco.y
            longitud = barco.longitud
            for _ in range(longitud):
                self.mapa_barcos[(x, y)] = barco

                if not self.es_maquina:
                    self.tablero[x][y] = 'B'
                if barco.orientacion == 'H':
                    y += 1
                else:
                    x += 1'''

    def colocar_barcos_aleatoriamente(self, dimension=10, max_intentos=1000):
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
            # Si ningún barco falló y tenemos las 20 casillas completas, terminamos con éxito
            if not hubo_fallo and len(self.mapa_barcos) == 20:
                break

    def disparar(self, rival: 'Jugador', coordenada_x: int = None, coordenada_y: int = None):
        if coordenada_x is None or coordenada_y is None:
            while True:
                coordenada_x = random.randint(0, 9)
                coordenada_y = random.randint(0, 9)

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

    '''def disparar(self, rival: 'Jugador'):
        bucle = True
        while bucle:
            disparo = True
            if not self.es_maquina:
                try:
                    coor_x = int(input("Introduzca la coordenada X a la que disparar:"))
                    coor_y = int(input("Introduzca la coordenada Y a la que disparar:"))
                except ValueError:
                    print("Error al introducir las coordenadas. Las coordenadas tienen que ser numeros entre 0 y 9")
                    continue

                if coor_x < 0 or coor_x > 9:
                    print("La coordenada X no puede ser menor a 0 ni mayor a 9")
                    disparo = False
                elif coor_y < 0 or coor_y > 9:
                    print("La coordenada Y no puede ser menor a 0 ni mayor a 9")
                    disparo = False
                elif rival.tablero[coor_x][coor_y] in ['D', 'X']:
                    disparo = False
                    print("Ya has disparado anteriormente a esa coordenada")
            else:
                coor_x = random.randint(0, 9)
                coor_y = random.randint(0, 9)
                #print("Dispara la maquina")
                if rival.tablero[coor_x][coor_y] in ['D', 'X']:
                    disparo = False  

            if disparo:
                vidas = 0
                bucle = False
                if (coor_x, coor_y) in rival.mapa_barcos:
                    barco = rival.mapa_barcos[(coor_x, coor_y)]
                    barco.vidas -= 1
                    vidas = barco.vidas
                    rival.tablero[coor_x][coor_y] = "X"
                else:
                    vidas = -1
                    rival.tablero[coor_x][coor_y] = "D"
                    
                print(f"X: {coor_x}\tY: {coor_y}")
                return vidas'''
