import pygame as p
from config import *

# ¿Qué poner aquí?
#- Clase Juego
#- Mover nave
#- Disparar balas
#- Mover balas
#- Enemigos
#- Colisiones
#- Explosiones
#- Puntuación
#- Dibujar todo del juego

class Juego:
    def __init__(self, ventana, nivel, nave_tipo, bala_tipo):
        self.ventana = ventana
        self.nivel = nivel
        self.nave_tipo = nave_tipo
        self.bala_tipo = bala_tipo
        
        # Cargar configuración del nivel
        config_nivel = NIVELES[nivel]
        
        # Posición nave
        self.x = 300
        self.y = 650
        
        # Vida
        self.vida_nave = 5
        self.vida_nave_maxima = 5
        
        # Velocidades (según nave elegida)
        self.velocidad = NAVES[nave_tipo]["velocidad"]
        self.velocidadB = 20
        
        # Puntuación
        self.score = 0
        
        # Recursos
        self.cargar_recursos()
        
        # Balas
        self.balas = []
        
        # Enemigo
        self.enemigo = {
            "x": 300,
            "y": 100,
            "ancho": 60,
            "alto": 60,
            "vida": config_nivel["vida_enemigo"],
            "vida_maxima": config_nivel["vida_enemigo"]
        }
        
        # Explosiones
        self.explosiones = []
        
        # Control
        self.ejecutandose = True
    
    def cargar_recursos(self):
        """Carga imágenes y recursos"""
        self.nave_img = p.image.load(NAVES[self.nave_tipo]["sprite"]).convert_alpha()
        self.nave_img = p.transform.scale(self.nave_img, (50, 80))
        
        self.bala_img = p.image.load(BALAS[self.bala_tipo]["sprite"]).convert_alpha()
        self.bala_img = p.transform.scale(self.bala_img, (15, 30))
        
        self.explosion_imgs = []
        for i in range(1, 6):
            img = p.image.load(f"recursos/explosion/exp2_0{i}.png").convert_alpha()
            img = p.transform.scale(img, (70, 70))
            self.explosion_imgs.append(img)
    
    def manejar_eventos(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                return "quit"
            
            if event.type == p.KEYDOWN:
                if event.key == p.K_SPACE:
                    nueva_bala = {"x": self.x + 17, "y": self.y}
                    self.balas.append(nueva_bala)
                
                elif event.key == p.K_ESCAPE:
                    return "menu_inicio"
        
        return None
    
    def mover_nave(self):
        teclas = p.key.get_pressed()
        
        if teclas[p.K_LEFT] and self.x > 5:
            self.x -= self.velocidad
        if teclas[p.K_RIGHT] and self.x < 545:
            self.x += self.velocidad
        if teclas[p.K_UP] and self.y > 550:
            self.y -= self.velocidad
        if teclas[p.K_DOWN] and self.y < 715:
            self.y += self.velocidad
    
    def mover_balas(self):
        for bala in self.balas:
            bala["y"] -= self.velocidadB
        
        self.balas = [b for b in self.balas if b["y"] > 0]
    
    def actualizar_explosiones(self):
        for explosion in self.explosiones[:]:
            explosion["contador_frames"] += 1
            
            if explosion["contador_frames"] >= 10:
                explosion["contador_frames"] = 0
                explosion["frame_actual"] += 1
            
            if explosion["frame_actual"] >= len(self.explosion_imgs):
                self.explosiones.remove(explosion)
    
    def detectar_colisiones(self):
        enemigo_rect = p.Rect(self.enemigo["x"], self.enemigo["y"], 
                             self.enemigo["ancho"], self.enemigo["alto"])
        
        daño_bala = BALAS[self.bala_tipo]["daño"]
        
        for bala in self.balas[:]:
            bala_rect = p.Rect(bala["x"], bala["y"], 15, 30)
            if bala_rect.colliderect(enemigo_rect):
                self.enemigo["vida"] -= daño_bala
                self.balas.remove(bala)
                
                if self.enemigo["vida"] <= 0:
                    self.score += 10
                    
                    nueva_explosion = {
                        "x": self.enemigo["x"],
                        "y": self.enemigo["y"],
                        "frame_actual": 0,
                        "contador_frames": 0
                    }
                    self.explosiones.append(nueva_explosion)
                    
                    self.enemigo["x"] = 300
                    self.enemigo["y"] = 100
                    self.enemigo["vida"] = self.enemigo["vida_maxima"]
    
    def dibujar(self):
        self.ventana.fill(NEGRO)
        
        # Nave
        self.ventana.blit(self.nave_img, (self.x, self.y))
        
        # Enemigo
        p.draw.rect(self.ventana, ROJO, (self.enemigo["x"], self.enemigo["y"], 
                                        self.enemigo["ancho"], self.enemigo["alto"]))
        
        # Explosiones
        for explosion in self.explosiones:
            self.ventana.blit(self.explosion_imgs[explosion["frame_actual"]],
                             (explosion["x"], explosion["y"]))
        
        # Balas
        for bala in self.balas:
            self.ventana.blit(self.bala_img, (bala["x"], bala["y"]))
        
        # HUD
        self.ventana.blit(FUENTE_TEXTO.render(f"Score: {self.score}", True, BLANCO), (10, 10))
        self.ventana.blit(FUENTE_TEXTO.render(f"Vida: {self.vida_nave}/{self.vida_nave_maxima}", True, VERDE), (10, 50))
        self.ventana.blit(FUENTE_TEXTO.render(f"Enemigo: {self.enemigo['vida']}", True, ROJO), (10, 90))
        self.ventana.blit(FUENTE_TEXTO.render(f"Nivel: {self.nivel}", True, AMARILLO), (10, 130))
        self.ventana.blit(FUENTE_TEXTO.render("ESC: Menú", True, BLANCO), (450, 10))
        
        p.display.flip()
    
    def ejecutar(self):
        reloj = p.time.Clock()
        
        while self.ejecutandose:
            resultado = self.manejar_eventos()
            if resultado:
                return resultado
            
            self.mover_nave()
            self.mover_balas()
            self.actualizar_explosiones()
            self.detectar_colisiones()
            self.dibujar()
            
            reloj.tick(100)
        
        return "menu_inicio"