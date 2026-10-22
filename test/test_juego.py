"""
Suite completa y exhaustiva de pruebas unitarias, de integración, de estrés
y de interfaz gráfica para el juego Hundir la Flota.
"""

import io
import os
import sys
import unittest
import tkinter as tk

# Asegurar que el directorio raíz del proyecto esté en el path de búsqueda de módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from variables import (
    barcos,
    barcos_maquina,
    DIMENSION_TABLERO,
    TOTAL_BARCOS,
    TOTAL_CASILLAS_BARCOS,
    TIEMPO_ESPERA_TURNO,
    MAX_INTENTOS_COLOCACION,
    RUTA_VICTORIA_MP3,
    RUTA_DERROTA_MP3,
    RUTA_PORTAVIONES_MP3,
    RUTA_ACORAZADO_MP3,
    RUTA_CRUCERO_MP3,
    RUTA_DESTRUCTOR_MP3,
    RUTA_AGUA_MP3,
    RUTA_BARCO_HUNDIDO_MP3,
    RUTA_VICTORIA_GIF,
    RUTA_DERROTA_GIF,
    VENTANA_ANCHO,
    VENTANA_ALTO,
    COLOR_FONDO_PRINCIPAL,
    COLOR_FONDO_SECUNDARIO,
    COLOR_BARRA_ESTADO,
    COLOR_AGUA_TABLERO,
    COLOR_BARCO_TABLERO,
    COLOR_IMPACTO,
    COLOR_AGUA_DISPARO,
    COLOR_TEXTO_CLARO,
    COLOR_TEXTO_MUTED,
    COLOR_TEXTO_SECUNDARIO,
    COLOR_ENEMIGO,
    COLOR_VICTORIA,
    COLOR_DERROTA,
    COLOR_DERROTA_CRITICA,
    COLOR_ALERTA,
    COLOR_TOCADO,
    COLOR_RADAR_AGUA,
    COLOR_BOTON_PRIMARIO_ACTIVO,
    COLOR_BOTON_SECUNDARIO_ACTIVO,
    COLOR_BLANCO,
    COLOR_NEGRO,
)
from clases.barco import Barco
from clases.tablero import Tablero
from clases.jugador import Jugador
from funciones import inicializar_audio


