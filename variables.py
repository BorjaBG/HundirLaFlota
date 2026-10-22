'''
    Módulo de variables globales y constantes del juego Hundir la Flota.
    
    Contiene:
        - Listados de configuración de barcos para jugador y máquina.
        - Constantes de reglas y dimensiones del juego.
        - Rutas a los recursos de audio y animaciones (assets).
        - Paleta de colores y dimensiones de la interfaz gráfica.
'''

barcos = [
    {"ID": 10, "Nombre": "Portaviones", "Longitud": 4, "Vidas": 4},
    {"ID": 11, "Nombre": "Crucero", "Longitud": 2, "Vidas": 2},
    {"ID": 12, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 13, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 14, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 15, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 16, "Nombre": "Crucero", "Longitud": 2, "Vidas": 2},
    {"ID": 17, "Nombre": "Crucero", "Longitud": 2, "Vidas": 2},
    {"ID": 18, "Nombre": "Acorazado", "Longitud": 3, "Vidas": 3},
    {"ID": 19, "Nombre": "Acorazado", "Longitud": 3, "Vidas": 3}
]

barcos_maquina = [
    {"ID": 10, "Nombre": "Portaviones", "Longitud": 4, "Vidas": 4},
    {"ID": 11, "Nombre": "Crucero", "Longitud": 2, "Vidas": 2},
    {"ID": 12, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 13, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 14, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 15, "Nombre": "Destructor", "Longitud": 1, "Vidas": 1},
    {"ID": 16, "Nombre": "Crucero", "Longitud": 2, "Vidas": 2},
    {"ID": 17, "Nombre": "Crucero", "Longitud": 2, "Vidas": 2},
    {"ID": 18, "Nombre": "Acorazado", "Longitud": 3, "Vidas": 3},
    {"ID": 19, "Nombre": "Acorazado", "Longitud": 3, "Vidas": 3}
]

# Configuración del tablero y reglas de juego
DIMENSION_TABLERO = 10
TOTAL_BARCOS = 10
TOTAL_CASILLAS_BARCOS = 20
TIEMPO_ESPERA_TURNO = 2000
MAX_INTENTOS_COLOCACION = 1000

# Rutas de audios
RUTA_VICTORIA_MP3 = "assets/victoria.mp3"
RUTA_DERROTA_MP3 = "assets/derrota.mp3"
RUTA_PORTAVIONES_MP3 = "assets/portaviones.mp3"
RUTA_ACORAZADO_MP3 = "assets/acorazado.mp3"
RUTA_CRUCERO_MP3 = "assets/crucero.mp3"
RUTA_DESTRUCTOR_MP3 = "assets/destructor.mp3"
RUTA_AGUA_MP3 = "assets/agua.mp3"
RUTA_BARCO_HUNDIDO_MP3 = "assets/barco_hundido.mp3"

# Rutas de imágenes y animaciones
RUTA_VICTORIA_GIF = "assets/victoria.gif"
RUTA_DERROTA_GIF = "assets/derrota.gif"

# Dimensiones y paleta de colores de la interfaz gráfica
VENTANA_ANCHO = 900
VENTANA_ALTO = 550
COLOR_FONDO_PRINCIPAL = "#1e293b"
COLOR_FONDO_SECUNDARIO = "#0f172a"
COLOR_BARRA_ESTADO = "#334155"
COLOR_AGUA_TABLERO = "#0284c7"
COLOR_BARCO_TABLERO = "#475569"
COLOR_IMPACTO = "#dc2626"
COLOR_AGUA_DISPARO = "#38bdf8"
COLOR_TEXTO_CLARO = "#f8fafc"
COLOR_TEXTO_MUTED = "#94a3b8"
COLOR_TEXTO_SECUNDARIO = "#cbd5e1"
COLOR_ENEMIGO = "#f43f5e"
COLOR_VICTORIA = "#4ade80"
COLOR_DERROTA = "#f87171"
COLOR_DERROTA_CRITICA = "#ef4444"
COLOR_ALERTA = "#fbbf24"
COLOR_TOCADO = "#facc15"
COLOR_RADAR_AGUA = "#64748b"
COLOR_BOTON_PRIMARIO_ACTIVO = "#0369a1"
COLOR_BOTON_SECUNDARIO_ACTIVO = "#475569"
COLOR_BLANCO = "#ffffff"
COLOR_NEGRO = "#000000"
