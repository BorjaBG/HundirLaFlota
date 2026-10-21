"""
Punto de entrada principal para ejecutar el juego Hundir la Flota con interfaz gráfica Tkinter.
"""

from tkinter import Tk, Label, Frame, Button
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

    jugador = Jugador("Jugador 1", listado_barcos, False)
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
    lbl_estado.pack(fill="x", pady=(0, 10))

    # Contenedor principal
    contenedor = Frame(ventana, bg="#1e293b")
    contenedor.pack(expand=True)

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

    def turno_maquina():
        nonlocal juego_activo
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
                    return
                lbl_estado.config(text=f"La máquina ha hundido tu {barco.tipo}. La maquina vuelve a disparar", fg="#f87171")
            else:
                lbl_estado.config(text=f"Le han dado a tu {barco.tipo}. La maquina vuelve a disparar", fg="#fbbf24")
            ventana.after(700, turno_maquina)
        else:
            btn.config(text="D", bg="#0284c7")  # Azul
            lbl_estado.config(text="La máquina disparó al agua. Es tu turno", fg="#38bdf8")

    def disparar_jugador(coor_x, coor_y):
        nonlocal juego_activo
        if not juego_activo:
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
                    return
                lbl_estado.config(text=f"¡Hundido! Destruiste su {barco.tipo}. Repites disparo", fg="#4ade80")
            else:
                lbl_estado.config(text=f"Tocado en ({coor_x}, {coor_y}). Repites disparo", fg="#facc15")
            
        else:
            btn.config(text="D", bg="#38bdf8", fg="black")
            lbl_estado.config(text=f"Agua en ({coor_x}, {coor_y}). Turno de la máquina...", fg="#94a3b8")
            
            ventana.after(600, turno_maquina)

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

    ventana.mainloop()


def main():
    iniciar_juego()


if __name__ == "__main__":
    main()
