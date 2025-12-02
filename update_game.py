#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para actualizar la función ejecutar() en juego.py"""

with open('juego/juego.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontrar y reemplazar la función ejecutar
old_func = '''    def ejecutar(self):
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

        return "menu_inicio"'''

new_func = '''    def ejecutar(self):
        """Bucle principal del juego"""
        reloj = p.time.Clock()

        while self.ejecutandose:
            # Si estamos en pantalla final, BLOQUEAR y esperar evento
            if self.victoria or self.vida_nave <= 0:
                self.dibujar()
                p.display.flip()
                
                # Esperar bloqueante hasta recibir evento
                while True:
                    evt = p.event.wait()  # BLOQUEA hasta evento
                    
                    if evt.type == p.QUIT:
                        return "quit"
                    
                    if evt.type == p.KEYDOWN:
                        if evt.key == p.K_RETURN:
                            return "niveles"
                        elif evt.key == p.K_ESCAPE:
                            return "menu_inicio"
                    
                    if evt.type == p.MOUSEBUTTONDOWN:
                        return "niveles"
            
            # Manejo de eventos en juego normal
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

            # Dibujo
            self.dibujar()

            # FPS
            reloj.tick(100)

        return "menu_inicio"'''

new_content = content.replace(old_func, new_func)

if new_content == content:
    print("ERROR: Reemplazo no funcionó")
    print("Buscando 'def ejecutar'...")
    if 'def ejecutar' in content:
        idx = content.find('def ejecutar')
        print(f"Encontrado en posición {idx}")
        print("Primeras 300 caracteres después:")
        print(repr(content[idx:idx+300]))
else:
    with open('juego/juego.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("OK: Archivo actualizado exitosamente")
