# Informe Técnico de Pruebas: Hundir la Flota

- **Fecha de ejecución:** 22 de Octubre de 2026  
- **Entorno:** Python 3.13 en Windows con Pygame 2.6.1 y Tkinter  
- **Suite de pruebas:** [test_juego.py](./test_juego.py)  
- **Resultado global:** **43 / 43 pruebas superadas (100% éxito)**

---

## 1. Resumen Ejecutivo

Se ha diseñado y ejecutado un plan de pruebas exhaustivo que abarca la totalidad de capas, módulos refactorizados y dinámicas de juego:

1. **Configuración, Variables y Paleta Visual:** [`variables.py`](../variables.py)
2. **Entidades del Dominio:** [`clases/barco.py`](../clases/barco.py) y [`clases/tablero.py`](../clases/tablero.py)
3. **Lógica de Juego, Algoritmos IA y Efectos de Audio:** [`clases/jugador.py`](../clases/jugador.py)
4. **Lógica de Partida, Multimedia y Flujo:** [`funciones.py`](../funciones.py)
5. **Interfaz Gráfica Tkinter (Menús, Gestión de Turnos, Pantalla Final y Protocolo de Cierre):** [`funciones.py`](../funciones.py) / [`main.py`](../main.py)
6. **Pruebas de Estrés y Simulación de Partidas Completas**

---

## 2. Detalle de Pruebas por Módulo

### 2.1. Configuración de Flotas y Variables (`TestVariables`)
Verifica la consistencia del catálogo de naves, constantes de juego y recursos multimedia.

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_cantidad_barcos_ambos_jugadores` | 10 barcos asignados al jugador y 10 a la máquina | **SUPERADA** |
| `test_claves_obligatorias_barcos` | Integridad de claves reglamentarias: ID, Nombre, Longitud, Vidas | **SUPERADA** |
| `test_tipos_datos_barcos` | Validación estricta de tipos de datos en la flota | **SUPERADA** |
| `test_distribucion_flota_reglamentaria` | 1 Portaviones (4), 2 Acorazados (3), 3 Cruceros (2), 4 Destructores (1) | **SUPERADA** |
| `test_total_vidas_y_casillas` | Suma de vidas y casillas exactamente igual a 20 | **SUPERADA** |
| `test_ids_unicos` | Sin colisión ni duplicación de identificadores de barcos | **SUPERADA** |
| `test_constantes_juego_y_tiempos` | Dimensiones (10x10), barcos (10), espera (2000 ms) y ventana (900x550) | **SUPERADA** |
| `test_existencia_archivos_assets` | Comprobación física en disco de todos los archivos `.mp3` y `.gif` | **SUPERADA** |
| `test_paleta_colores_hex` | Validación de formato hexadecimal `#RRGGBB` para toda la paleta de diseño | **SUPERADA** |

---

### 2.2. Tablero de Juego (`TestTablero`)
Verifica la estructura matricial y la independencia de memoria.

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_constructor_tablero` | Atributos `id_jugador`, `dimension` y `barcos` | **SUPERADA** |
| `test_dimensiones_matriz` | Matriz bidimensional exacta de 10 x 10 con `DIMENSION_TABLERO` | **SUPERADA** |
| `test_contenido_inicial_agua` | 100% de las casillas inicializadas con `'A'` (Agua) | **SUPERADA** |
| `test_independencia_de_filas` | Cada fila es una lista independiente en memoria (sin referencias compartidas) | **SUPERADA** |

---

### 2.3. Entidad Barco y Factorías (`TestBarco`)

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_instanciacion_atributos` | Validación del constructor de `Barco` | **SUPERADA** |
| `test_asignar_posicion` | Métodos mutadores de posición (`x`, `y`) y orientación | **SUPERADA** |
| `test_decremento_de_vidas` | Reducción de vidas tras impacto | **SUPERADA** |
| `test_crear_desde_diccionario` | Método de factoría que instancia barcos a partir de diccionarios | **SUPERADA** |
| `test_crear_flota` | Creación masiva de flotas de barcos sin coordenadas fijas | **SUPERADA** |

---

### 2.4. Colocación de Flota y Reglas Navales (`TestJugadorColocacion`)

