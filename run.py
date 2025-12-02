#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecutor del juego Space Shooter
Ejecuta: python run.py
"""
import sys
import os

# Añadir la carpeta juego al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'juego'))

from main import main

if __name__ == "__main__":
    main()
