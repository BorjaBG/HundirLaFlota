from tkinter import Tk, Label, Frame, Button, Toplevel, Menu, messagebox
from variables import barcos, barcos_maquina
from clases.barco import Barco
from clases.jugador import Jugador


def iniciar_juego():
    # Instanciación de los barcos de ambos jugadores
    listado_barcos = [
        Barco(barco["ID"], barco["Nombre"], barco["Longitud"], barco["X"], barco["Y"], barco["Orientacion"], barco["Vidas"]) 
        for barco in barcos
    ]

    listado_barcos_maquina = [
        Barco(barco["ID"], barco["Nombre"], barco["Longitud"], 0, 0, 'H', barco["Vidas"]) 
        for barco in barcos_maquina
    ]

    jugador = Jugador("Jugador", listado_barcos, False)
    maquina = Jugador("Ordenador", listado_barcos_maquina, True)

    # Ventana principal
    ventana = Tk()
    ventana.title("Hundir la Flota")
    ventana.geometry("900x550")
    ventana.config(bg="#1e293b")

    # Barra superior donde aparecen los mensajes durante la partida
    lbl_estado = Label(
        ventana,
        text="Empieza la partida",
        font=("Arial", 12, "bold"),
        bg="#334155",
        fg="#f8fafc",
        pady=10
    )
    #lbl_estado.pack(fill="x", pady=(0, 10))

    # Contenedor principal
    contenedor = Frame(ventana, bg="#1e293b")
    #contenedor.pack(expand=True)

    # Tablero izquierdo
    frame_jugador = Frame(contenedor, bg="#0f172a", padx=10, pady=10, relief="ridge", bd=2)
    frame_jugador.grid(row=0, column=0, padx=20)
    Label(frame_jugador, text="TU FLOTA", font=("Arial", 11, "bold"), bg="#0f172a", fg="#38bdf8").grid(row=0, column=0, columnspan=10, pady=(0, 8))

    # Tablero derecho
    frame_maquina = Frame(contenedor, bg="#0f172a", padx=10, pady=10, relief="ridge", bd=2)
    frame_maquina.grid(row=0, column=1, padx=20)
    Label(frame_maquina, text="ENEMIGO", font=("Arial", 11, "bold"), bg="#0f172a", fg="#f43f5e").grid(row=0, column=0, columnspan=10, pady=(0, 8))

    botones_maquina = {}
    botones_jugador = {}
    juego_activo = True
    turno_jugador = True

    reiniciar_partida = False

    def accion_reiniciar():
        nonlocal reiniciar_partida
        reiniciar_partida = True
        ventana.destroy()

    def accion_salir():
        nonlocal reiniciar_partida
        reiniciar_partida = False
        ventana.destroy()

    # Asegurar que la X de la ventana principal siempre cierre el juego
    ventana.protocol("WM_DELETE_WINDOW", accion_salir)

    barra_menu = Menu(ventana)
    ventana.config(menu=barra_menu)
    menu_partida = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Partida", menu=menu_partida)
    menu_partida.add_command(label="Nueva partida/Reiniciar", command=accion_reiniciar)
    menu_partida.add_separator()
    menu_partida.add_command(label="Salir del juego", command=accion_salir)
    
    def mostrar_reglas():
        messagebox.showinfo("Placeholder de las reglas e instrucciones")

    menu_ayuda = Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
    menu_ayuda.add_command(label="Reglas del juego", command=mostrar_reglas)

    def mostrar_pantalla_final(victoria: bool):
        # Pantalla final superpuesta en la misma ventana (garantiza visibilidad inmediata)
        frame_fin = Frame(ventana, bg="#1e293b")
        frame_fin.place(relx=0, rely=0, relwidth=1, relheight=1)

        centro_fin = Frame(frame_fin, bg="#0f172a", padx=40, pady=30, relief="ridge", bd=2)
        centro_fin.pack(expand=True)

        color_titulo = "#4ade80" if victoria else "#f87171"
        icono = "🏆" if victoria else "💥"
        texto_titulo = f"{icono} ¡Victoria!" if victoria else f"{icono} ¡Derrota!"
        texto_desc = (
            "¡Enhorabuena, comandante! Has hundido toda la flota enemiga."
            if victoria else
            "La máquina ha destruido todos tus barcos."
        )

        Label(
            centro_fin,
            text=texto_titulo,
            font=("Arial", 22, "bold"),
            fg=color_titulo,
            bg="#0f172a"
        ).pack(pady=(0, 10))

        Label(
            centro_fin,
            text=texto_desc,
            font=("Arial", 11),
            fg="#cbd5e1",
            bg="#0f172a"
        ).pack(pady=(0, 25))

        frame_botones_fin = Frame(centro_fin, bg="#0f172a")
        frame_botones_fin.pack()

        Button(
            frame_botones_fin,
            text="🔄 Jugar otra vez",
            font=("Arial", 12, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            padx=18,
            pady=8,
            bd=0,
            cursor="hand2",
            command=accion_reiniciar
        ).grid(row=0, column=0, padx=10)

        Button(
            frame_botones_fin,
            text="❌ Salir del juego",
            font=("Arial", 12, "bold"),
            bg="#334155",
            fg="#f8fafc",
            activebackground="#475569",
            padx=18,
            pady=8,
            bd=0,
            cursor="hand2",
            command=accion_salir
        ).grid(row=0, column=1, padx=10)

    def turno_maquina():
        nonlocal juego_activo, turno_jugador
        if not juego_activo:
            return
        mx, my, vidas, barco = maquina.disparar(jugador)
        btn = botones_jugador[(mx, my)]
        if vidas >= 0:
            btn.config(text="X", bg="#dc2626")  # Rojo fuego
            
            if vidas == 0:
                if maquina.barcos_hundidos == 10:
                    juego_activo = False
                    lbl_estado.config(text="¡Has perdido! Toda tu flota ha sido hundida", fg="#ef4444")
                    ventana.after(2000, lambda: mostrar_pantalla_final(victoria=False))
                    return
                lbl_estado.config(text=f"La máquina ha hundido tu {barco.tipo}. Vuelve a disparar...", fg="#f87171")
            else:
                lbl_estado.config(text=f"Le han dado a tu {barco.tipo}. La máquina vuelve a disparar...", fg="#fbbf24")
            ventana.after(2000, turno_maquina)
        else:
            btn.config(text="D", bg="#0284c7")  # Azul
            lbl_estado.config(text="La máquina disparó al agua. ¡Es tu turno!", fg="#38bdf8")
            turno_jugador = True

    def disparar_jugador(coor_x, coor_y):
        nonlocal juego_activo, turno_jugador
        if not juego_activo or not turno_jugador:
            return
        btn = botones_maquina[(coor_x, coor_y)]
        btn.config(state="disabled")

        _, _, vidas, barco = jugador.disparar(maquina, coordenada_x=coor_x, coordenada_y=coor_y)
        if vidas >= 0:
            btn.config(text="X", bg="#dc2626", fg="white")
            
            if vidas == 0:
                if jugador.barcos_hundidos == 10:
                    juego_activo = False
                    lbl_estado.config(text="¡Victoria! Has hundido toda la flota enemiga.", fg="#4ade80")
                    ventana.after(2000, lambda: mostrar_pantalla_final(victoria=True))
                    return
                lbl_estado.config(text=f"¡Hundido! Destruiste su {barco.tipo}. Repites disparo", fg="#4ade80")
            else:
                lbl_estado.config(text=f"Tocado en ({coor_x}, {coor_y}). Repites disparo", fg="#facc15")
            
        else:
            turno_jugador = False
            btn.config(text="D", bg="#38bdf8", fg="black")
            lbl_estado.config(text=f"Agua en ({coor_x}, {coor_y}). Turno de la máquina...", fg="#94a3b8")
            
            ventana.after(2000, turno_maquina)


    for x in range(10):
        for y in range(10):
            btn = Button(
                frame_maquina,
                text="A",
                width=2,
                height=1,
                font=("Arial", 9, "bold"),
                bg="#1e293b",
                fg="#64748b",
                activebackground="#38bdf8"
            )
            btn.config(command=lambda fila=x, col=y: disparar_jugador(fila, col))
            btn.grid(row=x + 1, column=y, padx=1, pady=1)

            botones_maquina[(x, y)] = btn

    for x in range(10):
        for y in range(10):
            es_barco = (x, y) in jugador.mapa_barcos
            color_fondo = "#475569" if es_barco else "#0284c7"  # Si es agua, azul, si es barco, gris
            texto = "B" if es_barco else "A"

            btn = Button(
                frame_jugador,
                text=texto,
                width=2,
                height=1,
                font=("Arial", 9, "bold"),
                bg=color_fondo,
                fg="white",
                state="disabled"
            )

            btn.grid(row=x + 1, column=y, padx=1, pady=1)

            botones_jugador[(x, y)] = btn

    # Pantalla de inicio
    frame_inicio = Frame(ventana, bg="#1e293b")
    frame_inicio.place(relx=0, rely=0, relwidth=1, relheight=1)
    centro = Frame(frame_inicio, bg="#0f172a")
    centro.pack(expand=True)

    Label(
        centro,
        text="Hundir la flota",
        font=("Arial", 18, "bold"),
        fg="#94a3b8",
        bg="#0f172a"
    ).pack(pady=(0, 30))

    def empezar_partida():
        frame_inicio.destroy()
        lbl_estado.pack(fill="x", pady=(10, 0))
        contenedor.pack(expand=True)

    # Botón principal de JUGAR
    Button(
        centro,
        text="▶ JUGAR",
        font=("Arial", 14, "bold"),
        bg="#0284c7",
        fg="white",
        activebackground="#0369a1",
        activeforeground="white",
        padx=30,
        pady=10,
        bd=0,
        cursor="hand2",
        command=empezar_partida
    ).pack(pady=10)
    # Botón secundario para salir
    Button(
        centro,
        text="Salir",
        font=("Arial", 10, "bold"),
        bg="#334155",
        fg="#cbd5e1",
        activebackground="#475569",
        padx=20,
        pady=6,
        bd=0,
        cursor="hand2",
        command=accion_salir
    ).pack(pady=5)

    ventana.mainloop()
    return reiniciar_partida


def main():
    jugar_de_nuevo = True
    while jugar_de_nuevo:
        jugar_de_nuevo = iniciar_juego()

if __name__ == "__main__":
    main()
