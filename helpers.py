# Contendrá funciones generales comunes
import re
import os
import platform

def limpiar_pantalla():
    os.system("cls") if platform.system() == "Windows" else os.system("clear") # para limpiar la terminal CLS para windows y CLEAR en Mac y Linux

def leer_texto(min=0, max=100, mensaje=None):
    # Esta forma es una condicion formateada donde primero va lo que queremos hacer luego la condicion y ultimo lo contrario a lo que queremos
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) >= min and len(texto) <= max:
            return texto
        else:
            print("Ingrese los datos correctamente!\n")

def validar_dni(dni, lista):
    if not re.match("[0-9]{2}[A-Z]$", dni):
        print("DNI incorrecto. Debe cumplir el formato!")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("El DNI ya existe registrado. Intenta ingresar otro DNI")
            return False
    return True