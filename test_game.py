#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba rapida para verificar que el juego inicia correctamente
Ejecuta: python test_game.py
"""

import sys
import os

# Diagnostico
print("=" * 60)
print("DIAGNOSTICO DEL JUEGO - Space Shooter")
print("=" * 60)

# 1. Verificar Python
print(f"\n[1] Version de Python: {sys.version.split()[0]}")
if sys.version_info < (3, 10):
    print("    [WARNING] Se recomienda Python 3.10 o superior")
else:
    print("    [OK] Versión compatible")

# 2. Verificar Pygame
try:
    import pygame
    print(f"\n[2] Pygame: {pygame.__version__}")
    print("    [OK] Pygame instalado correctamente")
except ImportError:
    print("\n[2] Pygame: NO INSTALADO")
    print("    [ERROR] Ejecuta: pip install pygame==2.6.1")
    sys.exit(1)

# 3. Verificar estructura de archivos
print("\n[3] Estructura de archivos:")
required_files = {
    "run.py": "Punto de entrada principal",
    "README.md": "Documentacion",
    "juego/__init__.py": "Paquete Python",
    "juego/main.py": "Logica principal",
    "juego/config.py": "Configuracion",
    "juego/menu.py": "Menus",
    "juego/juego.py": "Clase del juego",
}

all_files_exist = True
for file_path, description in required_files.items():
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"    [OK] {file_path} ({size} bytes) - {description}")
    else:
        print(f"    [ERROR] FALTA {file_path}")
        all_files_exist = False

# 4. Verificar imports
print("\n[4] Verificando imports:")
try:
    sys.path.insert(0, 'juego')
    from config import *
    print("    [OK] config.py importado")
    from menu import MenuInicio, MenuNiveles, MenuVestuario
    print("    [OK] menu.py importado")
    from juego import Juego
    print("    [OK] juego.py importado")
    from main import main
    print("    [OK] main.py importado")
except ImportError as e:
    print(f"    [ERROR] Fallo en import: {e}")
    sys.exit(1)

# 5. Verificar recursos
print("\n[5] Verificando recursos graficos:")
resources_to_check = [
    "recursos/explosion/exp2_01.png",
    "recursos/enemigos/",
    "recursos/fondos/",
]

for resource in resources_to_check:
    if os.path.exists(resource):
        print(f"    [OK] {resource}")
    else:
        print(f"    [WARNING] No encontrado: {resource}")

# Resumen
print("\n" + "=" * 60)
if all_files_exist:
    print("ESTADO: [OK] TODO LISTO PARA JUGAR")
    print("\nEjecuta: python run.py")
else:
    print("ESTADO: [ERROR] Faltan archivos")
    sys.exit(1)

print("=" * 60)
