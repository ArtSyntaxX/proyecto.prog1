import pygame as p
from config import *
from menu import MenuInicio, MenuNiveles, MenuVestuario
from juego import Juego
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ¿Qué poner aquí?
#- Crear ventana de pygame
#- Bucle principal que controla:
#  → Si estás en menú inicio → muestra MenuInicio
#  → Si eliges nivel → muestra MenuNiveles
#  → Si empiezas juego → muestra Juego
#  → Si vuelves atrás → vuelve al menú
#- Cerrar pygame al salir
def main():
    p.init()
    ventana = p.display.set_mode((ANCHO, ALTO))
    p.display.set_caption("Space Shooter")
    
    # Estado inicial
    estado = "menu_inicio"
    nave_elegida = 1
    bala_elegida = 1
    
    while True:
        if estado == "menu_inicio":
            menu = MenuInicio(ventana)
            
            while True:
                resultado = menu.manejar_eventos()
                menu.dibujar()
                
                if resultado == "quit":
                    p.quit()
                    return
                elif resultado == "niveles":
                    estado = "niveles"
                    break
                elif resultado == "vestuario":
                    estado = "vestuario"
                    break
        
        elif estado == "niveles":
            menu = MenuNiveles(ventana)
            
            while True:
                resultado = menu.manejar_eventos()
                menu.dibujar()
                
                if resultado == "quit":
                    p.quit()
                    return
                elif resultado == "menu_inicio":
                    estado = "menu_inicio"
                    break
                elif isinstance(resultado, tuple) and resultado[0] == "juego":
                    nivel = resultado[1]
                    juego = Juego(ventana, nivel, nave_elegida, bala_elegida)
                    resultado_juego = juego.ejecutar()
                    
                    if resultado_juego == "quit":
                        p.quit()
                        return
                    else:
                        estado = "menu_inicio"
                        break
        
        elif estado == "vestuario":
            menu = MenuVestuario(ventana)
            
            while True:
                resultado = menu.manejar_eventos()
                menu.dibujar()
                
                if resultado == "quit":
                    p.quit()
                    return
                elif resultado == "menu_inicio":
                    estado = "menu_inicio"
                    break
                elif isinstance(resultado, tuple) and resultado[0] == "vestuario_completo":
                    nave_elegida = resultado[1]
                    bala_elegida = resultado[2]
                    estado = "menu_inicio"
                    break

if __name__ == "__main__":
    main()