> **Regla de no-contacto naval:**  
> El algoritmo de colocación aleatoria garantiza que ningún barco quede en contacto con otro (ni ortogonal ni diagonalmente).

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_humano_coloca_exactamente_20_casillas` | 20 casillas en `mapa_barcos` y 20 celdas `'B'` en el tablero visible | **SUPERADA** |
| `test_maquina_oculta_barcos_en_tablero` | 20 casillas en memoria, pero tablero público 100% niebla (`'A'`) | **SUPERADA** |
| `test_coordenadas_dentro_del_rango_oficial` | Todas las coordenadas generadas pertenecen al rango [0..9] | **SUPERADA** |
| `test_regla_no_contacto_entre_barcos` | Verificación de vecindario 3x3: separación estricta entre barcos | **SUPERADA** |

---

### 2.5. Mecánica de Disparos, Daño y Efectos de Audio (`TestJugadorDisparos`)

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_disparo_agua_coordenada_especifica` | Marcado con `'D'`, vidas retorna `-1`, barco `None` | **SUPERADA** |
| `test_disparo_tocado_reduce_vidas` | Marcado con `'X'`, reducción de vida del barco impactado | **SUPERADA** |
| `test_disparo_hundido_incrementa_contador` | Al llegar vidas a 0, `barcos_hundidos` incrementa en 1 | **SUPERADA** |
| `test_disparo_aleatorio_no_toca_casillas_ya_disparadas` | La IA nunca ataca casillas previamente marcadas con `'D'` o `'X'` | **SUPERADA** |
| `test_disparo_aleatorio_en_tablero_limpio` | El disparo aleatorio inicial opera dentro de los límites de 0 a 9 | **SUPERADA** |
| `test_disparar_ejecuta_match_case_por_tipo` | Ejecución del `match/case` sonoro para Portaviones, Crucero, Destructor y Acorazado | **SUPERADA** |

---

### 2.6. Funciones de Juego y Multimedia (`TestFuncionesJuego`)

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_inicializar_audio_retorno` | Inicialización de pygame mixer a baja latencia y retorno de tupla de sonidos | **SUPERADA** |
| `test_escalado_gif_animacion` | Carga de `PhotoImage` y escalado `subsample(2, 2)` si altura > 260px | **SUPERADA** |

---

### 2.7. Pruebas de Estrés y Simulación (`TestEstresYSimulacion`)

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_estres_generacion_50_tableros_aleatorios` | 50 generaciones consecutivas con 20 casillas exactas y 0 fallos | **SUPERADA** |
| `test_simulacion_10_partidas_completas` | 10 partidas de principio a fin entre dos IAs con mecánica de repetición de turnos | **SUPERADA** |

---

### 2.8. Interfaz Gráfica Tkinter, Gestión de Turnos y Ciclo de Vida (`TestInterfazGrafica`)

| Nombre de la Prueba | Objetivo | Estado |
| :--- | :--- | :---: |
| `test_tk_disponible` | Inicialización, ciclo de eventos y destrucción de ventana Tkinter | **SUPERADA** |
| `test_componentes_interfaz_juego` | Validación de los 100 botones de radar, 100 botones de flota, label y disparos | **SUPERADA** |
| `test_pantalla_inicio_y_transicion_a_juego` | Pantalla de bienvenida, botón JUGAR y transición limpia a tableros | **SUPERADA** |
| `test_barra_menu_superior_estructura` | Barra de menús con opciones "Partida", "Nueva partida", "Salir" y "Ayuda" | **SUPERADA** |
| `test_pantalla_final_integrada_victoria_y_derrota` | Pantalla final integrada para Victoria y Derrota con botones Rejugar y Salir | **SUPERADA** |
| `test_mecanica_bloqueo_turno_jugador` | Bloqueo de clics mientras no sea el turno del jugador humano (`turno_jugador = False`) | **SUPERADA** |
| `test_mecanica_repeticion_turno_jugador_tras_impacto` | Mantenimiento del turno en el jugador tras acertar a un barco rival | **SUPERADA** |
| `test_mecanica_cambio_turno_tras_agua` | Cesión del turno a la máquina al disparar al agua | **SUPERADA** |
| `test_condicion_fin_de_partida_victoria` | Detección de fin de juego y victoria al hundir 10 barcos rivales | **SUPERADA** |
| `test_condicion_fin_de_partida_derrota` | Detección de fin de juego y derrota al perder los 10 barcos propios | **SUPERADA** |
| `test_protocolo_cierre_ventana` | Manejo del protocolo `WM_DELETE_WINDOW` para cierre inmediato y seguro con la X | **SUPERADA** |

---

## 3. Métricas y Conclusión

```text
======================================================================
Ran 43 tests in 3.221s

OK
======================================================================
```

- **Total de pruebas ejecutadas:** 43
- **Pruebas superadas:** 43 (100%)
- **Pruebas fallidas:** 0
- **Errores de ejecución:** 0
- **Tiempo total de ejecución:** ~3.2 segundos

### Conclusión Técnica
La suite de pruebas cubre de forma completa y exhaustiva la arquitectura refactorizada (`variables.py`, `clases/`, `funciones.py` y `main.py`). Se garantiza la solidez de las mecánicas de disparo por turnos, los efectos de sonido por tipo de nave, las animaciones GIF escaladas, la prevención de bloqueos de interfaz mediante frames integrados y el cierre seguro de ventana.