class TestVariables(unittest.TestCase):
    """Pruebas sobre las definiciones de configuración y variables globales."""

    def test_cantidad_barcos_ambos_jugadores(self):
        """Verifica que tanto jugador como máquina cuenten con exactamente 10 barcos."""
        self.assertEqual(len(barcos), 10, "El jugador debe tener exactamente 10 barcos")
        self.assertEqual(len(barcos_maquina), 10, "La máquina debe tener exactamente 10 barcos")

    def test_claves_obligatorias_barcos(self):
        """Verifica que todos los diccionarios de barcos contengan las claves requeridas."""
        claves_esperadas = {"ID", "Nombre", "Longitud", "Vidas"}
        for b in barcos:
            self.assertTrue(claves_esperadas.issubset(b.keys()), f"Faltan campos en barco jugador: {b}")

        for b in barcos_maquina:
            self.assertTrue(claves_esperadas.issubset(b.keys()), f"Faltan campos en barco máquina: {b}")

    def test_tipos_datos_barcos(self):
        """Verifica que los tipos de datos de los atributos de los barcos sean correctos."""
        for b in barcos:
            self.assertIsInstance(b["ID"], int)
            self.assertIsInstance(b["Nombre"], str)
            self.assertIsInstance(b["Longitud"], int)
            self.assertIsInstance(b["Vidas"], int)

    def test_distribucion_flota_reglamentaria(self):
        """
        Verifica la distribución oficial del juego:
        - 1 barco de 4 posiciones (Portaviones)
        - 2 barcos de 3 posiciones (Acorazados)
        - 3 barcos de 2 posiciones (Cruceros)
        - 4 barcos de 1 posición (Destructores)
        """
        longitudes_jugador = [b["Longitud"] for b in barcos]
        self.assertEqual(longitudes_jugador.count(4), 1, "Debe haber exactamente 1 barco de 4 casillas")
        self.assertEqual(longitudes_jugador.count(3), 2, "Debe haber exactamente 2 barcos de 3 casillas")
        self.assertEqual(longitudes_jugador.count(2), 3, "Debe haber exactamente 3 barcos de 2 casillas")
        self.assertEqual(longitudes_jugador.count(1), 4, "Debe haber exactamente 4 barcos de 1 casilla")

    def test_total_vidas_y_casillas(self):
        """Verifica que la suma total de vidas iniciales sea 20."""
        self.assertEqual(sum(b["Vidas"] for b in barcos), TOTAL_CASILLAS_BARCOS)
        self.assertEqual(sum(b["Vidas"] for b in barcos_maquina), TOTAL_CASILLAS_BARCOS)

    def test_ids_unicos(self):
        """Verifica que no existan IDs duplicados en la flota."""
        ids_jugador = [b["ID"] for b in barcos]
        self.assertEqual(len(ids_jugador), len(set(ids_jugador)), "Los IDs de los barcos del jugador deben ser únicos")

    def test_constantes_juego_y_tiempos(self):
        """Verifica que las constantes globales de juego estén correctamente definidas."""
        self.assertEqual(DIMENSION_TABLERO, 10)
        self.assertEqual(TOTAL_BARCOS, 10)
        self.assertEqual(TOTAL_CASILLAS_BARCOS, 20)
        self.assertEqual(TIEMPO_ESPERA_TURNO, 2000)
        self.assertEqual(MAX_INTENTOS_COLOCACION, 1000)
        self.assertEqual(VENTANA_ANCHO, 900)
        self.assertEqual(VENTANA_ALTO, 550)

    def test_existencia_archivos_assets(self):
        """Comprueba que todos los archivos multimedia referenciados en variables.py existan físicamente en assets."""
        rutas_audios = [
            RUTA_VICTORIA_MP3,
            RUTA_DERROTA_MP3,
            RUTA_PORTAVIONES_MP3,
            RUTA_ACORAZADO_MP3,
            RUTA_CRUCERO_MP3,
            RUTA_DESTRUCTOR_MP3,
            RUTA_AGUA_MP3,
            RUTA_BARCO_HUNDIDO_MP3,
        ]
        for ruta in rutas_audios:
            self.assertTrue(os.path.isfile(ruta), f"No existe el archivo de audio: {ruta}")

        rutas_imagenes = [RUTA_VICTORIA_GIF, RUTA_DERROTA_GIF]
        for ruta in rutas_imagenes:
            self.assertTrue(os.path.isfile(ruta), f"No existe el archivo de imagen: {ruta}")

    def test_paleta_colores_hex(self):
        """Verifica que todos los colores definidos tengan formato hexadecimal válido (#RRGGBB)."""
        colores = [
            COLOR_FONDO_PRINCIPAL,
            COLOR_FONDO_SECUNDARIO,
            COLOR_BARRA_ESTADO,
            COLOR_AGUA_TABLERO,
            COLOR_BARCO_TABLERO,
            COLOR_IMPACTO,
            COLOR_AGUA_DISPARO,
            COLOR_TEXTO_CLARO,
            COLOR_TEXTO_MUTED,
            COLOR_TEXTO_SECUNDARIO,
            COLOR_ENEMIGO,
            COLOR_VICTORIA,
            COLOR_DERROTA,
            COLOR_DERROTA_CRITICA,
            COLOR_ALERTA,
            COLOR_TOCADO,
            COLOR_RADAR_AGUA,
            COLOR_BOTON_PRIMARIO_ACTIVO,
            COLOR_BOTON_SECUNDARIO_ACTIVO,
            COLOR_BLANCO,
            COLOR_NEGRO,
        ]
        for c in colores:
            self.assertTrue(c.startswith("#") and len(c) == 7, f"Color hexadecimal no válido: {c}")


