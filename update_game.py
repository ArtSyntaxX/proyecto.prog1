#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para actualizar la función ejecutar() en juego.py"""

# Leer el archivo actual
with open('juego/juego.py', 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Buscar donde está la función ejecutar
inicio = None
for i, linea in enumerate(lineas):
    if 'def ejecutar(self):' in linea:
        inicio = i
        break

if inicio is None:
    print("No se encontró la función ejecutar")
    exit(1)

# Encontrar dónde termina (siguiente def o EOF)
fin = len(lineas)
for i in range(inicio + 1, len(lineas)):
    if lineas[i].strip().startswith('def ') and not lineas[i].strip().startswith('"""'):
        fin = i
        break

print(f"Función ejecutar: líneas {inicio+1} a {fin}")

# Nueva función
nueva_func = '''    def ejecutar(self):
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

        return "menu_inicio"

'''

# Reemplazar
nuevo_contenido = ''.join(lineas[:inicio]) + nueva_func + ''.join(lineas[fin:])

# Escribir
with open('juego/juego.py', 'w', encoding='utf-8') as f:
    f.write(nuevo_contenido)

print("Archivo actualizado correctamente")
