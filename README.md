# Space Shooter - Guia de Ejecucion

## Como Ejecutar el Juego

### Opcion 1: Usando run.py (Recomendado)
```bash
python run.py
```

### Opcion 2: Ejecutar main.py directamente desde juego/
```bash
cd juego
python main.py
```

## Requisitos
- Python 3.10+
- Pygame 2.6.1

## Instalacion de Dependencias
```bash
pip install pygame==2.6.1
```

## Controles del Juego

### En Menus
- **ARRIBA/ABAJO**: Navegar opciones
- **ESPACIO**: Seleccionar
- **ESC**: Volver

### En el Juego
- **FLECHAS**: Mover nave
- **ESPACIO**: Disparar
- **ESC**: Volver a menu

### En Pantallas de Victoria/Derrota
- **CUALQUIER TECLA**: Volver al menu de niveles
- **CLIC DE RATON**: Tambien funciona para volver

## Caracteristicas

### 5 Niveles
- Nivel 1: Tutorial facil
- Nivel 2: Dificultad normal
- Nivel 3: Desafio moderado
- Nivel 4: Dificultad alta
- Nivel 5: Dificultad extrema

### 3 Tipos de Naves
- Nave Verde: Velocidad normal
- Nave Azul: Velocidad rapida
- Nave Roja: Velocidad lenta (mas vida)

### 3 Tipos de Balas
- Balas Verdes: Velocidad normal
- Balas Rapidas: Mayor velocidad
- Balas Potentes: Mayor danio

### Sistema de Vestuario
- Selecciona tu nave y tipo de balas
- La configuracion se guarda entre niveles
- Cambia tu setup en cualquier momento desde el menu

## Resolucion
- Ventana: 1200x800 px
- Pantalla completa: No (ventana flotante)

## Sistema de Puntuacion
- Cada enemigo derrotado: 10 puntos
- Objetivo de puntos varia por nivel
- Debes derrotar todos los enemigos para ganar

## Errores Comunes

### "ModuleNotFoundError: No module named 'pygame'"
Instala pygame: `pip install pygame==2.6.1`

### "No se pudo cargar la imagen"
Asegurate de que el archivo existe en la carpeta `recursos/`

### "ENTER no funciona en pantalla de derrota"
Presiona CUALQUIER TECLA (no solo ENTER) para volver

## Estructura del Proyecto

```
proyecto.prog1/
|- run.py                 # Punto de entrada principal
|- juego/
|  - __init__.py
|  - main.py              # Logica principal del juego
|  - config.py            # Configuracion y constantes
|  - menu.py              # Clases de menus
|  - juego.py             # Clase principal del juego
|  - juegazo              # Alias del juego (compatible)
|- recursos/              # Imagenes y assets
|  - enemigos/
|  - explosion/
|  - fondos/
│   └── ...
└── README.md            # Este archivo
```

## Notas Importantes

- El juego usa imports relativos dentro del paquete `juego/`
- `run.py` es el punto de entrada que resuelve los imports correctamente
- Todos los archivos deben estar codificados en UTF-8
- No se pueden usar caracteres Unicode especiales en print() (solo ASCII)

## Git y Colaboracion

El repositorio esta en: https://github.com/ArtSyntaxX/proyecto.prog1

Para actualizar:
```bash
git pull origin main
python run.py
```

Para contribuir:
```bash
git checkout -b feature/mi-rama
# Hacer cambios...
git commit -m "Descripcion de cambios"
git push origin feature/mi-rama
```

---
Juego desarrollado con Pygame | Python 3.13.7