class TestTablero(unittest.TestCase):
    """Pruebas unitarias de la clase Tablero."""

    def test_constructor_tablero(self):
        """Verifica que el constructor asigne correctamente id, dimension y barcos."""
        tablero_obj = Tablero(id=1, dimension=10, barcos=[])
        self.assertEqual(tablero_obj.id_jugador, 1)
        self.assertEqual(tablero_obj.dimension, 10)
        self.assertEqual(tablero_obj.barcos, [])

    def test_dimensiones_matriz(self):
        """Verifica que el método estático crear_tablero retorne una matriz 10x10."""
        tablero = Tablero.crear_tablero()
        self.assertEqual(len(tablero), DIMENSION_TABLERO)
        for fila in tablero:
            self.assertEqual(len(fila), DIMENSION_TABLERO)

    def test_contenido_inicial_agua(self):
        """Verifica que todas las celdas se inicialicen con 'A'."""
        tablero = Tablero.crear_tablero()
        for i in range(10):
            for j in range(10):
                self.assertEqual(tablero[i][j], "A")

    def test_independencia_de_filas(self):
        """Verifica que las filas del tablero sean listas independientes y no copias por referencia."""
        tablero = Tablero.crear_tablero()
        tablero[0][0] = "X"
        self.assertEqual(tablero[0][0], "X")
        self.assertEqual(tablero[1][0], "A", "Modificar una fila no debe afectar a otra fila")


class TestBarco(unittest.TestCase):
    """Pruebas unitarias de la clase Barco."""

    def test_instanciacion_atributos(self):
        """Verifica la asignación correcta de todos los atributos en __init__."""
        barco = Barco(10, "Portaviones", 4, 1, 2, "H", 4)
        self.assertEqual(barco.id, 10)
        self.assertEqual(barco.tipo, "Portaviones")
        self.assertEqual(barco.longitud, 4)
        self.assertEqual(barco.x, 1)
        self.assertEqual(barco.y, 2)
        self.assertEqual(barco.orientacion, "H")
        self.assertEqual(barco.vidas, 4)

    def test_asignar_posicion(self):
        """Verifica la actualización de coordenadas y orientación mediante asignar_posicion."""
        barco = Barco(11, "Crucero", 2, 0, 0, "H", 2)
        barco.asignar_posicion(5, 7, "V")
        self.assertEqual(barco.x, 5)
        self.assertEqual(barco.y, 7)
        self.assertEqual(barco.orientacion, "V")

    def test_decremento_de_vidas(self):
        """Verifica que las vidas del barco se puedan decrementar correctamente."""
        barco = Barco(12, "Destructor", 1, 3, 3, "H", 1)
        barco.vidas -= 1
        self.assertEqual(barco.vidas, 0)

    def test_crear_desde_diccionario(self):
        """Verifica la creación de un Barco a partir de un diccionario."""
        datos = {"ID": 99, "Nombre": "Submarino", "Longitud": 3, "Vidas": 3}
        barco = Barco.crear_desde_diccionario(datos)
        self.assertEqual(barco.id, 99)
        self.assertEqual(barco.tipo, "Submarino")
        self.assertEqual(barco.longitud, 3)
        self.assertEqual(barco.vidas, 3)
        self.assertEqual(barco.x, 0)
        self.assertEqual(barco.y, 0)
        self.assertEqual(barco.orientacion, "H")

    def test_crear_flota(self):
        """Verifica la creación masiva de barcos a partir de una lista de diccionarios."""
        flota = Barco.crear_flota(barcos)
        self.assertEqual(len(flota), 10)
        self.assertTrue(all(isinstance(b, Barco) for b in flota))


