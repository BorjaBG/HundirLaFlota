"""
Módulo de funciones auxiliares y lógica del juego Hundir la Flota.
"""

def imprimir_tableros_paralelos(tablero1, tablero2, titulo1="Jugador", titulo2="Máquina"):
    """
    Imprime en la consola dos tableros uno al lado del otro.
    """
    print(f"{titulo1:^40}    {titulo2:^20}")
    print("-" * 80)

    for fila1, fila2 in zip(tablero1, tablero2):
        print(f'{" ".join(fila1)} {" ":^25} {" ".join(fila2)}')
    print()
