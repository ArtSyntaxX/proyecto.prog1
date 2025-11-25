import pygame as p

# ¿Qué poner aquí?
#- Tamaños de ventana (ANCHO, ALTO)
#- Colores (ROJO, VERDE, AZUL...)
#- Fuentes (FUENTE_TITULO, FUENTE_MENU...)
#- Configuraciones de naves (velocidad, sprite...)
#- Configuraciones de balas (daño, sprite...)
#- Configuraciones de niveles (dificultad, enemigos...)

# Dimensiones de ventana
ANCHO = 600
ALTO = 800

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)

# Fuentes
p.font.init()
FUENTE_TITULO = p.font.Font(None, 72)
FUENTE_MENU = p.font.Font(None, 48)
FUENTE_TEXTO = p.font.Font(None, 36)

# Configuración de naves
NAVES = {
    1: {"sprite": "recursos/ship5.png", "nombre": "Básica", "velocidad": 5},
    2: {"sprite": "recursos/ship5.png", "nombre": "Rápida", "velocidad": 7},
    3: {"sprite": "recursos/ship5.png", "nombre": "Resistente", "velocidad": 4}
}

# Configuración de balas
BALAS = {
    1: {"sprite": "recursos/bala.png", "nombre": "Normal", "daño": 1, "velocidadB": 8},
    2: {"sprite": "recursos/bala.png", "nombre": "Potente", "daño": 2, "velocidadB": 6},
    3: {"sprite": "recursos/bala.png", "nombre": "Explosiva", "daño": 3, "velocidadB": 4}
}

# Niveles (5 niveles)
NIVELES = {
    1: {"nombre": "Muy Fácil", "enemigos": 2, "vida_enemigo": 2},
    2: {"nombre": "Fácil", "enemigos": 3, "vida_enemigo": 3},
    3: {"nombre": "Normal", "enemigos": 5, "vida_enemigo": 5},
    4: {"nombre": "Difícil", "enemigos": 8, "vida_enemigo": 7},
    5: {"nombre": "Muy Difícil", "enemigos": 10, "vida_enemigo": 10}
}