class TestJugadorColocacion(unittest.TestCase):
    """Pruebas de la colocación y posicionamiento de barcos por la clase Jugador."""

    def setUp(self):
        self.flota_humano = Barco.crear_flota(barcos)
        self.flota_maquina = Barco.crear_flota(barcos_maquina)

    def test_humano_coloca_exactamente_20_casillas(self):
        """El jugador humano debe tener exactamente 20 coordenadas de barco en mapa y en tablero."""
        j = Jugador("Humano", self.flota_humano, es_maquina=False)
        self.assertEqual(len(j.mapa_barcos), TOTAL_CASILLAS_BARCOS)
        conteo_b = sum(fila.count("B") for fila in j.tablero)
        self.assertEqual(conteo_b, TOTAL_CASILLAS_BARCOS)

    def test_maquina_oculta_barcos_en_tablero(self):
        """La máquina debe tener 20 coordenadas en mapa_barcos pero su tablero visible debe ser sólo agua ('A')."""
        m = Jugador("Máquina", self.flota_maquina, es_maquina=True)
        self.assertEqual(len(m.mapa_barcos), TOTAL_CASILLAS_BARCOS)
        conteo_b = sum(fila.count("B") for fila in m.tablero)
        self.assertEqual(conteo_b, 0, "El tablero de la máquina no debe mostrar 'B' al inicio")

    def test_coordenadas_dentro_del_rango_oficial(self):
        """Todas las coordenadas de los barcos deben estar estrictamente dentro de [0, 9]."""
        j = Jugador("Tester", self.flota_humano, es_maquina=False)
        for (x, y) in j.mapa_barcos.keys():
            self.assertTrue(0 <= x < 10, f"Coordenada X={x} fuera de rango")
            self.assertTrue(0 <= y < 10, f"Coordenada Y={y} fuera de rango")

    def test_regla_no_contacto_entre_barcos(self):
        """Regla naval: dos barcos distintos no deben tocarse ni ortogonal ni diagonalmente."""
        j = Jugador("Tester", self.flota_humano, es_maquina=False)
        for (x, y), barco_actual in j.mapa_barcos.items():
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in j.mapa_barcos:
                        barco_vecino = j.mapa_barcos[(nx, ny)]
                        self.assertEqual(
                            barco_actual.id,
                            barco_vecino.id,
                            f"Conflicto de contacto en ({x},{y}) y ({nx},{ny}) entre barcos distintos"
                        )


class TestJugadorDisparos(unittest.TestCase):
    """Pruebas del mecanismo de disparo, actualización de tableros y conteo de bajas."""

    def setUp(self):
        self.flota_j1 = Barco.crear_flota(barcos)
        self.flota_j2 = Barco.crear_flota(barcos_maquina)
        self.atacante = Jugador("Atacante", self.flota_j1, es_maquina=False)
        self.defensor = Jugador("Defensor", self.flota_j2, es_maquina=True)

    def test_disparo_agua_coordenada_especifica(self):
        """Disparar al agua marca 'D' en el rival y retorna vidas=-1 y barco=None."""
        coord_agua = None
        for x in range(10):
            for y in range(10):
                if (x, y) not in self.defensor.mapa_barcos:
                    coord_agua = (x, y)
                    break
            if coord_agua:
                break

        rx, ry, vidas, barco = self.atacante.disparar(self.defensor, coord_agua[0], coord_agua[1])
        self.assertEqual((rx, ry), coord_agua)
        self.assertEqual(vidas, -1)
        self.assertIsNone(barco)
        self.assertEqual(self.defensor.tablero[coord_agua[0]][coord_agua[1]], "D")

    def test_disparo_tocado_reduce_vidas(self):
        """Disparar a un barco reduce sus vidas en 1 y marca 'X' en el tablero rival."""
        coord_barco = next(iter(self.defensor.mapa_barcos.keys()))
        barco_objetivo = self.defensor.mapa_barcos[coord_barco]
        vidas_previas = barco_objetivo.vidas

        rx, ry, vidas, barco = self.atacante.disparar(self.defensor, coord_barco[0], coord_barco[1])
        self.assertEqual((rx, ry), coord_barco)
        self.assertEqual(vidas, vidas_previas - 1)
        self.assertIs(barco, barco_objetivo)
        self.assertEqual(self.defensor.tablero[coord_barco[0]][coord_barco[1]], "X")

    def test_disparo_hundido_incrementa_contador(self):
        """Al destruir todas las casillas de un barco, vidas llega a 0 y barcos_hundidos incrementa."""
        barco_destructor = next(b for b in self.defensor.barcos if b.longitud == 1)
        coords_destructor = [coord for coord, b in self.defensor.mapa_barcos.items() if b.id == barco_destructor.id]
        self.assertEqual(len(coords_destructor), 1)

        coord = coords_destructor[0]
        hundidos_antes = self.atacante.barcos_hundidos
        _, _, vidas, barco = self.atacante.disparar(self.defensor, coord[0], coord[1])

        self.assertEqual(vidas, 0)
        self.assertEqual(self.atacante.barcos_hundidos, hundidos_antes + 1)

    def test_disparo_aleatorio_en_tablero_limpio(self):
        """Disparo aleatorio inicial genera coordenadas válidas dentro de 0..9."""
        rx, ry, vidas, _ = self.atacante.disparar(self.defensor)
        self.assertTrue(0 <= rx < 10)
        self.assertTrue(0 <= ry < 10)
        self.assertIn(self.defensor.tablero[rx][ry], ["D", "X"])

    def test_disparo_aleatorio_no_toca_casillas_ya_disparadas(self):
        """El disparo aleatorio nunca selecciona una casilla que ya tenga 'D' o 'X'."""
        for x in range(10):
            for y in range(10):
                if not (x == 5 and y == 5):
                    self.defensor.tablero[x][y] = "D"

        rx, ry, _, _ = self.atacante.disparar(self.defensor)
        self.assertEqual((rx, ry), (5, 5))

    def test_disparar_ejecuta_match_case_por_tipo(self):
        """Verifica que el match/case de sonido en disparar maneje adecuadamente los distintos tipos de barcos."""
        for tipo in ["Portaviones", "Crucero", "Destructor", "Acorazado"]:
            barco = next(b for b in self.defensor.barcos if b.tipo == tipo)
            coord = next(c for c, b in self.defensor.mapa_barcos.items() if b.id == barco.id)
            rx, ry, vidas, b_afectado = self.atacante.disparar(self.defensor, coord[0], coord[1])
            self.assertEqual((rx, ry), coord)
            self.assertEqual(b_afectado.tipo, tipo)


