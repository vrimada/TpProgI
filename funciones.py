import json
import os
from tkinter import messagebox

# Inicializar de los datos
def cargar_datos(archivo):
    try:
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo: {archivo}")
        return []
        
 

# Guardar datos en el archivo JSON
def guardar_datos(archivo, datos):
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except (FileNotFoundError, PermissionError, OSError) as e:
        messagebox.showerror("Error de archivo", f"No se pudo abrir el archivo: {archivo} \n{e}")
    except TypeError as e:
        messagebox.showerror("Error de formato", f"Datos no serializables a JSON:\n{e}")
