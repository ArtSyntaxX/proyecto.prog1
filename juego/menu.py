import pygame as p
from .config import *
#=================================
# CLASES DE MENUS
#
# Menu (clase base)
# - MenuInicio
# - MenuNiveles
# - MenuVestuario
#=================================

class Menu:
    # Clase base de utilidades de dibujo y selección para menús
    
    # Parametros: ventana (pygame.Surface)
    # Retorno: None
    def __init__(self, ventana):  # Guarda ventana y estado de selección
        self.ventana = ventana
        self.opcion_seleccionada = 0
        
    # Parametros: texto (str), fuente (pygame.font.Font), color (tuple RGB), y (int)
    # Retorno: pygame.Rect del texto dibujado
    def dibujar_texto_centrado(self, texto, fuente, color, y):  # Centra texto en X
        """Dibuja texto centrado horizontalmente"""
        superficie = fuente.render(texto, True, color)
        rect = superficie.get_rect(center=(ANCHO // 2, y))
        self.ventana.blit(superficie, rect)
        return rect
    
    # Parametros: texto (str), y (int), seleccionada (bool)
    # Retorno: None
    def dibujar_opcion(self, texto, y, seleccionada):  # Pinta opción y cuadrado activo
        """Dibuja una opción del menú con indicador"""
        color = AMARILLO if seleccionada else BLANCO
        superficie = FUENTE_MENU.render(texto, True, color)
        rect = superficie.get_rect(center=(ANCHO // 2, y))
        # Indicador cuadrado discretamente centrado respecto al texto
        if seleccionada:
            indicador_w = 12
            indicador_h = 12
            indicador_x = rect.left - 24
            indicador_y = rect.centery - indicador_h // 2
            p.draw.rect(self.ventana, CIAN, (indicador_x, indicador_y, indicador_w, indicador_h))
        self.ventana.blit(superficie, rect)
    
    # Parametros: ninguno
    # Retorno: None
    def dibujar_cuadricula_fondo(self):  # Fondo rejilla decorativa
        """Dibuja una cuadrícula de fondo"""
        tamaño_grid = 50
        
        for x in range(0, ANCHO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (x, 0), (x, ALTO), 1)
        
        for y in range(0, ALTO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (0, y), (ANCHO, y), 1)
    
    # Parametros: x,y (int), ancho,alto (int)
    # Retorno: None
    def dibujar_borde_decorativo(self, x, y, ancho, alto):  # Marco simple con color CIAN
        """Dibuja un borde decorativo"""
        p.draw.rect(self.ventana, CIAN, (x, y, ancho, alto), 2)


class MenuInicio(Menu):  # Menú principal: START, VESTUARIO, QUIT
    """Menú principal con opciones START, VESTUARIO y QUIT"""
    # Parametros: ventana (pygame.Surface)
    # Retorno: None
    def __init__(self, ventana):  # Define lista de opciones y selección
        super().__init__(ventana) # usa el init de la calse menu q es la padre
        self.opciones = ["START", "VESTUARIO", "QUIT"]
        self.opcion_seleccionada = 0
    
    # Parametros: ninguno (usa p.event.get())
    # Retorno: 'quit'|'niveles'|'vestuario'|None
    def manejar_eventos(self):  # Navega con TAB/UP/DOWN y selecciona con ENTER
        """Maneja eventos del menú inicio"""
        for event in p.event.get():
            if event.type == p.QUIT:# la x de la ventana 
                return "quit"
            
            if event.type == p.KEYDOWN: #entra si un boton es pulsado
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
    
    # Parametros: ninguno
    # Retorno: None
    def dibujar(self):  # Fondo, títulos, opciones y ayudas
        """Dibuja el menú de inicio"""
        # Fondo de pantalla de inicio
        try:
                fondo = p.image.load(FONDOS["inicio"]).convert()
                self.ventana.blit(p.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))
        except Exception:
            self.ventana.fill(FONDO_OSCURO)
            self.dibujar_cuadricula_fondo()
        
        # Título
        self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 80)
        self.dibujar_texto_centrado("MENU PRINCIPAL", FUENTE_MENU, VERDE, 160)
        
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
        self.dibujar_texto_centrado("TAB: Navegar  |  ENTER: Seleccionar", 
            FUENTE_PEQUENA, BLANCO, ALTO - 40)
        
        p.display.flip()

class MenuNiveles(Menu):  # Selector de nivel (1..5) o volver
    """Menú para seleccionar uno de los 5 niveles disponibles"""
    # Parametros: ventana (pygame.Surface)
    # Retorno: None
    def __init__(self, ventana):  # Crea opciones desde config.NIVELES
        super().__init__(ventana)
        # Crear opciones dinámicamente desde config
        self.opciones = [f"Nivel {i} - {NIVELES[i]['nombre']}" for i in range(1, 6)]
        self.opciones.append("<- Volver al Menú Principal")
        self.opcion_seleccionada = 0
    
    # Parametros: ninguno
    # Retorno: 'quit'|'menu_inicio'|('juego',nivel)|None
    def manejar_eventos(self):  # Devuelve ("juego", nivel) o back/quit
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
    
    # Parametros: ninguno
    # Retorno: None
    def dibujar(self):  # Fondo niveles, títulos y lista con selección
        # Fondo del selector de niveles
        try:
            fondo = p.image.load(FONDOS["niveles"]).convert()
            self.ventana.blit(p.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))
        except Exception:
            self.ventana.fill(FONDO_OSCURO)
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
        self.dibujar_texto_centrado("TAB/UP-DOWN: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
            FUENTE_PEQUENA, BLANCO, ALTO - 40)
        
        p.display.flip()


class MenuVestuario(Menu):  # Dos fases: elegir nave y luego balas
    """Menú para seleccionar nave y tipo de bala en dos fases"""
    # Parametros: ventana (pygame.Surface)
    # Retorno: None
    def __init__(self, ventana):  # Carga previews y estado fase/selección
        super().__init__(ventana)
        self.fase = "nave"  # "nave" o "bala"
        self.nave_seleccionada = 1
        self.bala_seleccionada = 1
        self.opcion_seleccionada = 0
        # Previews de naves y balas
        self.preview_naves = {}
        self.preview_balas = {}
        try:
            # Previews de naves: tamaño fijo 70x100
            for i in range(1, 4):
                img = p.image.load(NAVES[i]["sprite"]).convert_alpha()
                self.preview_naves[i] = p.transform.smoothscale(img, (70, 100))
            # Previews de balas: preservar aspecto dentro de caja max 60x120 (mas grandes)
            for i in range(1, 4):
                img = p.image.load(BALAS[i]["sprite"]).convert_alpha()
                max_w, max_h = 60, 120
                ow, oh = img.get_size()
                escala = min(max_w / ow, max_h / oh)
                nw = max(8, int(ow * escala))
                nh = max(12, int(oh * escala))
                self.preview_balas[i] = p.transform.smoothscale(img, (nw, nh))
        except Exception:
            pass
    
    # Parametros: ninguno
    # Retorno: 'quit'|'menu_inicio'|('vestuario_completo',nave,bala)|None
    def manejar_eventos(self):  # Control de TAB/UP/DOWN/ENTER/ESC entre fases
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
    
    # Parametros: ninguno
    # Retorno: None
    def dibujar(self):  # Pinta fondo, títulos, previews y opciones
        """Dibuja el menú de vestuario"""
        # Fondo del vestuario: reutiliza fondo de inicio
        try:
            fondo = p.image.load(FONDOS["inicio"]).convert()
            self.ventana.blit(p.transform.scale(fondo, (ANCHO, ALTO)), (0, 0))
        except Exception:
            self.ventana.fill(FONDO_OSCURO)
            self.dibujar_cuadricula_fondo()
        
        y_inicio = 220
        espaciado = 100
        ancho_caja = 500
        
        if self.fase == "nave":
            # Títulos
            self.dibujar_texto_centrado("SPACE SHOOTER", FUENTE_TITULO, AZUL, 40)
            self.dibujar_texto_centrado("ELIGE TU NAVE", FUENTE_MENU, VERDE, 140)
            # Previsualización fila superior de las naves
            try:
                base_y = 200
                pos_x = [ANCHO//2 - 220, ANCHO//2, ANCHO//2 + 220]
                for i in range(1, 4):
                    surf = self.preview_naves.get(i)
                    if surf:
                        rect = surf.get_rect(center=(pos_x[i-1], base_y))
                        self.ventana.blit(surf, rect)
                        # Etiqueta bajo cada preview
                        nombre = NAVES[i]['nombre']
                        etiqueta = FUENTE_PEQUENA.render(nombre, True, BLANCO)
                        etiqueta_rect = etiqueta.get_rect(center=(pos_x[i-1], base_y + 70))
                        self.ventana.blit(etiqueta, etiqueta_rect)
            except Exception:
                pass

            opciones = [
                f"Nave 1 - {NAVES[1]['nombre']} (Velocidad: {NAVES[1]['velocidad']})",
                f"Nave 2 - {NAVES[2]['nombre']} (Velocidad: {NAVES[2]['velocidad']})",
                f"Nave 3 - {NAVES[3]['nombre']} (Velocidad: {NAVES[3]['velocidad']})",
                "<- Volver al Menú Principal"
            ]
            
            # Empuja opciones hacia abajo para no colapsar con previews
            y_inicio = 320
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
            self.dibujar_texto_centrado("ELIGE TUS BALAS", FUENTE_MENU, ROJO, 140)
            
            # Info nave seleccionada (subimos para no tapar la segunda bala)
            nave_info = f"Nave: {NAVES[self.nave_seleccionada]['nombre']}"
            self.dibujar_texto_centrado(nave_info, FUENTE_PEQUENA, VERDE, 170)
            
            # Previsualización fila superior de balas
            try:
                base_y = 240
                pos_x = [ANCHO//2 - 220, ANCHO//2, ANCHO//2 + 220]
                for i in range(1, 4):
                    surf = self.preview_balas.get(i)
                    if surf:
                        rect = surf.get_rect(center=(pos_x[i-1], base_y))
                        self.ventana.blit(surf, rect)
                        nombre = BALAS[i]['nombre']
                        etiqueta = FUENTE_PEQUENA.render(nombre, True, BLANCO)
                        etiqueta_rect = etiqueta.get_rect(center=(pos_x[i-1], base_y + 85))
                        self.ventana.blit(etiqueta, etiqueta_rect)
            except Exception:
                pass
            
            opciones = [
                f"Balas 1 - {BALAS[1]['nombre']} (Daño: {BALAS[1]['daño']})",
                f"Balas 2 - {BALAS[2]['nombre']} (Daño: {BALAS[2]['daño']})",
                f"Balas 3 - {BALAS[3]['nombre']} (Daño: {BALAS[3]['daño']})",
                "<- Volver a Elegir Nave"
            ]
            
            y_inicio = 360
            for i, opcion in enumerate(opciones):
                y_opcion = y_inicio + i * espaciado
                
                # Fondo de opción seleccionada
                if i == self.opcion_seleccionada:
                    p.draw.rect(self.ventana, GRIS_OSCURO, (50, y_opcion - 30, ancho_caja, 60))
                    p.draw.rect(self.ventana, CIAN, (50, y_opcion - 30, ancho_caja, 60), 2)
                
                self.dibujar_opcion(opcion, y_opcion, i == self.opcion_seleccionada)
        
        # Instrucciones
        self.dibujar_texto_centrado("TAB: Navegar  |  ENTER: Seleccionar  |  ESC: Volver", 
            FUENTE_PEQUENA, BLANCO, ALTO - 40)
        
        p.display.flip()