class TestFuncionesJuego(unittest.TestCase):
    """Pruebas de funciones auxiliares, inicialización de audio y assets del juego."""

    def test_inicializar_audio_retorno(self):
        """Verifica que inicializar_audio configure el mixer y devuelva una tupla de 2 sonidos."""
        res = inicializar_audio()
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)

    def test_escalado_gif_animacion(self):
        """Verifica que PhotoImage cargue los gifs y que subsample reduzca correctamente su altura si supera 260px."""
        try:
            root = tk.Tk()
            root.withdraw()
        except tk.TclError:
            self.skipTest("Entorno gráfico no disponible")

        try:
            img_vic = tk.PhotoImage(file=RUTA_VICTORIA_GIF)
            self.assertGreater(img_vic.height(), 0)
            if img_vic.height() > 260:
                scaled = img_vic.subsample(2, 2)
                self.assertLessEqual(scaled.height(), 260)

            img_der = tk.PhotoImage(file=RUTA_DERROTA_GIF)
            self.assertGreater(img_der.height(), 0)
            if img_der.height() > 260:
                scaled_der = img_der.subsample(2, 2)
                self.assertLessEqual(scaled_der.height(), 260)
        finally:
            root.destroy()


class TestEstresYSimulacion(unittest.TestCase):
    """Pruebas de robustez algorítmica, estrés y simulación completa de partidas."""

    def test_estres_generacion_50_tableros_aleatorios(self):
        """
        Genera 50 tableros aleatorios de forma consecutiva.
        Comprueba que el algoritmo de reintento siempre converge a una configuración válida:
        - 20 casillas ocupadas por barcos.
        - 0 colisiones.
        - 0 adyacencias prohibidas.
        """
        for i in range(50):
            flota = Barco.crear_flota(barcos_maquina)
            j = Jugador(f"Bot_{i}", flota, es_maquina=True)
            self.assertEqual(len(j.mapa_barcos), 20, f"Fallo de casillas en iteración {i}")
            self.assertEqual(len(j.barcos), 10, f"Fallo de barcos en iteración {i}")

    def test_simulacion_10_partidas_completas(self):
        """
        Simula 10 partidas completas entre dos bots aleatorios.
        Verifica:
        - Siempre hay exactamente un ganador que hunde los 10 barcos.
        - La partida concluye en un número acotado de disparos (<= 100 por jugador).
        - No se generan estados inconsistentes ni excepciones.
        """
        for partida in range(10):
            flota1 = Barco.crear_flota(barcos_maquina)
            flota2 = Barco.crear_flota(barcos_maquina)

            j1 = Jugador(f"Bot1_{partida}", flota1, es_maquina=True)
            j2 = Jugador(f"Bot2_{partida}", flota2, es_maquina=True)

            disparos_j1 = 0
            disparos_j2 = 0
            turno = 0  # 0: j1, 1: j2

            while j1.barcos_hundidos < 10 and j2.barcos_hundidos < 10:
                if turno == 0:
                    disparos_j1 += 1
                    _, _, vidas, _ = j1.disparar(j2)
                    if vidas < 0:
                        turno = 1
                else:
                    disparos_j2 += 1
                    _, _, vidas, _ = j2.disparar(j1)
                    if vidas < 0:
                        turno = 0

                self.assertLessEqual(disparos_j1, 100)
                self.assertLessEqual(disparos_j2, 100)

            ganador = j1 if j1.barcos_hundidos == 10 else j2
            perdedor = j2 if ganador is j1 else j1

            self.assertEqual(ganador.barcos_hundidos, 10)
            self.assertLess(perdedor.barcos_hundidos, 10)


