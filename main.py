'''
    Punto de entrada principal para el juego Hundir la Flota.
'''

from funciones import iniciar_juego


def main():
    '''
        Funcion principal que inicia el bucle de juego.
        Permite reiniciar partidas sucesivas hasta que el usuario decida salir.
    '''
    jugar_de_nuevo = True
    while jugar_de_nuevo:
        jugar_de_nuevo = iniciar_juego()


if __name__ == "__main__":
    main()

