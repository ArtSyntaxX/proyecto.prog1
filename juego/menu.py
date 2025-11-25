import pygame as p
from config import *

# ¿Qué poner aquí?
#- Clase MenuInicio (pantalla START/QUIT)
#- Clase MenuNiveles (elegir nivel 1/2/3)
#- Clase MenuVestuario (elegir nave y balas)
#- Funciones para dibujar texto
#- Funciones para manejar navegación con TAB

class Menu:
    def __init__(self, ventana):
        self.ventana = ventana
        self.opcion_seleccionada = 0
        
    def dibujar_texto_centrado(self, texto, fuente, color, y):
        """Dibuja texto centrado horizontalmente"""
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(ANCHO // 2, y))
        self.ventana.blit(superficie, rect)
        return rect
    
    def dibujar_opcion(self, texto, y, seleccionada):
        """Dibuja una opción del menú"""
        color = AMARILLO if seleccionada else BLANCO
        prefijo = "► " if seleccionada else "  "
        self.dibujar_texto_centrado(prefijo + texto, FUENTE_MENU, color, y)

class MenuInicio(Menu):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.opciones = ["START", "VESTUARIO", "QUIT"]
        self.opcion_seleccionada = 0
    
    def manejar_eventos(self):
        """Maneja eventos del menú inicio"""
        for event in p.event.get():
            if event.type == p.QUIT:
                return "quit"
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_TAB or event.key == p.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                
                elif event.key == p.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                
                elif event.key == p.K_RETURN:
                    if self.opcion_seleccionada == 0:
                        return "niveles"
                    elif self.opcion_seleccionada == 1:
                        return "vestuario"
                    elif self.opcion_seleccionada == 2:
                        return "quit"
        
        return None
    
    def dibujar(self):
        """Dibuja el menú de inicio"""
        self.ventana.fill(NEGRO)
        
        # Título
        self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 150)
        
        # Opciones
        y_inicio = 350
        espaciado = 80
        
        for i, opcion in enumerate(self.opciones):
            self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar", 
                                   FUENTE_TEXTO, BLANCO, 700)
        
        p.display.flip()

class MenuNiveles(Menu):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.opciones = ["Nivel 1 - Fácil", "Nivel 2 - Normal", "Nivel 3 - Difícil", "Volver"]
        self.opcion_seleccionada = 0
    
    def manejar_eventos(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                return "quit"
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_TAB or event.key == p.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                
                elif event.key == p.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                
                elif event.key == p.K_RETURN:
                    if self.opcion_seleccionada == 3:  # Volver
                        return "menu_inicio"
                    else:
                        return ("juego", self.opcion_seleccionada + 1)  # Devuelve nivel elegido
                
                elif event.key == p.K_ESCAPE:
                    return "menu_inicio"
        
        return None
    
    def dibujar(self):
        self.ventana.fill(NEGRO)
        
        self.dibujar_texto_centrado("SELECTOR DE NIVELES", FUENTE_TITULO, VERDE, 150)
        
        y_inicio = 300
        espaciado = 70
        
        for i, opcion in enumerate(self.opciones):
            self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
                                   FUENTE_TEXTO, BLANCO, 700)
        
        p.display.flip()

class MenuVestuario(Menu):
    def __init__(self, ventana):
        super().__init__(ventana)
        self.fase = "nave"  # "nave" o "bala"
        self.nave_seleccionada = 1
        self.bala_seleccionada = 1
        self.opcion_seleccionada = 0
    
    def manejar_eventos(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                return "quit"
            
            if event.type == p.KEYDOWN:
                if self.fase == "nave":
                    if event.key == p.K_TAB or event.key == p.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % 4
                    
                    elif event.key == p.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % 4
                    
                    elif event.key == p.K_RETURN:
                        if self.opcion_seleccionada == 3:  # Volver
                            return "menu_inicio"
                        else:
                            self.nave_seleccionada = self.opcion_seleccionada + 1
                            self.fase = "bala"
                            self.opcion_seleccionada = 0
                    
                    elif event.key == p.K_ESCAPE:
                        return "menu_inicio"
                
                elif self.fase == "bala":
                    if event.key == p.K_TAB or event.key == p.K_DOWN:
                        self.opcion_seleccionada = (self.opcion_seleccionada + 1) % 4
                    
                    elif event.key == p.K_UP:
                        self.opcion_seleccionada = (self.opcion_seleccionada - 1) % 4
                    
                    elif event.key == p.K_RETURN:
                        if self.opcion_seleccionada == 3:  # Volver
                            self.fase = "nave"
                            self.opcion_seleccionada = 0
                        else:
                            self.bala_seleccionada = self.opcion_seleccionada + 1
                            return ("vestuario_completo", self.nave_seleccionada, self.bala_seleccionada)
                    
                    elif event.key == p.K_ESCAPE:
                        self.fase = "nave"
                        self.opcion_seleccionada = 0
        
        return None
    
    def dibujar(self):
        self.ventana.fill(NEGRO)
        
        if self.fase == "nave":
            self.dibujar_texto_centrado("ELIGE TU NAVE", FUENTE_TITULO, AZUL, 100)
            
            opciones = [
                "Nave 1 - Básica",
                "Nave 2 - Rápida",
                "Nave 3 - Resistente",
                "Volver"
            ]
            
            y_inicio = 250
            espaciado = 70
            
            for i, opcion in enumerate(opciones):
                self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        else:  # fase == "bala"
            self.dibujar_texto_centrado("ELIGE TUS BALAS", FUENTE_TITULO, ROJO, 100)
            self.dibujar_texto_centrado(f"Nave elegida: {NAVES[self.nave_seleccionada]['nombre']}", 
                                       FUENTE_TEXTO, VERDE, 180)
            
            opciones = [
                "Balas 1 - Normales",
                "Balas 2 - Potentes",
                "Balas 3 - Explosivas",
                "Volver"
            ]
            
            y_inicio = 280
            espaciado = 70
            
            for i, opcion in enumerate(opciones):
                self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
                                   FUENTE_TEXTO, BLANCO, 700)
        
        p.display.flip()