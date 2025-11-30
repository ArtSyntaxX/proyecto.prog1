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
    
    def dibujar_cuadricula_fondo(self):
        """Dibuja una cuadrícula de fondo"""
        tamaño_grid = 50
        
        for x in range(0, ANCHO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (x, 0), (x, ALTO), 1)
        
        for y in range(0, ALTO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (0, y), (ANCHO, y), 1)
    
    def dibujar_borde_decorativo(self, x, y, ancho, alto):
        """Dibuja un borde decorativo"""
        p.draw.rect(self.ventana, CIAN, (x, y, ancho, alto), 2)


class MenuInicio(Menu):


    """Menú principal con opciones START, VESTUARIO y QUIT"""
    def __init__(self, ventana):
        super().__init__(ventana)
        self.opciones = ["START - Elegir Nivel", "VESTUARIO - Naves y Balas", "QUIT - Salir"]
        self.opcion_seleccionada = 0

        self.fondo = p.image.load(FONDO_START)
        self.fondo = p.transform.scale(self.fondo, (ANCHO, ALTO))
    
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
        self.ventana.blit(self.fondo, (0, 0))
        self.dibujar_cuadricula_fondo()
        
        # Título
        self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 80)
        self.dibujar_texto_centrado("MENÚ PRINCIPAL", FUENTE_MENU, VERDE, 160)
        
        # Opciones con recuadro
        y_inicio = 280
        espaciado = 90
        ancho_caja = 500
        
        for i, opcion in enumerate(self.opciones):
            y_opcion = y_inicio + i * espaciado
            
            # Fondo de opción seleccionada
            if i == self.opcion_seleccionada:
                p.draw.rect(self.ventana, GRIS_OSCURO, (50, y_opcion - 30, ancho_caja, 60))
                p.draw.rect(self.ventana, CIAN, (50, y_opcion - 30, ancho_caja, 60), 2)
            
            self.dibujar_opcion(opcion, y_opcion, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar", 
                                   FUENTE_PEQUEÑA, BLANCO, ALTO - 40)
        
        p.display.flip()


class MenuNiveles(Menu):
    """Menú para seleccionar uno de los 5 niveles disponibles"""
    def __init__(self, ventana):
        super().__init__(ventana)
        # Crear opciones dinámicamente desde config
        self.opciones = [f"Nivel {i} - {NIVELES[i]['nombre']}" for i in range(1, 6)]
        self.opciones.append("◄ Volver al Menú Principal")
        self.opcion_seleccionada = 0
        self.fondo = p.image.load(FONDO_NIVELES)
        self.fondo = p.transform.scale(self.fondo, (ANCHO, ALTO))
    
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
        self.ventana.blit(self.fondo, (0, 0))
        self.dibujar_cuadricula_fondo()
        
        # Títulos
        self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 40)
        self.dibujar_texto_centrado("SELECCIONA UN NIVEL", FUENTE_MENU, VERDE, 120)
        
        # Opciones con recuadro
        y_inicio = 200
        espaciado = 100
        ancho_caja = 500
        
        for i, opcion in enumerate(self.opciones):
            y_opcion = y_inicio + i * espaciado
            
            # Fondo de opción seleccionada
            if i == self.opcion_seleccionada:
                p.draw.rect(self.ventana, GRIS_OSCURO, (50, y_opcion - 30, ancho_caja, 60))
                p.draw.rect(self.ventana, CIAN, (50, y_opcion - 30, ancho_caja, 60), 2)
            
            self.dibujar_opcion(opcion, y_opcion, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
                                   FUENTE_PEQUEÑA, BLANCO, ALTO - 40)
        
        p.display.flip()


class MenuVestuario(Menu):
    """Menú para seleccionar nave y tipo de bala en dos fases"""
    def __init__(self, ventana):
        super().__init__(ventana)
        self.fase = "nave"  # "nave" o "bala"
        self.nave_seleccionada = 1
        self.bala_seleccionada = 1
        self.opcion_seleccionada = 0
        self.fondo = p.image.load(FONDO_NIVELES)
        self.fondo = p.transform.scale(self.fondo, (ANCHO, ALTO))
    
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
        self.ventana.blit(self.fondo, (0, 0))
        self.dibujar_cuadricula_fondo()
        
        y_inicio = 220
        espaciado = 100
        ancho_caja = 500
        
        if self.fase == "nave":
            # Títulos
            self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 40)
            self.dibujar_texto_centrado("ELIGE TU NAVE", FUENTE_MENU, VERDE, 120)
            
            opciones = [
                f"Nave 1 - {NAVES[1]['nombre']} (Velocidad: {NAVES[1]['velocidad']})",
                f"Nave 2 - {NAVES[2]['nombre']} (Velocidad: {NAVES[2]['velocidad']})",
                f"Nave 3 - {NAVES[3]['nombre']} (Velocidad: {NAVES[3]['velocidad']})",
                "◄ Volver al Menú Principal"
            ]
            
            for i, opcion in enumerate(opciones):
                y_opcion = y_inicio + i * espaciado
                
                # Fondo de opción seleccionada
                if i == self.opcion_seleccionada:
                    p.draw.rect(self.ventana, GRIS_OSCURO, (50, y_opcion - 30, ancho_caja, 60))
                    p.draw.rect(self.ventana, CIAN, (50, y_opcion - 30, ancho_caja, 60), 2)
                
                self.dibujar_opcion(opcion, y_opcion, i == self.opcion_seleccionada)
        
        else:  # fase == "bala"
            # Títulos
            self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 40)
            self.dibujar_texto_centrado("ELIGE TUS BALAS", FUENTE_MENU, ROJO, 120)
            
            # Info nave seleccionada
            nave_info = f"Nave: {NAVES[self.nave_seleccionada]['nombre']}"
            self.dibujar_texto_centrado(nave_info, FUENTE_PEQUEÑA, VERDE, 180)
            
            opciones = [
                f"Balas 1 - {BALAS[1]['nombre']} (Daño: {BALAS[1]['daño']})",
                f"Balas 2 - {BALAS[2]['nombre']} (Daño: {BALAS[2]['daño']})",
                f"Balas 3 - {BALAS[3]['nombre']} (Daño: {BALAS[3]['daño']})",
                "◄ Volver a Elegir Nave"
            ]
            
            for i, opcion in enumerate(opciones):
                y_opcion = y_inicio + i * espaciado
                
                # Fondo de opción seleccionada
                if i == self.opcion_seleccionada:
                    p.draw.rect(self.ventana, GRIS_OSCURO, (50, y_opcion - 30, ancho_caja, 60))
                    p.draw.rect(self.ventana, CIAN, (50, y_opcion - 30, ancho_caja, 60), 2)
                
                self.dibujar_opcion(opcion, y_opcion, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB/↑↓: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
                                   FUENTE_PEQUEÑA, BLANCO, ALTO - 40)
        
        p.display.flip()