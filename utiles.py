from datetime import datetime
import json
import os


# Cargar o inicializar datos de un archivo JSON
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# Funciones para pedir entradas al usuario con validación
def pedir_string(mensaje):
        while True:
            valor = input(mensaje)
            if valor != "" and not valor.isdigit():
                return valor
            else:
                print( " Ingresá un texto válido (no vacío ni solo números).")

def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)
        try:
            return int(valor)
        except ValueError:
           print(" Ingresá un número entero válido.")

def pedir_fecha(mensaje):
    while True:
        valor = input(mensaje)
        try:
        # Intenta convertir el string en una fecha con formato exacto DD/MM/AAAA
            fecha = datetime.strptime(valor, "%d/%m/%Y")
            return valor
        except ValueError:
            print(" Ingresá una fecha válida en formato DD/MM/AAAA.")

def valida_tipo_usuario(mensaje):
        while True:
            valor = input(mensaje)
            if valor.lower() in ["alumno", "docente"]:
                return valor.lower()
            else:
                print(" Ingresá un tipo válido (alumno o docente).")