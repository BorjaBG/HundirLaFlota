'''
    Módulo de funciones de lógica de juego e interfaz gráfica para Hundir la Flota.
'''

import pygame
from tkinter import Tk, Label, Frame, Button, Menu, messagebox, PhotoImage

from variables import (
    barcos,
    barcos_maquina,
    DIMENSION_TABLERO,
    TOTAL_BARCOS,
    TIEMPO_ESPERA_TURNO,
    RUTA_VICTORIA_MP3,
    RUTA_DERROTA_MP3,
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
    COLOR_NEGRO
)
from clases.barco import Barco
from clases.jugador import Jugador

def inicializar_audio():
    '''
        Inicializa el subsistema de audio con baja latencia y precarga los sonidos de victoria y derrota.

        Returns:
            tuple: Tupla con (sonido_victoria, sonido_derrota) como objetos pygame.mixer.Sound o None.
    '''
    if not pygame.mixer.get_init():
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()

    try:
        sonido_victoria = pygame.mixer.Sound(RUTA_VICTORIA_MP3)
    except Exception:
        sonido_victoria = None

    try:
        sonido_derrota = pygame.mixer.Sound(RUTA_DERROTA_MP3)
    except Exception:
        sonido_derrota = None

    return sonido_victoria, sonido_derrota


