import pygame as p



# todas las variables globales 

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
CIAN = (0, 255, 255)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)
GRIS_OSCURO = (30, 30, 30)
GRIS_CLARO = (100, 100, 100)
FONDO_OSCURO = (15, 15, 35)

# Fuentes
p.font.init()
FUENTE_TITULO = p.font.Font(None, 72)
FUENTE_MENU = p.font.Font(None, 48)
FUENTE_TEXTO = p.font.Font(None, 36)
FUENTE_PEQUENA = p.font.Font(None, 24)
FUENTE_HUD = p.font.Font(None, 28)

# Configuración de naves (3 naves diferentes)
NAVES = {
    1: {
        "sprite": "recursos/ship5.png",
        "nombre": "Halcon",
        "velocidad": 5,
        "color": AZUL,
        "descripcion": "Equilibrada"
    },
    2: {
        "sprite": "recursos/ship6.png",
        "nombre": "Rayo",
        "velocidad": 8,
        "color": AMARILLO,
        "descripcion": "Rapida"
    },
    3: {
        "sprite": "recursos/nave.png",
        "nombre": "Titan",
        "velocidad": 3,
        "color": VERDE,
        "descripcion": "Resistente"
    }
}

# Configuración de balas (3 tipos diferentes)
BALAS = {
    1: {
        "sprite": "recursos/bala.png",
        "nombre": "Normal",
        "daño": 1,
        "velocidadB": 8,
        "color": VERDE,
        "tamaño": (10, 25)
    },
    2: {
        "sprite": "recursos/bala2.png",
        "nombre": "Potente",
        "daño": 2,
        "velocidadB": 6,
        "color": NARANJA,
        "tamaño": (15, 35)
    },
    3: {
        "sprite": "recursos/bala2.png",
        "nombre": "Explosiva",
        "daño": 3,
        "velocidadB": 5,
        "color": ROJO,
        "tamaño": (20, 40)
    }
}

# Niveles (5 niveles con objetivos claros)
NIVELES = {
    1: {
        "nombre": "Muy Facil",
        "enemigos": 3,
        "vida_enemigo": 2,
        "objetivo_puntos": 30,
        "velocidad_enemigo": 1,
        "pueden_disparar": False,
        "descripcion": "Aprende los controles"
    },
    2: {
        "nombre": "Facil",
        "enemigos": 5,
        "vida_enemigo": 3,
        "objetivo_puntos": 50,
        "velocidad_enemigo": 1,
        "pueden_disparar": False,
        "descripcion": "Primeros disparos enemigos"
    },
    3: {
        "nombre": "Normal",
        "enemigos": 7,
        "vida_enemigo": 4,
        "objetivo_puntos": 70,
        "velocidad_enemigo": 2,
        "pueden_disparar": True,
        "descripcion": "Enemigos se mueven"
    },
    4: {
        "nombre": "Dificil",
        "enemigos": 10,
        "vida_enemigo": 5,
        "objetivo_puntos": 100,
        "velocidad_enemigo": 3,
        "pueden_disparar": True,
        "descripcion": "Desafío extremo"
    },
    5: {
        "nombre": "Muy Dificil",
        "enemigos": 15,
        "vida_enemigo": 6,
        "objetivo_puntos": 150,
        "velocidad_enemigo": 4,
        "pueden_disparar": True,
        "descripcion": "Modo leyenda"
    }
}

# Configuración de enemigos (5 tipos disponibles en recursos/enemigos)
ENEMIGOS = {
    1: "recursos/enemigos/enemigo1.png",
    2: "recursos/enemigos/enemigo2.png",
    3: "recursos/enemigos/enemigo3.png",
    4: "recursos/enemigos/enemigo4.png",
    5: "recursos/enemigos/enemigo5.png",
}

# Fondos por pantalla (en recursos/fondos)
FONDOS = {
    "inicio": "recursos/fondos/fondostart.png",
    "niveles": "recursos/fondos/fondoniveles.png",
    # Por nivel (fondo1..fondo5)
    1: "recursos/fondos/fondo1.png",
    2: "recursos/fondos/fondo2.png",
    3: "recursos/fondos/fondo3.png",
    4: "recursos/fondos/fondo4.png",
    5: "recursos/fondos/fondo5.png",
}