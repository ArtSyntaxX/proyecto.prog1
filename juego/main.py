import pygame as p  # Librería de gráficos/eventos (loop y teclas)
from .config import *  # Constantes y mapas de recursos del paquete 'juego'
# Archivo: main.py
# Propósito: orquestar el flujo de pantallas (menús y juego).
# Este módulo crea la ventana, decide el estado actual y llama
# a métodos de las clases de menú y del juego según la interacción.
from .menu import MenuInicio, MenuNiveles, MenuVestuario  # Clases de menús (definidas en 'juego/menu.py')
from .juego import Juego  # Clase principal del juego (definida en 'juego/juego.py')
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# Parametros: ninguno
# Retorno: None
def main():  # Entrada: crea ventana y orquesta menús y juego
    """
    Función principal (entrypoint) que controla el flujo de la aplicación.
    Viene del módulo 'main.py' dentro del paquete 'juego'.

    Flujo:
      - MenuInicio: START/NIVELES, VESTUARIO, QUIT
      - MenuNiveles: al elegir nivel se crea y ejecuta Juego
      - MenuVestuario: elegir Nave/Balas y volver a inicio
    """
    p.init()  # Inicializa subsistemas de pygame (video, audio, input)
    ventana = p.display.set_mode((ANCHO, ALTO))  # Superficie principal; se pasa a menús y juego
    p.display.set_caption("Space Shooter - Selecciona tu aventura")  # Título de la ventana
    
    # Estado inicial y variables globales
    estado = "menu_inicio"  # Controla qué pantalla se dibuja (inicio/niveles/vestuario)
    nave_elegida = 1  # ID de nave seleccionada (origen: config.NAVES)
    bala_elegida = 1  # ID de balas seleccionadas (origen: config.BALAS)
    
    print("=" * 50)
    print("SPACE SHOOTER - Sistema de Menús Inicializado")
    print("=" * 50)
    print(f"Ventana: {ANCHO}x{ALTO}")
    print(f"Nave inicial: {NAVES[nave_elegida]['nombre']}")
    print(f"Bala inicial: {BALAS[bala_elegida]['nombre']}")
    print(f"Niveles disponibles: {len(NIVELES)}")
    print("=" * 50)
    
    # Bucle principal (decide pantalla según 'estado').
    # Origen: bucle de juego típico de pygame;
    # espera eventos con p.event.get(), dibuja y actualiza pantalla.
    aplicacion_activa = True  # Variable de control del bucle principal
    while aplicacion_activa:
        # ========== MENÚ INICIO ==========
        if estado == "menu_inicio":  # Muestra menú principal y navega
            print("[*] Entrando a MENU PRINCIPAL")
            menu = MenuInicio(ventana)  # Parámetro 'ventana' es la superficie de dibujo compartida el llamamineto entero de esta 
                                        #Menu inicio siendo una de las funciones q se encuentra en menu.py
            
            menu_activo = True  # Variable de control del bucle
            while menu_activo:
                resultado = menu.manejar_eventos()  # Origen: método de clase MenuInicio (lee teclado/ventana)
                menu.dibujar()  # Origen: método de clase MenuInicio (pinta fondo/opciones)
                
                if resultado == "quit":
                    print("[*] Cerrando aplicacion...")
                    p.quit()
                    return
                
                elif resultado == "niveles":
                    print("[>] Navegando a SELECTOR DE NIVELES")
                    estado = "niveles"  # Cambia estado; el while externo decidirá nueva pantalla
                    menu_activo = False  # Sale del bucle
                
                elif resultado == "vestuario":
                    print("[>] Navegando a VESTUARIO")
                    estado = "vestuario"  # Cambia estado para abrir vestuario
                    menu_activo = False  # Sale del bucle
        
        # ========== MENÚ NIVELES ==========
        elif estado == "niveles":  # Selector de niveles y arranque del juego
            print(f"\n[>] Menu de Niveles (Nave: {NAVES[nave_elegida]['nombre']}, Balas: {BALAS[bala_elegida]['nombre']})")
            menu = MenuNiveles(ventana)  # Recibe 'ventana'; construye opciones desde config.NIVELES
            
            menu_activo = True  # Variable de control del bucle
            while menu_activo:
                resultado = menu.manejar_eventos()  # Lee teclas y devuelve acción/tupla
                menu.dibujar()  # Pinta títulos y lista de niveles
                
                if resultado == "quit":
                    print("[*] Cerrando aplicacion...")
                    p.quit()
                    return
                
                elif resultado == "menu_inicio":
                    print("[<] Volviendo a MENU PRINCIPAL")
                    estado = "menu_inicio"
                    menu_activo = False  # Sale del bucle
                
                elif isinstance(resultado, tuple) and resultado[0] == "juego":
                    nivel = resultado[1]  # Parámetro 'nivel' (int 1..5) proviene del menú
                    print(f"\n[>>] INICIANDO JUEGO - Nivel {nivel}: {NIVELES[nivel]['nombre']}")
                    print(f"   Nave: {NAVES[nave_elegida]['nombre']} | Balas: {BALAS[bala_elegida]['nombre']}")
                    # Construye juego con:
                    # - ventana: superficie compartida
                    # - nivel: config.NIVELES[nivel]
                    # - nave_elegida: config.NAVES[id]
                    # - bala_elegida: config.BALAS[id]
                    juego = Juego(ventana, nivel, nave_elegida, bala_elegida)
                    resultado_juego = juego.ejecutar()  # Loop interno del juego; devuelve 'quit' o estado de retorno
                    
                    if resultado_juego == "quit":
                        print("[*] Cerrando aplicacion...")
                        p.quit()
                        return
                    elif resultado_juego == "niveles":
                        print("[<] Volviendo a MENU DE NIVELES despues del juego")
                        menu_activo = False  # Sale del bucle
                    else:
                        print("[<] Volviendo a MENU PRINCIPAL despues del juego")
                        estado = "menu_inicio"
                        menu_activo = False  # Sale del bucle
        
        # ========== MENÚ VESTUARIO ==========
        elif estado == "vestuario":  # Elegir nave y balas en dos fases
            print(f"\n[>] Abriendo VESTUARIO")
            menu = MenuVestuario(ventana)  # Usa ventana; fase 'nave' y luego 'bala'
            
            menu_activo = True  # Variable de control del bucle
            while menu_activo:
                resultado = menu.manejar_eventos()  # Devuelve tuplas ('vestuario_completo', nave, bala) o navegación
                menu.dibujar()  # Pinta fondo, previews y opciones
                
                if resultado == "quit":
                    print("[*] Cerrando aplicacion...")
                    p.quit()
                    return
                
                elif resultado == "menu_inicio":
                    print("[<] Volviendo a MENU PRINCIPAL")
                    estado = "menu_inicio"
                    menu_activo = False  # Sale del bucle
                
                elif isinstance(resultado, tuple) and resultado[0] == "vestuario_completo":
                    nave_elegida = resultado[1]  # Origen: ID elegido en fase de naves (1..3)
                    bala_elegida = resultado[2]  # Origen: ID elegido en fase de balas (1..3)
                    print(f"[OK] Configuracion guardada:")
                    print(f"   Nave: {NAVES[nave_elegida]['nombre']} (Velocidad: {NAVES[nave_elegida]['velocidad']})")
                    print(f"   Balas: {BALAS[bala_elegida]['nombre']} (Danio: {BALAS[bala_elegida]['daño']})")
                    print("[<] Volviendo a MENU PRINCIPAL")
                    estado = "menu_inicio"
                    menu_activo = False  # Sale del bucle


if __name__ == "__main__":
    main()