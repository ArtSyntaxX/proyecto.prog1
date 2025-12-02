import pygame as p
from .config import *
# Archivo: main.py
# Propósito: orquestar el flujo de pantallas (menús y juego).
# Este módulo crea la ventana, decide el estado actual y llama
# a métodos de las clases de menú y del juego según la interacción.
from .menu import MenuInicio, MenuNiveles, MenuVestuario
from .juego import Juego
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def main():
        """
        Función principal (entrypoint) que controla el flujo de la aplicación.
        Viene del módulo 'main.py' dentro del paquete 'juego'.
    
        Flujo:
            - MenuInicio: START/NIVELES, VESTUARIO, QUIT
            - MenuNiveles: al elegir nivel se crea y ejecuta Juego
            - MenuVestuario: elegir Nave/Balas y volver a inicio
        """
    p.init()
    ventana = p.display.set_mode((ANCHO, ALTO))
    p.display.set_caption("Space Shooter - Selecciona tu aventura")
    
    # Estado inicial y variables globales
    estado = "menu_inicio"
    nave_elegida = 1
    bala_elegida = 1
    
    print("=" * 50)
    print("SPACE SHOOTER - Sistema de Menús Inicializado")
    print("=" * 50)
    print(f"Ventana: {ANCHO}x{ALTO}")
    print(f"Nave inicial: {NAVES[nave_elegida]['nombre']}")
    print(f"Bala inicial: {BALAS[bala_elegida]['nombre']}")
    print(f"Niveles disponibles: {len(NIVELES)}")
    print("=" * 50)
    
    # Bucle principal (decide qué pantalla mostrar según 'estado')
    while True:
        # ========== MENÚ INICIO ==========
        if estado == "menu_inicio":
            print("[*] Entrando a MENU PRINCIPAL")
            menu = MenuInicio(ventana)
            
            while True:
                resultado = menu.manejar_eventos()
                menu.dibujar()
                
                if resultado == "quit":
                    print("[*] Cerrando aplicacion...")
                    p.quit()
                    return
                
                elif resultado == "niveles":
                    print("[>] Navegando a SELECTOR DE NIVELES")
                    estado = "niveles"
                    break
                
                elif resultado == "vestuario":
                    print("[>] Navegando a VESTUARIO")
                    estado = "vestuario"
                    break
        
        # ========== MENÚ NIVELES ==========
        elif estado == "niveles":
            print(f"\n[>] Menu de Niveles (Nave: {NAVES[nave_elegida]['nombre']}, Balas: {BALAS[bala_elegida]['nombre']})")
            menu = MenuNiveles(ventana)
            
            while True:
                resultado = menu.manejar_eventos()
                menu.dibujar()
                
                if resultado == "quit":
                    print("[*] Cerrando aplicacion...")
                    p.quit()
                    return
                
                elif resultado == "menu_inicio":
                    print("[<] Volviendo a MENU PRINCIPAL")
                    estado = "menu_inicio"
                    break
                
                elif isinstance(resultado, tuple) and resultado[0] == "juego":
                    nivel = resultado[1]
                    print(f"\n[>>] INICIANDO JUEGO - Nivel {nivel}: {NIVELES[nivel]['nombre']}")
                    print(f"   Nave: {NAVES[nave_elegida]['nombre']} | Balas: {BALAS[bala_elegida]['nombre']}")
                    
                    juego = Juego(ventana, nivel, nave_elegida, bala_elegida)
                    resultado_juego = juego.ejecutar()
                    
                    if resultado_juego == "quit":
                        print("[*] Cerrando aplicacion...")
                        p.quit()
                        return
                    elif resultado_juego == "niveles":
                        print("[<] Volviendo a MENU DE NIVELES despues del juego")
                        break
                    else:
                        print("[<] Volviendo a MENU PRINCIPAL despues del juego")
                        estado = "menu_inicio"
                        break
        
        # ========== MENÚ VESTUARIO ==========
        elif estado == "vestuario":
            print(f"\n[>] Abriendo VESTUARIO")
            menu = MenuVestuario(ventana)
            
            while True:
                resultado = menu.manejar_eventos()
                menu.dibujar()
                
                if resultado == "quit":
                    print("[*] Cerrando aplicacion...")
                    p.quit()
                    return
                
                elif resultado == "menu_inicio":
                    print("[<] Volviendo a MENU PRINCIPAL")
                    estado = "menu_inicio"
                    break
                
                elif isinstance(resultado, tuple) and resultado[0] == "vestuario_completo":
                    nave_elegida = resultado[1]
                    bala_elegida = resultado[2]
                    print(f"[OK] Configuracion guardada:")
                    print(f"   Nave: {NAVES[nave_elegida]['nombre']} (Velocidad: {NAVES[nave_elegida]['velocidad']})")
                    print(f"   Balas: {BALAS[bala_elegida]['nombre']} (Danio: {BALAS[bala_elegida]['daño']})")
                    print("[<] Volviendo a MENU PRINCIPAL")
                    estado = "menu_inicio"
                    break


if __name__ == "__main__":
    main()