import pygame as p
from config import *
import random
import math


class Juego:
    """Clase principal del juego con enemigos avanzados"""
    
    def __init__(self, ventana, nivel, nave_tipo, bala_tipo):
        self.ventana = ventana
        self.nivel = nivel
        self.nave_tipo = nave_tipo
        self.bala_tipo = bala_tipo
        self.fondo = p.image.load(FONDOS_NIVELES[nivel])
        self.fondo = p.transform.scale(self.fondo, (ANCHO, ALTO))
        
        # Configuración del nivel
        self.config_nivel = NIVELES[nivel]
        
        # Posición nave jugador
        self.nave_x = ANCHO // 2 - 25
        self.nave_y = ALTO - 100
        
        # Velocidad nave
        self.velocidad_nave = NAVES[nave_tipo]["velocidad"]
        self.velocidad_bala = BALAS[bala_tipo]["velocidadB"]
        
        # Vida
        self.vida_nave = 5
        self.vida_maxima = 5
        
        # Puntuación
        self.score = 0
        self.objetivo_puntos = self.config_nivel["objetivo_puntos"]
        self.enemigos_derrotados = 0
        
        # Recursos
        self.cargar_recursos()
        
        # Balas
        self.balas_jugador = []
        self.balas_enemigo = []
        
        # Enemigos
        self.enemigos = []
        self.crear_oleada_enemigos()
        
        # Explosiones
        self.explosiones = []
        
        # Control
        self.ejecutandose = True
        self.victoria = False
        self.contador_victoria = 0
        self.contador_disparo_enemigo = 0
    
    def cargar_recursos(self):
        """Carga todas las imágenes necesarias"""
        # Nave del jugador
        self.nave_img = p.image.load(NAVES[self.nave_tipo]["sprite"]).convert_alpha()
        self.nave_img = p.transform.scale(self.nave_img, (50, 80))
        
        # Bala del jugador
        bala_size = BALAS[self.bala_tipo]["tamaño"]
        self.bala_img = p.image.load(BALAS[self.bala_tipo]["sprite"]).convert_alpha()
        self.bala_img = p.transform.scale(self.bala_img, bala_size)
        
        # Enemigo
        self.enemigo_img = p.image.load(ENEMIGOS[self.nivel]).convert_alpha()
        self.enemigo_img = p.transform.scale(self.enemigo_img, (50, 50))
        
        # Bala enemiga
        self.bala_enemiga_img = p.image.load(BALA_ENEMIGO).convert_alpha()
        self.bala_enemiga_img = p.transform.scale(self.bala_enemiga_img, (10, 15))
        
        # Explosiones
        self.explosion_imgs = []
        for i in range(1, 6):
            img = p.image.load(f"recursos/explosion/exp2_0{i}.png").convert_alpha()
            img = p.transform.scale(img, (70, 70))
            self.explosion_imgs.append(img)
    
    def crear_oleada_enemigos(self):
        """Crea una oleada de enemigos"""
        self.enemigos = []
        num_enemigos = self.config_nivel["enemigos"]
        vida_enemigo = self.config_nivel["vida_enemigo"]
        enemigo_img = p.image.load(ENEMIGOS[self.nivel]).convert_alpha()
        enemigo_img = p.transform.scale(enemigo_img, (50, 50))
        
        # Distribuir enemigos en la pantalla
        for i in range(num_enemigos):
            x = (ANCHO // (num_enemigos + 1)) * (i + 1)
            y = 50 + (i % 3) * 80
            
            enemigo = {
                "x": x,
                "y": y,
                "vx": random.choice([-2, 2]) if self.config_nivel["velocidad_enemigo"] > 0 else 0,
                "vy": 0,
                "vida": vida_enemigo,
                "vida_maxima": vida_enemigo,
                "contador_disparo": random.randint(50, 150)
            }
            self.enemigos.append(enemigo)
    
    def manejar_eventos(self):
        """Maneja eventos del jugador"""
        for event in p.event.get():
            if event.type == p.QUIT:
                return "quit"
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    self.disparar_jugador()
                elif event.key == p.K_ESCAPE:
                    return "menu_inicio"
        
        return None
    
    def disparar_jugador(self):
        """Crea una bala del jugador"""
        bala = {
            "x": self.nave_x + 25,
            "y": self.nave_y,
            "vx": 0,
            "vy": -self.velocidad_bala,
            "tipo": "jugador"
        }
        self.balas_jugador.append(bala)
    
    def disparar_enemigo(self, enemigo):
        """Crea una bala de enemigo"""
        if not self.config_nivel["pueden_disparar"]:
            return
        
        # Calcular dirección hacia el jugador
        dx = self.nave_x - enemigo["x"]
        dy = self.nave_y - enemigo["y"]
        distancia = math.sqrt(dx**2 + dy**2)
        
        if distancia > 0:
            vx = (dx / distancia) * 3
            vy = (dy / distancia) * 3
        else:
            vx, vy = 0, 3
        
        bala = {
            "x": enemigo["x"] + 25,
            "y": enemigo["y"] + 25,
            "vx": vx,
            "vy": vy,
            "tipo": "enemigo"
        }
        self.balas_enemigo.append(bala)
    
    def mover_nave(self):
        """Mueve la nave del jugador"""
        teclas = p.key.get_pressed()
        
        if teclas[p.K_LEFT] and self.nave_x > 5:
            self.nave_x -= self.velocidad_nave
        if teclas[p.K_RIGHT] and self.nave_x < ANCHO - 55:
            self.nave_x += self.velocidad_nave
        if teclas[p.K_UP] and self.nave_y > 100:
            self.nave_y -= self.velocidad_nave
        if teclas[p.K_DOWN] and self.nave_y < ALTO - 85:
            self.nave_y += self.velocidad_nave
    
    def mover_balas(self):
        """Mueve todas las balas"""
        # Balas del jugador
        for bala in self.balas_jugador[:]:
            bala["y"] += bala["vy"]
            if bala["y"] < 0:
                self.balas_jugador.remove(bala)
        
        # Balas del enemigo
        for bala in self.balas_enemigo[:]:
            bala["x"] += bala["vx"]
            bala["y"] += bala["vy"]
            if bala["y"] < 0 or bala["y"] > ALTO or bala["x"] < 0 or bala["x"] > ANCHO:
                self.balas_enemigo.remove(bala)
    
    def mover_enemigos(self):
        """Mueve los enemigos"""
        velocidad_movimiento = self.config_nivel["velocidad_enemigo"]
        
        for enemigo in self.enemigos:
            # Movimiento horizontal
            if velocidad_movimiento > 0:
                enemigo["x"] += enemigo["vx"] * velocidad_movimiento
                
                # Rebotar en los bordes
                if enemigo["x"] < 10 or enemigo["x"] > ANCHO - 60:
                    enemigo["vx"] *= -1
            
            # Disparo
            if self.config_nivel["pueden_disparar"]:
                enemigo["contador_disparo"] -= 1
                if enemigo["contador_disparo"] <= 0:
                    self.disparar_enemigo(enemigo)
                    enemigo["contador_disparo"] = random.randint(60, 120)
    
    def actualizar_explosiones(self):
        """Actualiza las animaciones de explosiones"""
        for explosion in self.explosiones[:]:
            explosion["contador_frames"] += 1
            
            if explosion["contador_frames"] >= 8:
                explosion["contador_frames"] = 0
                explosion["frame_actual"] += 1
            
            if explosion["frame_actual"] >= len(self.explosion_imgs):
                self.explosiones.remove(explosion)
    
    def detectar_colisiones(self):
        """Detecta todas las colisiones"""
        daño_bala = BALAS[self.bala_tipo]["daño"]
        
        # Colisiones: balas del jugador con enemigos
        for bala in self.balas_jugador[:]:
            for enemigo in self.enemigos[:]:
                bala_rect = p.Rect(bala["x"], bala["y"], 10, 15)
                enemigo_rect = p.Rect(enemigo["x"], enemigo["y"], 50, 50)
                
                if bala_rect.colliderect(enemigo_rect):
                    if bala in self.balas_jugador:
                        self.balas_jugador.remove(bala)
                    
                    enemigo["vida"] -= daño_bala
                    
                    if enemigo["vida"] <= 0:
                        self.score += 10
                        self.enemigos_derrotados += 1
                        
                        # Explosión
                        explosion = {
                            "x": enemigo["x"],
                            "y": enemigo["y"],
                            "frame_actual": 0,
                            "contador_frames": 0
                        }
                        self.explosiones.append(explosion)
                        self.enemigos.remove(enemigo)
                    break
        
        # Colisiones: balas enemiga con nave
        for bala in self.balas_enemigo[:]:
            nave_rect = p.Rect(self.nave_x, self.nave_y, 50, 80)
            bala_rect = p.Rect(bala["x"], bala["y"], 10, 15)
            
            if bala_rect.colliderect(nave_rect):
                self.balas_enemigo.remove(bala)
                self.vida_nave -= 1
                
                # Explosión en la nave
                explosion = {
                    "x": self.nave_x,
                    "y": self.nave_y,
                    "frame_actual": 0,
                    "contador_frames": 0
                }
                self.explosiones.append(explosion)
                break
    
    def verificar_victoria(self):
        """Verifica si se alcanzó el objetivo"""
        if self.score >= self.objetivo_puntos and len(self.enemigos) == 0:
            self.victoria = True
            return True
        return False
    
    def dibujar(self):
        """Dibuja todos los elementos del juego"""
        # Dibujar fondo del nivel
        self.ventana.blit(self.fondo, (0, 0))

        
        # Cuadrícula de fondo
        self.dibujar_cuadricula()
        
        # Enemigos
        for enemigo in self.enemigos:
            self.ventana.blit(self.enemigo_img, (enemigo["x"], enemigo["y"]))
            
            # Barra de vida del enemigo
            self.dibujar_barra_vida(enemigo["x"], enemigo["y"] - 10, 
                                   enemigo["vida"], enemigo["vida_maxima"])
        
        # Balas del jugador
        for bala in self.balas_jugador:
            self.ventana.blit(self.bala_img, (bala["x"], bala["y"]))
        
        # Balas del enemigo
        for bala in self.balas_enemigo:
            p.draw.circle(self.ventana, ROJO, (int(bala["x"]), int(bala["y"])), 5)
        
        # Explosiones
        for explosion in self.explosiones:
            self.ventana.blit(self.explosion_imgs[explosion["frame_actual"]],
                             (explosion["x"], explosion["y"]))
        
        # Nave del jugador
        self.ventana.blit(self.nave_img, (self.nave_x, self.nave_y))
        
        # HUD
        self.dibujar_hud()
        
        # Pantalla de victoria
        if self.victoria:
            self.dibujar_victoria()
        
        # Pantalla de derrota
        if self.vida_nave <= 0:
            self.dibujar_derrota()
        
        p.display.flip()
    
    def dibujar_cuadricula(self):
        """Dibuja una cuadrícula de fondo"""
        tamaño_grid = 40
        
        for x in range(0, ANCHO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (x, 0), (x, ALTO))
        
        for y in range(0, ALTO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (0, y), (ANCHO, y))
    
    def dibujar_barra_vida(self, x, y, vida, vida_max):
        """Dibuja una barra de vida"""
        ancho_barra = 50
        alto_barra = 5
        
        # Fondo rojo
        p.draw.rect(self.ventana, ROJO, (x, y, ancho_barra, alto_barra))
        
        # Vida en verde
        vida_porcentaje = (vida / vida_max) * ancho_barra
        p.draw.rect(self.ventana, VERDE, (x, y, vida_porcentaje, alto_barra))
    
    def dibujar_hud(self):
        """Dibuja la interfaz del juego"""
        # Score
        score_text = FUENTE_HUD.render(f"⭐ Score: {self.score}/{self.objetivo_puntos}", True, AMARILLO)
        self.ventana.blit(score_text, (10, 10))
        
        # Vida
        vida_text = FUENTE_HUD.render(f"❤ Vida: {self.vida_nave}/{self.vida_maxima}", True, ROJO)
        self.ventana.blit(vida_text, (10, 45))
        
        # Nivel
        nivel_text = FUENTE_HUD.render(f"Nivel {self.nivel}: {self.config_nivel['nombre']}", True, CIAN)
        self.ventana.blit(nivel_text, (10, 80))
        
        # Enemigos restantes
        enemigos_text = FUENTE_HUD.render(f"Enemigos: {len(self.enemigos)}", True, VERDE)
        self.ventana.blit(enemigos_text, (10, 115))
        
        # Ayuda
        ayuda_text = FUENTE_PEQUEÑA.render("ESPACIO: Disparar | FLECHAS: Mover | ESC: Menú", True, BLANCO)
        self.ventana.blit(ayuda_text, (10, ALTO - 30))
    
    def dibujar_victoria(self):
        """Dibuja la pantalla de victoria"""
        # Fondo semi-transparente
        overlay = p.Surface((ANCHO, ALTO))
        overlay.set_alpha(200)
        overlay.fill(NEGRO)
        self.ventana.blit(overlay, (0, 0))
        
        # Texto de victoria
        victoria_text = FUENTE_TITULO.render("¡VICTORIA!", True, VERDE)
        rect = victoria_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        self.ventana.blit(victoria_text, rect)
        
        # Información
        info_text = FUENTE_MENU.render(f"Puntuación: {self.score}", True, AMARILLO)
        rect = info_text.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.ventana.blit(info_text, rect)
        
        # Instrucciones
        instruc_text = FUENTE_TEXTO.render("ENTER: Volver a niveles | ESC: Menú", True, BLANCO)
        rect = instruc_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
        self.ventana.blit(instruc_text, rect)
    
    def dibujar_derrota(self):
        """Dibuja la pantalla de derrota"""
        # Fondo semi-transparente
        overlay = p.Surface((ANCHO, ALTO))
        overlay.set_alpha(200)
        overlay.fill(NEGRO)
        self.ventana.blit(overlay, (0, 0))
        
        # Texto de derrota
        derrota_text = FUENTE_TITULO.render("¡DERROTA!", True, ROJO)
        rect = derrota_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        self.ventana.blit(derrota_text, rect)
        
        # Información
        info_text = FUENTE_MENU.render(f"Puntuación: {self.score}", True, AMARILLO)
        rect = info_text.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.ventana.blit(info_text, rect)
        
        # Instrucciones
        instruc_text = FUENTE_TEXTO.render("ENTER: Reintentar | ESC: Menú", True, BLANCO)
        rect = instruc_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
        self.ventana.blit(instruc_text, rect)
    
    def ejecutar(self):
        """Bucle principal del juego"""
        reloj = p.time.Clock()
        
        while self.ejecutandose:
            # Manejo de eventos
            resultado = self.manejar_eventos()
            if resultado:
                return resultado
            
            # Lógica del juego
            if self.vida_nave > 0 and not self.victoria:
                self.mover_nave()
                self.mover_balas()
                self.mover_enemigos()
                self.actualizar_explosiones()
                self.detectar_colisiones()
                self.verificar_victoria()
            
            # Pantallas finales
            if self.victoria or self.vida_nave <= 0:
                for event in p.event.get():
                    if event.type == p.QUIT:
                        return "quit"
                    if event.type == p.KEYDOWN:
                        if event.key == p.K_RETURN:
                            return "niveles"
                        elif event.key == p.K_ESCAPE:
                            return "menu_inicio"
            
            # Dibujo
            self.dibujar()
            
            # FPS
            reloj.tick(100)
        
        return "menu_inicio"