def iniciar_juego():
    '''
        Funcion principal que orquesta la partida y la interfaz grafica de usuario en Tkinter.

        Returns:
            bool: True si el usuario solicita reiniciar la partida, False si decide salir.
    '''
    sonido_victoria, sonido_derrota = inicializar_audio()

    # Creación de flotas usando el método de clase Barco.crear_flota
    listado_barcos = Barco.crear_flota(barcos)
    listado_barcos_maquina = Barco.crear_flota(barcos_maquina)

    jugador = Jugador("Jugador", listado_barcos, False)
    maquina = Jugador("Ordenador", listado_barcos_maquina, True)

    # Ventana principal
    ventana = Tk()
    ventana.title("Hundir la Flota")
    ventana.geometry(f"{VENTANA_ANCHO}x{VENTANA_ALTO}")
    ventana.config(bg=COLOR_FONDO_PRINCIPAL)

    # Barra superior donde aparecen los mensajes durante la partida
    lbl_estado = Label(
        ventana,
        text="Empieza la partida",
        font=("Arial", 12, "bold"),
        bg=COLOR_BARRA_ESTADO,
        fg=COLOR_TEXTO_CLARO,
        pady=10
    )

    # Contenedor principal
    contenedor = Frame(ventana, bg=COLOR_FONDO_PRINCIPAL)

    # Tablero izquierdo (Jugador)
    frame_jugador = Frame(contenedor, bg=COLOR_FONDO_SECUNDARIO, padx=10, pady=10, relief="ridge", bd=2)
    frame_jugador.grid(row=0, column=0, padx=20)
    Label(frame_jugador, text="TU FLOTA", font=("Arial", 11, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_AGUA_DISPARO).grid(
        row=0, column=0, columnspan=DIMENSION_TABLERO, pady=(0, 8)
    )

    # Tablero derecho (Máquina)
    frame_maquina = Frame(contenedor, bg=COLOR_FONDO_SECUNDARIO, padx=10, pady=10, relief="ridge", bd=2)
    frame_maquina.grid(row=0, column=1, padx=20)
    Label(frame_maquina, text="ENEMIGO", font=("Arial", 11, "bold"), bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_ENEMIGO).grid(
        row=0, column=0, columnspan=DIMENSION_TABLERO, pady=(0, 8)
    )

    botones_maquina = {}
    botones_jugador = {}
    juego_activo = True
    turno_jugador = True
    reiniciar_partida = False

    def accion_reiniciar():
        '''
            Detiene el audio, marca la partida para reiniciar y destruye la ventana actual.
        '''
        nonlocal reiniciar_partida
        pygame.mixer.stop()
        reiniciar_partida = True
        ventana.destroy()

    def accion_salir():
        '''
            Detiene el audio, cancela el bucle de reinicio y cierra el juego.
        '''
        nonlocal reiniciar_partida
        pygame.mixer.stop()
        reiniciar_partida = False
        ventana.destroy()

    # Asegurar que la X de la ventana principal siempre cierre el juego
    ventana.protocol("WM_DELETE_WINDOW", accion_salir)

    # Menú superior
    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)
    menu_partida = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Partida", menu=menu_partida)
    menu_partida.add_command(label="Nueva partida/Reiniciar", command=accion_reiniciar)
    menu_partida.add_separator()
    menu_partida.add_command(label="Salir del juego", command=accion_salir)

    def mostrar_reglas():
        '''
            Muestra una ventana modal con las instrucciones y reglas del juego.
        '''
        messagebox.showinfo("Reglas del juego", "Instrucciones de Hundir la Flota:\n\n1. Dispara a las casillas enemigas del tablero derecho.\n2. Si tocas o hundes un barco, vuelves a disparar.\n3. Si disparas al agua, pasa el turno a la máquina.\n4. ¡Gana quien hunda antes los 10 barcos rivales!")

    menu_ayuda = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Reglas del juego", command=mostrar_reglas)

    def mostrar_pantalla_final(victoria: bool):
        '''
            Muestra la pantalla final de victoria o derrota con animacion y opciones para jugar de nuevo o salir.

            Args:
                victoria (bool): True si el jugador gano, False si fue derrotado.
        '''
        if victoria and sonido_victoria:
            sonido_victoria.play()
        elif not victoria and sonido_derrota:
            sonido_derrota.play()

        # Pantalla final superpuesta en la misma ventana
        frame_fin = Frame(ventana, bg=COLOR_FONDO_PRINCIPAL)
        frame_fin.place(relx=0, rely=0, relwidth=1, relheight=1)

        centro_fin = Frame(frame_fin, bg=COLOR_FONDO_SECUNDARIO, padx=40, pady=20, relief="ridge", bd=2)
        centro_fin.pack(expand=True)

        color_titulo = COLOR_VICTORIA if victoria else COLOR_DERROTA
        texto_titulo = "¡Has ganado!" if victoria else "¡Has perdido!"
        texto_desc = (
            "¡Enhorabuena! Has hundido toda la flota enemiga."
            if victoria else
            "La máquina ha destruido todos tus barcos."
        )

        Label(
            centro_fin,
            text=texto_titulo,
            font=("Arial", 22, "bold"),
            fg=color_titulo,
            bg=COLOR_FONDO_SECUNDARIO
        ).pack(pady=(0, 10))

        try:
            ruta_gif = RUTA_VICTORIA_GIF if victoria else RUTA_DERROTA_GIF
            img_fin = PhotoImage(file=ruta_gif)
            if img_fin.height() > 260:
                img_fin = img_fin.subsample(2, 2)
            lbl_img = Label(centro_fin, image=img_fin, bg=COLOR_FONDO_SECUNDARIO)
            lbl_img.image = img_fin
            lbl_img.pack(pady=(0, 15))
        except Exception:
            pass

        Label(
            centro_fin,
            text=texto_desc,
            font=("Arial", 11),
            fg=COLOR_TEXTO_SECUNDARIO,
            bg=COLOR_FONDO_SECUNDARIO
        ).pack(pady=(0, 20))

        frame_botones_fin = Frame(centro_fin, bg=COLOR_FONDO_SECUNDARIO)
        frame_botones_fin.pack()

        Button(
            frame_botones_fin,
            text="Jugar otra vez",
            font=("Arial", 12, "bold"),
            bg=COLOR_AGUA_TABLERO,
            fg=COLOR_BLANCO,
            activebackground=COLOR_BOTON_PRIMARIO_ACTIVO,
            padx=18,
            pady=8,
            bd=0,
            cursor="hand2",
            command=accion_reiniciar
        ).grid(row=0, column=0, padx=10)

        Button(
            frame_botones_fin,
            text="Salir del juego",
            font=("Arial", 12, "bold"),
            bg=COLOR_BARRA_ESTADO,
            fg=COLOR_TEXTO_CLARO,
            activebackground=COLOR_BOTON_SECUNDARIO_ACTIVO,
            padx=18,
            pady=8,
            bd=0,
            cursor="hand2",
            command=accion_salir
        ).grid(row=0, column=1, padx=10)

    def turno_maquina():
        '''
            Ejecuta el turno de disparo de la maquina de forma automatica y evalua el resultado.
        '''
        nonlocal juego_activo, turno_jugador
        if not juego_activo:
            return
        mx, my, vidas, barco = maquina.disparar(jugador)
        btn = botones_jugador[(mx, my)]
        if vidas >= 0:
            btn.config(text="X", bg=COLOR_IMPACTO)
            
            if vidas == 0:
                if maquina.barcos_hundidos == TOTAL_BARCOS:
                    juego_activo = False
                    lbl_estado.config(text="¡Has perdido! Toda tu flota ha sido hundida", fg=COLOR_DERROTA_CRITICA)
                    ventana.after(TIEMPO_ESPERA_TURNO, lambda: mostrar_pantalla_final(victoria=False))
                    return
                lbl_estado.config(text=f"La máquina ha hundido tu {barco.tipo}. Vuelve a disparar...", fg=COLOR_DERROTA)
            else:
                lbl_estado.config(text=f"Le han dado a tu {barco.tipo}. La máquina vuelve a disparar...", fg=COLOR_ALERTA)
            ventana.after(TIEMPO_ESPERA_TURNO, turno_maquina)
        else:
            btn.config(text="D", bg=COLOR_AGUA_TABLERO)
            lbl_estado.config(text="La máquina disparó al agua. ¡Es tu turno!", fg=COLOR_AGUA_DISPARO)
            turno_jugador = True

    def disparar_jugador(coor_x, coor_y):
        '''
            Procesa el disparo del jugador en las coordenadas especificadas del tablero enemigo.

            Args:
                coor_x (int): Coordenada X (fila) seleccionada.
                coor_y (int): Coordenada Y (columna) seleccionada.
        '''
        nonlocal juego_activo, turno_jugador
        if not juego_activo or not turno_jugador:
            return
        btn = botones_maquina[(coor_x, coor_y)]
        btn.config(state="disabled")

        _, _, vidas, barco = jugador.disparar(maquina, coordenada_x=coor_x, coordenada_y=coor_y)
        if vidas >= 0:
            btn.config(text="X", bg=COLOR_IMPACTO, fg=COLOR_BLANCO)
            
            if vidas == 0:
                if jugador.barcos_hundidos == TOTAL_BARCOS:
                    juego_activo = False
                    lbl_estado.config(text="¡Victoria! Has hundido toda la flota enemiga.", fg=COLOR_VICTORIA)
                    ventana.after(TIEMPO_ESPERA_TURNO, lambda: mostrar_pantalla_final(victoria=True))
                    return
                lbl_estado.config(text=f"¡Hundido! Destruiste su {barco.tipo}. Repites disparo", fg=COLOR_VICTORIA)
            else:
                lbl_estado.config(text=f"Tocado en ({coor_x}, {coor_y}). Repites disparo", fg=COLOR_TOCADO)
            
        else:
            turno_jugador = False
            btn.config(text="D", bg=COLOR_AGUA_DISPARO, fg=COLOR_NEGRO)
            lbl_estado.config(text=f"Agua en ({coor_x}, {coor_y}). Turno de la máquina...", fg=COLOR_TEXTO_MUTED)
            ventana.after(TIEMPO_ESPERA_TURNO, turno_maquina)

    # Creación del radar enemigo (tablero derecho)
    for x in range(DIMENSION_TABLERO):
        for y in range(DIMENSION_TABLERO):
            btn = Button(
                frame_maquina,
                text="A",
                width=2,
                height=1,
                font=("Arial", 9, "bold"),
                bg=COLOR_FONDO_PRINCIPAL,
                fg=COLOR_RADAR_AGUA,
                activebackground=COLOR_AGUA_DISPARO
            )
            btn.config(command=lambda fila=x, col=y: disparar_jugador(fila, col))
            btn.grid(row=x + 1, column=y, padx=1, pady=1)
            botones_maquina[(x, y)] = btn

    # Creación del tablero propio (tablero izquierdo)
    for x in range(DIMENSION_TABLERO):
        for y in range(DIMENSION_TABLERO):
            es_barco = (x, y) in jugador.mapa_barcos
            color_fondo = COLOR_BARCO_TABLERO if es_barco else COLOR_AGUA_TABLERO
            texto = "B" if es_barco else "A"

            btn = Button(
                frame_jugador,
                text=texto,
                width=2,
                height=1,
                font=("Arial", 9, "bold"),
                bg=color_fondo,
                fg=COLOR_BLANCO,
                state="disabled"
            )
            btn.grid(row=x + 1, column=y, padx=1, pady=1)
            botones_jugador[(x, y)] = btn

    # Pantalla de inicio
    frame_inicio = Frame(ventana, bg=COLOR_FONDO_PRINCIPAL)
    frame_inicio.place(relx=0, rely=0, relwidth=1, relheight=1)
    centro = Frame(frame_inicio, bg=COLOR_FONDO_SECUNDARIO)
    centro.pack(expand=True)

    Label(
        centro,
        text="Hundir la flota",
        font=("Arial", 18, "bold"),
        fg=COLOR_TEXTO_MUTED,
        bg=COLOR_FONDO_SECUNDARIO
    ).pack(pady=(0, 30))

    def empezar_partida():
        '''
            Oculta la pantalla de inicio y muestra los tableros para dar comienzo a la partida.
        '''
        frame_inicio.destroy()
        lbl_estado.pack(fill="x", pady=(10, 0))
        contenedor.pack(expand=True)

    Button(
        centro,
        text="JUGAR",
        font=("Arial", 14, "bold"),
        bg=COLOR_AGUA_TABLERO,
        fg=COLOR_BLANCO,
        activebackground=COLOR_BOTON_PRIMARIO_ACTIVO,
        activeforeground=COLOR_BLANCO,
        padx=30,
        pady=10,
        bd=0,
        cursor="hand2",
        command=empezar_partida
    ).pack(pady=10)

    Button(
        centro,
        text="Salir",
        font=("Arial", 10, "bold"),
        bg=COLOR_BARRA_ESTADO,
        fg=COLOR_TEXTO_SECUNDARIO,
        activebackground=COLOR_BOTON_SECUNDARIO_ACTIVO,
        padx=20,
        pady=6,
        bd=0,
        cursor="hand2",
        command=accion_salir
    ).pack(pady=5)

    ventana.mainloop()
    return reiniciar_partida

