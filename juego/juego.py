import pygame as p
from .config import *
import random
import math
# test para comprobar git

class Juego:
    """Clase principal del juego con enemigos avanzados"""
    
    def __init__(self, ventana, nivel, nave_tipo, bala_tipo):
        self.ventana = ventana
        self.nivel = nivel
        self.nave_tipo = nave_tipo
        self.bala_tipo = bala_tipo
        
        # Configuracion del nivel
        self.config_nivel = NIVELES[nivel]
        
        # Posicion nave jugador
        self.nave_x = ANCHO // 2 - 25
        self.nave_y = ALTO - 100
        
        # Velocidad nave
        self.velocidad_nave = NAVES[nave_tipo]["velocidad"]
        self.velocidad_bala = BALAS[bala_tipo]["velocidadB"]
        
        # Vida
        self.vida_nave = 5
        self.vida_maxima = 5
        
        # Puntuacion
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
        # Rect del botón final (se asigna en el dibujo de pantalla final)
        self.final_button_rect = None
    
    def cargar_recursos(self):
        """Carga todas las imagenes necesarias"""
        # Nave del jugador
        self.nave_img = p.image.load(NAVES[self.nave_tipo]["sprite"]).convert_alpha()
        self.nave_img = p.transform.scale(self.nave_img, (50, 80))
        
        # Bala del jugador
        bala_size = BALAS[self.bala_tipo]["tamaño"]
        self.bala_img = p.image.load(BALAS[self.bala_tipo]["sprite"]).convert_alpha()
        self.bala_img = p.transform.scale(self.bala_img, bala_size)
        
        # Enemigo
        self.enemigo_img = p.image.load(ENEMIGOS["normal"]).convert_alpha()
        self.enemigo_img = p.transform.scale(self.enemigo_img, (50, 50))
        
        # Bala enemiga
        self.bala_enemiga_img = p.image.load(ENEMIGOS["boss"]).convert_alpha()
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

            # Si estamos en estado final (victoria/derrota) cualquier tecla
            # o clic debe devolver al menú de niveles.
            if self.victoria or self.vida_nave <= 0:
                # Registro para depuración: entrada a handler final
                msg = f"[DEBUG] manejar_eventos: estado final detectado, evento: {event.type}\n"
                print(msg, end="")
                try:
                    with open("debug_game.log", "a", encoding="utf-8") as _f:
                        _f.write(msg)
                except Exception:
                    pass
                if event.type == p.KEYDOWN or event.type == p.MOUSEBUTTONDOWN:
                    msg2 = "[DEBUG] manejar_eventos: evento final -> volver a niveles\n"
                    print(msg2, end="")
                    try:
                        with open("debug_game.log", "a", encoding="utf-8") as _f:
                            _f.write(msg2)
                    except Exception:
                        pass
                    return "niveles"

            # En juego activo, procesar controles normales
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
        for bala in self.balas_jugador[:]:
            bala["y"] += bala["vy"]
            if bala["y"] < 0:
                self.balas_jugador.remove(bala)
        
        for bala in self.balas_enemigo[:]:
            bala["x"] += bala["vx"]
            bala["y"] += bala["vy"]
            if bala["y"] < 0 or bala["y"] > ALTO or bala["x"] < 0 or bala["x"] > ANCHO:
                self.balas_enemigo.remove(bala)
    
    def mover_enemigos(self):
        """Mueve los enemigos"""
        velocidad_movimiento = self.config_nivel["velocidad_enemigo"]
        
        for enemigo in self.enemigos:
            if velocidad_movimiento > 0:
                enemigo["x"] += enemigo["vx"] * velocidad_movimiento
                
                if enemigo["x"] < 10 or enemigo["x"] > ANCHO - 60:
                    enemigo["vx"] *= -1
            
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
                        
                        explosion = {
                            "x": enemigo["x"],
                            "y": enemigo["y"],
                            "frame_actual": 0,
                            "contador_frames": 0
                        }
                        self.explosiones.append(explosion)
                        self.enemigos.remove(enemigo)
                    break
        
        for bala in self.balas_enemigo[:]:
            nave_rect = p.Rect(self.nave_x, self.nave_y, 50, 80)
            bala_rect = p.Rect(bala["x"], bala["y"], 10, 15)
            
            if bala_rect.colliderect(nave_rect):
                self.balas_enemigo.remove(bala)
                self.vida_nave -= 1
                
                explosion = {
                    "x": self.nave_x,
                    "y": self.nave_y,
                    "frame_actual": 0,
                    "contador_frames": 0
                }
                self.explosiones.append(explosion)
                break
    
    def verificar_victoria(self):
        """Verifica si se alcanzo el objetivo"""
        if self.score >= self.objetivo_puntos and len(self.enemigos) == 0:
            self.victoria = True
            return True
        return False
    
    def dibujar(self):
        """Dibuja todos los elementos del juego"""
        self.ventana.fill(FONDO_OSCURO)
        
        self.dibujar_cuadricula()
        
        for enemigo in self.enemigos:
            self.ventana.blit(self.enemigo_img, (enemigo["x"], enemigo["y"]))
            
            self.dibujar_barra_vida(enemigo["x"], enemigo["y"] - 10, 
                                   enemigo["vida"], enemigo["vida_maxima"])
        
        for bala in self.balas_jugador:
            self.ventana.blit(self.bala_img, (bala["x"], bala["y"]))
        
        for bala in self.balas_enemigo:
            p.draw.circle(self.ventana, ROJO, (int(bala["x"]), int(bala["y"])), 5)
        
        for explosion in self.explosiones:
            self.ventana.blit(self.explosion_imgs[explosion["frame_actual"]],
                             (explosion["x"], explosion["y"]))
        
        self.ventana.blit(self.nave_img, (self.nave_x, self.nave_y))
        
        self.dibujar_hud()
        
        if self.victoria:
            self.dibujar_victoria()
        
        if self.vida_nave <= 0:
            self.dibujar_derrota()
        
        p.display.flip()
    
    def dibujar_cuadricula(self):
        """Dibuja una cuadricula de fondo"""
        tamaño_grid = 40
        
        for x in range(0, ANCHO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (x, 0), (x, ALTO))
        
        for y in range(0, ALTO, tamaño_grid):
            p.draw.line(self.ventana, GRIS_OSCURO, (0, y), (ANCHO, y))
    
    def dibujar_barra_vida(self, x, y, vida, vida_max):
        """Dibuja una barra de vida"""
        ancho_barra = 50
        alto_barra = 5
        
        p.draw.rect(self.ventana, ROJO, (x, y, ancho_barra, alto_barra))
        
        vida_porcentaje = (vida / vida_max) * ancho_barra
        p.draw.rect(self.ventana, VERDE, (x, y, vida_porcentaje, alto_barra))
    
    def dibujar_hud(self):
        """Dibuja la interfaz del juego"""
        score_text = FUENTE_HUD.render(f"Score: {self.score}/{self.objetivo_puntos}", True, AMARILLO)
        self.ventana.blit(score_text, (10, 10))
        
        vida_text = FUENTE_HUD.render(f"Vida: {self.vida_nave}/{self.vida_maxima}", True, ROJO)
        self.ventana.blit(vida_text, (10, 45))
        
        nivel_text = FUENTE_HUD.render(f"Nivel {self.nivel}: {self.config_nivel['nombre']}", True, CIAN)
        self.ventana.blit(nivel_text, (10, 80))
        
        enemigos_text = FUENTE_HUD.render(f"Enemigos: {len(self.enemigos)}", True, VERDE)
        self.ventana.blit(enemigos_text, (10, 115))
        
        ayuda_text = FUENTE_PEQUEÑA.render("ESPACIO: Disparar | FLECHAS: Mover | ESC: MENU", True, BLANCO)
        self.ventana.blit(ayuda_text, (10, ALTO - 30))
    
    def dibujar_victoria(self):
        """Dibuja la pantalla de victoria"""
        overlay = p.Surface((ANCHO, ALTO))
        overlay.set_alpha(200)
        overlay.fill(NEGRO)
        self.ventana.blit(overlay, (0, 0))
        
        victoria_text = FUENTE_TITULO.render("VICTORIA", True, VERDE)
        rect = victoria_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        self.ventana.blit(victoria_text, rect)
        
        info_text = FUENTE_MENU.render(f"SCORE: {self.score}", True, AMARILLO)
        rect = info_text.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.ventana.blit(info_text, rect)
        
        # Texto informativo (seguro): también dibujamos un botón "VOLVER"
        instruc_text = FUENTE_TEXTO.render("Pulsa cualquier tecla o clic -> VOLVER", True, BLANCO)
        rect = instruc_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
        self.ventana.blit(instruc_text, rect)

        # Botón visible para volver
        btn_w, btn_h = 220, 60
        btn_x = ANCHO // 2 - btn_w // 2
        btn_y = ALTO // 2 + 90
        mouse_pos = p.mouse.get_pos()
        hover = p.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos)
        btn_color = GRIS_CLARO if hover else GRIS_OSCURO
        p.draw.rect(self.ventana, btn_color, (btn_x, btn_y, btn_w, btn_h))
        p.draw.rect(self.ventana, CIAN, (btn_x, btn_y, btn_w, btn_h), 2)

        btn_text = FUENTE_MENU.render("VOLVER", True, BLANCO)
        btn_rect = btn_text.get_rect(center=(ANCHO // 2, btn_y + btn_h // 2))
        self.ventana.blit(btn_text, btn_rect)

        # Guardar rect para posible uso en eventos
        self.final_button_rect = p.Rect(btn_x, btn_y, btn_w, btn_h)
    
    def dibujar_derrota(self):
        """Dibuja la pantalla de derrota"""
        overlay = p.Surface((ANCHO, ALTO))
        overlay.set_alpha(200)
        overlay.fill(NEGRO)
        self.ventana.blit(overlay, (0, 0))

        derrota_text = FUENTE_TITULO.render("DERROTA", True, ROJO)
        rect = derrota_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 100))
        self.ventana.blit(derrota_text, rect)

        info_text = FUENTE_MENU.render(f"SCORE: {self.score}", True, AMARILLO)
        rect = info_text.get_rect(center=(ANCHO // 2, ALTO // 2))
        self.ventana.blit(info_text, rect)

        # Texto informativo (seguro): también dibujamos un botón "VOLVER"
        instruc_text = FUENTE_TEXTO.render("PULSA UNA TECLA O CLIC EN 'VOLVER'", True, BLANCO)
        rect = instruc_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 60))
        self.ventana.blit(instruc_text, rect)

        # Botón visible para volver
        btn_w, btn_h = 220, 60
        btn_x = ANCHO // 2 - btn_w // 2
        btn_y = ALTO // 2 + 90
        mouse_pos = p.mouse.get_pos()
        hover = p.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(mouse_pos)
        btn_color = GRIS_CLARO if hover else GRIS_OSCURO
        p.draw.rect(self.ventana, btn_color, (btn_x, btn_y, btn_w, btn_h))
        p.draw.rect(self.ventana, CIAN, (btn_x, btn_y, btn_w, btn_h), 2)

        btn_text = FUENTE_MENU.render("VOLVER", True, BLANCO)
        btn_rect = btn_text.get_rect(center=(ANCHO // 2, btn_y + btn_h // 2))
        self.ventana.blit(btn_text, btn_rect)

        # Guardar rect para posible uso en eventos
        self.final_button_rect = p.Rect(btn_x, btn_y, btn_w, btn_h)
    
    def ejecutar(self):
        """Bucle principal del juego"""
        reloj = p.time.Clock()
        pantalla_final_esperando = False
        
        while self.ejecutandose:
            # Si estamos en pantalla final, esperar a cualquier evento (tecla o click)
            if (self.victoria or self.vida_nave <= 0) and not pantalla_final_esperando:
                pantalla_final_esperando = True
                self.dibujar()
                p.display.flip()
                
                # Bloquear y esperar evento en pantalla final
                while True:
                    evt = p.event.wait()
                    if evt.type == p.QUIT:
                        return "quit"
                    if evt.type == p.KEYDOWN or evt.type == p.MOUSEBUTTONDOWN:
                        return "niveles"
            
            # Gameplay normal
            resultado = self.manejar_eventos()
            if resultado:
                return resultado
            
            if self.vida_nave > 0 and not self.victoria:
                self.mover_nave()
                self.mover_balas()
                self.mover_enemigos()
                self.actualizar_explosiones()
                self.detectar_colisiones()
                self.verificar_victoria()
            
            self.dibujar()
            reloj.tick(100)
        
        return "menu_inicio"
