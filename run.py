#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecutor del juego Space Shooter
Ejecuta: python run.py
"""
import sys
import os

# Ejecutar como paquete para que los imports relativos (".config") funcionen
# Importa juego.main dentro del paquete "juego"
from juego.main import main

if __name__ == "__main__":
    main()
