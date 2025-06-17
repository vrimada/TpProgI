from datetime import datetime
import json
import os
from colorama import Fore, Style, init
init()

# Cargar o inicializar datos de un archivo JSON
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
# Colores
colores = {
        "verde": Fore.GREEN,
        "rojo": Fore.RED,
        "azul": Fore.BLUE,
        "amarillo": Fore.YELLOW,
        "cian": Fore.CYAN,
        "magenta": Fore.MAGENTA,
        "blanco": Fore.WHITE
    }
def error(texto):
    
    return f"{Fore.RED}{texto}{ Style.RESET_ALL}"
def exito(texto):
    return f"{Fore.GREEN}{texto}{ Style.RESET_ALL}"
def info(texto):
    return f"{Fore.CYAN}{texto}{ Style.RESET_ALL}"

# Funciones para pedir entradas al usuario con validación   
def pedir_string(mensaje):
        while True:
            valor = input(mensaje)
            if  (valor != "" and not valor.isdigit()):
                return valor
            else:
                print( error(" Ingresá un texto válido (no vacío ni solo números)."))

def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)
        try:
            return int(valor)
        except ValueError:
           print( error(" Ingresá un número entero válido."))

def pedir_fecha(mensaje):
    while True:
        valor = input(mensaje)
        try:
        # Intenta convertir el string en una fecha con formato exacto DD/MM/AAAA
            fecha = datetime.strptime(valor, "%d/%m/%Y")
            return valor
        except ValueError:
            print( error(" Ingresá una fecha válida en formato DD/MM/AAAA."))

def valida_tipo_usuario(mensaje):
        while True:
            valor = input(mensaje)
            if valor.lower() in ["alumno", "docente"]:
                return valor.lower()
            else:
                print( error(" Ingresá un tipo válido (alumno o docente)."))