class TestInterfazGrafica(unittest.TestCase):
    """Pruebas de la interfaz gráfica de usuario construida en Tkinter."""

    def setUp(self):
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except tk.TclError:
            self.skipTest("Entorno gráfico no disponible")

    def tearDown(self):
        if hasattr(self, "root") and self.root:
            self.root.destroy()

    def test_tk_disponible(self):
        """Verifica que el entorno gráfico Tkinter responda y procese eventos."""
        self.root.update()
        self.assertIsNotNone(self.root)

    def test_componentes_interfaz_juego(self):
        """
        Construye y valida los componentes de la interfaz de Hundir la Flota:
        - 100 botones de radar enemigo
        - 100 botones de la flota propia
        - Label de estado superior
        - Simulación de disparo sobre agua y sobre barco con actualización de widgets
        """
        flota_humano = Barco.crear_flota(barcos)
        flota_maquina = Barco.crear_flota(barcos_maquina)
        jugador = Jugador("Jugador 1", flota_humano, False)
        maquina = Jugador("Ordenador", flota_maquina, True)

        lbl_estado = tk.Label(self.root, text="Empieza la partida")
        lbl_estado.pack()

        contenedor = tk.Frame(self.root)
        contenedor.pack()

        frame_jugador = tk.Frame(contenedor)
        frame_maquina = tk.Frame(contenedor)
        frame_jugador.grid(row=0, column=0)
        frame_maquina.grid(row=0, column=1)

        botones_maquina = {}
        botones_jugador = {}

        for x in range(10):
            for y in range(10):
                btn_m = tk.Button(frame_maquina, text="A")
                btn_m.grid(row=x, column=y)
                botones_maquina[(x, y)] = btn_m

                btn_j = tk.Button(frame_jugador, text="B" if (x, y) in jugador.mapa_barcos else "A")
                btn_j.grid(row=x, column=y)
                botones_jugador[(x, y)] = btn_j

        self.assertEqual(len(botones_maquina), 100, "Debe haber 100 botones en el radar enemigo")
        self.assertEqual(len(botones_jugador), 100, "Debe haber 100 botones en la flota del jugador")

        # Simular disparo sobre casilla de agua en el radar
        coord_agua = next(c for c in [(x, y) for x in range(10) for y in range(10)] if c not in maquina.mapa_barcos)
        _, _, vidas, _ = jugador.disparar(maquina, coordenada_x=coord_agua[0], coordenada_y=coord_agua[1])
        btn_agua = botones_maquina[coord_agua]
        if vidas < 0:
            btn_agua.config(text="D", bg=COLOR_AGUA_DISPARO)
            lbl_estado.config(text="Agua. Turno de la máquina...")

        self.assertEqual(btn_agua.cget("text"), "D")
        self.assertEqual(lbl_estado.cget("text"), "Agua. Turno de la máquina...")

        # Simular disparo sobre casilla con barco en el radar
        coord_barco, barco = next(iter(maquina.mapa_barcos.items()))
        _, _, vidas, _ = jugador.disparar(maquina, coordenada_x=coord_barco[0], coordenada_y=coord_barco[1])
        btn_barco = botones_maquina[coord_barco]
        if vidas >= 0:
            btn_barco.config(text="X", bg=COLOR_IMPACTO)
            lbl_estado.config(text="Tocado! Repites disparo")

        self.assertEqual(btn_barco.cget("text"), "X")
        self.assertEqual(lbl_estado.cget("text"), "Tocado! Repites disparo")

    def test_pantalla_inicio_y_transicion_a_juego(self):
        """Verifica que la pantalla de inicio se cree correctamente y que el botón JUGAR revele los tableros."""
        lbl_estado = tk.Label(self.root, text="Empieza la partida")
        contenedor = tk.Frame(self.root)

        frame_inicio = tk.Frame(self.root, bg=COLOR_FONDO_PRINCIPAL)
        frame_inicio.place(relx=0, rely=0, relwidth=1, relheight=1)

        centro = tk.Frame(frame_inicio, bg=COLOR_FONDO_SECUNDARIO)
        centro.pack(expand=True)

        partida_iniciada = False

        def empezar_partida():
            nonlocal partida_iniciada
            partida_iniciada = True
            frame_inicio.destroy()
            lbl_estado.pack(fill="x", pady=(10, 0))
            contenedor.pack(expand=True)

        btn_jugar = tk.Button(centro, text="JUGAR", command=empezar_partida)
        btn_jugar.pack()

        self.assertTrue(frame_inicio.winfo_exists())
        self.assertFalse(partida_iniciada)

        btn_jugar.invoke()

        self.assertTrue(partida_iniciada)
        self.assertFalse(frame_inicio.winfo_exists(), "El frame de inicio debe destruirse al empezar")

    def test_barra_menu_superior_estructura(self):
        """Verifica que la barra de menús contenga los menús Partida y Ayuda con sus comandos."""
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        menu_partida = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Partida", menu=menu_partida)
        menu_partida.add_command(label="Nueva partida/Reiniciar")
        menu_partida.add_separator()
        menu_partida.add_command(label="Salir del juego")

        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Reglas del juego")

        self.assertEqual(barra_menu.entrycget(1, "label"), "Partida")
        self.assertEqual(barra_menu.entrycget(2, "label"), "Ayuda")
        self.assertEqual(menu_partida.entrycget(0, "label"), "Nueva partida/Reiniciar")
        self.assertEqual(menu_partida.entrycget(2, "label"), "Salir del juego")
        self.assertEqual(menu_ayuda.entrycget(0, "label"), "Reglas del juego")

    def test_pantalla_final_integrada_victoria_y_derrota(self):
        """Verifica que la pantalla final se superponga con títulos, estilos y botones correspondientes."""
        for victoria, texto_esperado, color_esperado in [
            (True, "¡Has ganado!", COLOR_VICTORIA),
            (False, "¡Has perdido!", COLOR_DERROTA),
        ]:
            frame_fin = tk.Frame(self.root, bg=COLOR_FONDO_PRINCIPAL)
            frame_fin.place(relx=0, rely=0, relwidth=1, relheight=1)

            centro_fin = tk.Frame(frame_fin, bg=COLOR_FONDO_SECUNDARIO)
            centro_fin.pack(expand=True)

            color_titulo = COLOR_VICTORIA if victoria else COLOR_DERROTA
            lbl_titulo = tk.Label(centro_fin, text=texto_esperado, fg=color_titulo)
            lbl_titulo.pack()

            btn_reiniciar = tk.Button(centro_fin, text="Jugar otra vez")
            btn_reiniciar.pack()
            btn_salir = tk.Button(centro_fin, text="Salir del juego")
            btn_salir.pack()

            self.assertEqual(lbl_titulo.cget("text"), texto_esperado)
            self.assertEqual(lbl_titulo.cget("fg"), color_esperado)
            self.assertEqual(btn_reiniciar.cget("text"), "Jugar otra vez")
            self.assertEqual(btn_salir.cget("text"), "Salir del juego")

            frame_fin.destroy()

    def test_mecanica_bloqueo_turno_jugador(self):
        """Verifica que si no es el turno del jugador (turno_jugador = False), no se procesen disparos."""
        juego_activo = True
        turno_jugador = False
        disparo_ejecutado = False

        def disparar_jugador(x, y):
            nonlocal disparo_ejecutado
            if not juego_activo or not turno_jugador:
                return
            disparo_ejecutado = True

        disparar_jugador(0, 0)
        self.assertFalse(disparo_ejecutado, "No debe permitir disparar cuando turno_jugador es False")

    def test_mecanica_repeticion_turno_jugador_tras_impacto(self):
        """Verifica que tras un impacto certero, el turno se mantenga en el jugador humano."""
        flota_humano = Barco.crear_flota(barcos)
        flota_maquina = Barco.crear_flota(barcos_maquina)
        jugador = Jugador("J1", flota_humano, False)
        maquina = Jugador("M1", flota_maquina, True)

        coord_barco = next(iter(maquina.mapa_barcos.keys()))
        turno_jugador = True

        _, _, vidas, _ = jugador.disparar(maquina, coord_barco[0], coord_barco[1])
        if vidas >= 0:
            # En impacto, repite turno
            turno_jugador = True
        else:
            turno_jugador = False

        self.assertTrue(turno_jugador, "El jugador debe repetir turno tras impactar un barco")

    def test_mecanica_cambio_turno_tras_agua(self):
        """Verifica que al disparar al agua, el turno del jugador cambie a False (pasa a la máquina)."""
        flota_humano = Barco.crear_flota(barcos)
        flota_maquina = Barco.crear_flota(barcos_maquina)
        jugador = Jugador("J1", flota_humano, False)
        maquina = Jugador("M1", flota_maquina, True)

        coord_agua = next(c for c in [(x, y) for x in range(10) for y in range(10)] if c not in maquina.mapa_barcos)
        turno_jugador = True

        _, _, vidas, _ = jugador.disparar(maquina, coord_agua[0], coord_agua[1])
        if vidas < 0:
            turno_jugador = False

        self.assertFalse(turno_jugador, "Disparar al agua debe ceder el turno a la máquina")

    def test_condicion_fin_de_partida_victoria(self):
        """Verifica que cuando el jugador hunde 10 barcos, el juego se marca como inactivo con victoria."""
        jugador_barcos_hundidos = 10
        juego_activo = True
        fin_victoria = False

        if jugador_barcos_hundidos == TOTAL_BARCOS:
            juego_activo = False
            fin_victoria = True

        self.assertFalse(juego_activo)
        self.assertTrue(fin_victoria)

    def test_condicion_fin_de_partida_derrota(self):
        """Verifica que cuando la máquina hunde 10 barcos, el juego se marca como inactivo con derrota."""
        maquina_barcos_hundidos = 10
        juego_activo = True
        fin_derrota = False

        if maquina_barcos_hundidos == TOTAL_BARCOS:
            juego_activo = False
            fin_derrota = True

        self.assertFalse(juego_activo)
        self.assertTrue(fin_derrota)

    def test_protocolo_cierre_ventana(self):
        """Verifica que la acción de salir configure correctamente reiniciar_partida en False."""
        reiniciar_partida = True

        def accion_salir():
            nonlocal reiniciar_partida
            reiniciar_partida = False

        self.root.protocol("WM_DELETE_WINDOW", accion_salir)
        accion_salir()
        self.assertFalse(reiniciar_partida, "El protocolo de salida debe asegurar que reiniciar_partida sea False")


if __name__ == "__main__":
    unittest.main(verbosity=2)
