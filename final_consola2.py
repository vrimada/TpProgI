import json
import os

# Archivos
ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PRESTAMOS = "prestamos.json"

# Cargar o inicializar datos
def cargar_datos(archivo):
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_datos(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Altas de libro en diccionario
def agregar_libro(libros):
    libro = {
        "id": input("ID del libro: "),
        "titulo": input("Título: "),
        "autor": input("Autor: "),
        "editorial": input("Editorial: "),
        "anio": input("Año: "),
        "genero": input("Género: "),
        "disponible": True
    }
    libros.append(libro)
    print("✅ Libro agregado con éxito.")
#alta de usuario en diccionario
def agregar_usuario(usuarios):
    usuario = {
        "id": input("ID de usuario: "),
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "tipo": input("Tipo (alumno/docente): ").lower()
    }
    usuarios.append(usuario)
    print("✅ Usuario agregado con éxito.")

#Revisar
def registrar_prestamo(prestamos, libros, usuarios):

    #agregar una funcion que poniendo el nombre del libro busque el ID y usarla ara la variable id_libro
    id_libro = input("ID del libro a prestar: ")
    id_usuario = input("ID del usuario: ")
    #id_usuario esta en el carnet

    libro = next((l for l in libros if l["id"] == id_libro and l["disponible"]), None)
    if not libro:
        print(" Libro no disponible o no existe.")
        return

    if not any(u for u in usuarios if u["id"] == id_usuario):
        print(" Usuario no encontrado.")
        return

    prestamo = {
        "id_libro": id_libro,
        "id_usuario": id_usuario,
        "fecha_prestamo": input("Fecha de préstamo (DD/MM/AAAA): "),
        "fecha_devolucion": ""
    }
    prestamos.append(prestamo)
    libro["disponible"] = False
    print(" Préstamo registrado con éxito.")

# Devolución
def devolver_libro(prestamos, libros):
    id_libro = input("ID del libro a devolver: ")
    prestamo = next((p for p in prestamos if p["id_libro"] == id_libro and not p["fecha_devolucion"]), None)

    if not prestamo:
        print(" No se encontró préstamo activo para ese libro.")
        return

    prestamo["fecha_devolucion"] = input("Fecha de devolución (DD/MM/AAAA): ")
    for libro in libros:
        if libro["id"] == id_libro:
            libro["disponible"] = True
            break
    print(" Libro devuelto con éxito.")

# Listados
def mostrar_libros(libros):
    print(" Lista de libros:")
    for libro in libros:
        estado = "Disponible" if libro["disponible"] else "Prestado"
        print(f"{libro['id']} - {libro['titulo']} ({estado})")

def mostrar_usuarios(usuarios):
    print("👤 Lista de usuarios:")
    for u in usuarios:
        print(f"{u['id']} - {u['nombre']} {u['apellido']} ({u['tipo']})")





#REVISARREVISARREVISAR

#agregar una funcion que imprima todos los libros restados y a quien

#def cargar_datos(nombre_archivo):
   # with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
    #    return json.load(archivo)

def mostrar_prestamos_activos():
    # Cargar datos desde los archivos JSON
    libros = cargar_datos("libros.json")
    usuarios = cargar_datos("usuarios.json")
    prestamos = cargar_datos("prestamos.json")

    # Convertimos libros y usuarios en diccionarios para acceso rápido 
    libros_dict = {libro['id']: libro for libro in libros}
    usuarios_dict = {usuario['id']: usuario for usuario in usuarios}

    print(" Listado de libros actualmente prestados:\n")

    prestamos_activos = [p for p in prestamos if p['fecha_devolucion'] is None]

    if not prestamos_activos:
        print("No hay libros prestados actualmente.")
        return

    for prestamo in prestamos_activos:
        libro = libros_dict.get(prestamo['id_libro'])
        usuario = usuarios_dict.get(prestamo['id_usuario'])

        if libro and usuario:
            print(f"📖 {libro['titulo']} - Prestado a: {usuario['nombre']} {usuario['apellido']}")


def menu():
    libros = cargar_datos(ARCHIVO_LIBROS)
    usuarios = cargar_datos(ARCHIVO_USUARIOS)
    prestamos = cargar_datos(ARCHIVO_PRESTAMOS)

    while True:
        print("\n📘 MENÚ BIBLIOTECA ESCOLAR")
        print("1. Agregar libro")
        print("2. Agregar usuario")
        print("3. Registrar préstamo")
        print("4. Devolver libro")
        print("5. Mostrar libros")
        print("6. Mostrar usuarios")
        print("7.Imprimir listado de prestamos")
        print("8. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            agregar_libro(libros)
        elif opcion == "2":
            agregar_usuario(usuarios)
        elif opcion == "3":
            registrar_prestamo(prestamos, libros, usuarios)
        elif opcion == "4":
            devolver_libro(prestamos, libros)
        elif opcion == "5":
            mostrar_libros(libros)
        elif opcion == "6":
            mostrar_usuarios(usuarios)
        elif opcion == "7":
            mostrar_prestamos_activos()
        elif opcion == "8":    
            guardar_datos(ARCHIVO_LIBROS, libros)
            guardar_datos(ARCHIVO_USUARIOS, usuarios)
            guardar_datos(ARCHIVO_PRESTAMOS, prestamos)
            print("💾 Datos guardados. ¡Hasta luego!")
            break
        else:
            print(" Opción no válida. Intentá de nuevo.")

# Ejecutar menú
if __name__ == "__main__":
    menu()
