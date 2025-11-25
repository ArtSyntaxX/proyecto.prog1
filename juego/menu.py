import pygame as p
from config import *


class Menu:
    """Clase base para todos los menús"""
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
        """Dibuja una opción del menú con indicador"""
        color = AMARILLO if seleccionada else BLANCO
        prefijo = "► " if seleccionada else "  "
        self.dibujar_texto_centrado(prefijo + texto, FUENTE_MENU, color, y)


class MenuInicio(Menu):
    """Menú principal con opciones START, VESTUARIO y QUIT"""
    def __init__(self, ventana):
        super().__init__(ventana)
        self.opciones = ["START - Elegir Nivel", "VESTUARIO - Naves y Balas", "QUIT - Salir"]
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
        self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 100)
        self.dibujar_texto_centrado("MENÚ PRINCIPAL", FUENTE_MENU, VERDE, 180)
        
        # Opciones
        y_inicio = 280
        espaciado = 80
        
        for i, opcion in enumerate(self.opciones):
            self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar", 
                                   FUENTE_TEXTO, BLANCO, 720)
        
        p.display.flip()


class MenuNiveles(Menu):
    """Menú para seleccionar uno de los 5 niveles disponibles"""
    def __init__(self, ventana):
        super().__init__(ventana)
        # Crear opciones dinámicamente desde config
        self.opciones = [f"Nivel {i} - {NIVELES[i]['nombre']}" for i in range(1, 6)]
        self.opciones.append("◄ Volver al Menú Principal")
        self.opcion_seleccionada = 0
    
    def manejar_eventos(self):
        """Maneja eventos del menú de niveles"""
        for event in p.event.get():
            if event.type == p.QUIT:
                return "quit"
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_TAB or event.key == p.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                
                elif event.key == p.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                
                elif event.key == p.K_RETURN:
                    if self.opcion_seleccionada == 5:  # Volver
                        return "menu_inicio"
                    else:
                        nivel = self.opcion_seleccionada + 1
                        return ("juego", nivel)
                
                elif event.key == p.K_ESCAPE:
                    return "menu_inicio"
        
        return None
    
    def dibujar(self):
        """Dibuja el menú de selección de niveles"""
        self.ventana.fill(NEGRO)
        
        # Títulos
        self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 50)
        self.dibujar_texto_centrado("SELECCIONA UN NIVEL", FUENTE_MENU, VERDE, 130)
        
        # Opciones
        y_inicio = 200
        espaciado = 80
        
        for i, opcion in enumerate(self.opciones):
            self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
                                   FUENTE_TEXTO, BLANCO, 720)
        
        p.display.flip()


class MenuVestuario(Menu):
    """Menú para seleccionar nave y tipo de bala en dos fases"""
    def __init__(self, ventana):
        super().__init__(ventana)
        self.fase = "nave"  # "nave" o "bala"
        self.nave_seleccionada = 1
        self.bala_seleccionada = 1
        self.opcion_seleccionada = 0
    
    def manejar_eventos(self):
        """Maneja eventos del menú vestuario"""
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
                        if self.opcion_seleccionada == 3:  # Volver atrás
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
        """Dibuja el menú de vestuario"""
        self.ventana.fill(NEGRO)
        
        if self.fase == "nave":
            # Títulos
            self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 50)
            self.dibujar_texto_centrado("ELIGE TU NAVE", FUENTE_MENU, VERDE, 130)
            
            opciones = [
                f"Nave 1 - {NAVES[1]['nombre']} (Velocidad: {NAVES[1]['velocidad']})",
                f"Nave 2 - {NAVES[2]['nombre']} (Velocidad: {NAVES[2]['velocidad']})",
                f"Nave 3 - {NAVES[3]['nombre']} (Velocidad: {NAVES[3]['velocidad']})",
                "◄ Volver al Menú Principal"
            ]
            
            y_inicio = 220
            espaciado = 90
            
            for i, opcion in enumerate(opciones):
                self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        else:  # fase == "bala"
            # Títulos
            self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 50)
            self.dibujar_texto_centrado("ELIGE TUS BALAS", FUENTE_MENU, ROJO, 130)
            
            # Info nave seleccionada
            nave_info = f"Nave: {NAVES[self.nave_seleccionada]['nombre']}"
            self.dibujar_texto_centrado(nave_info, FUENTE_TEXTO, VERDE, 200)
            
            opciones = [
                f"Balas 1 - {BALAS[1]['nombre']} (Daño: {BALAS[1]['daño']})",
                f"Balas 2 - {BALAS[2]['nombre']} (Daño: {BALAS[2]['daño']})",
                f"Balas 3 - {BALAS[3]['nombre']} (Daño: {BALAS[3]['daño']})",
                "◄ Volver a Elegir Nave"
            ]
            
            y_inicio = 270
            espaciado = 90
            
            for i, opcion in enumerate(opciones):
                self.dibujar_opcion(opcion, y_inicio + i * espaciado, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
                                   FUENTE_TEXTO, BLANCO, 720)
        
        p.display.flip()