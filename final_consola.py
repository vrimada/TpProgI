import utiles as u
from colorama import Fore, Style, init
init()

# Archivos
ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PRESTAMOS = "prestamos.json"


# Altas de libro en diccionario
def agregar_libro(libros):
    nuevo_id = str(len(libros) + 1) # Asignar ID automáticamente como número secuencial
    libro = {
        "id": "L"+ nuevo_id,
        "titulo": u.pedir_string("Título: "),
        "autor": u.pedir_string("Autor: "),
        "editorial": u.pedir_string("Editorial: "),
        "anio": u.pedir_entero("Año: "),
        "genero": u.pedir_string("Género: "),
        "disponible": True
    }
    libros.append(libro)
    print(" Libro agregado con éxito. ID asignado: " f"{libro['id']}")

#alta de usuario en diccionario
def agregar_usuario(usuarios):
     
    nuevo_id = str(len(usuarios) + 1) # Asignar ID automáticamente como número secuencial

    usuario = {
        "id": "U" + nuevo_id,
        "nombre": u.pedir_string("Nombre: "),
        "apellido": u.pedir_string("Apellido: "),
        "tipo": u.valida_tipo_usuario("Tipo (alumno/docente): ")
    }
    usuarios.append(usuario)
    print(" Usuario agregado con éxito. ID asignado: " f"{usuario['id']}")


def registrar_prestamo(prestamos, libros, usuarios):

    #agregar una funcion que poniendo el nombre del libro busque el ID y usarla ara la variable id_libro
    id_libro = u.pedir_string("ID del libro a prestar: ")
    id_usuario = u.pedir_string("ID del usuario: ") #id_usuario esta en el carnet
   
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
        "fecha_prestamo": u.pedir_fecha("Fecha de préstamo (DD/MM/AAAA): "),
        "fecha_devolucion": ""
    }
    prestamos.append(prestamo)
    libro["disponible"] = False
    print(" Préstamo registrado con éxito.")

# Devolución
def devolver_libro(prestamos, libros):
    id_libro = u.pedir_string("ID del libro a devolver: ")
    prestamo = next((p for p in prestamos if p["id_libro"] == id_libro and not p["fecha_devolucion"]), None)

    if not prestamo:
        print(" No se encontró préstamo activo para ese libro.")
        return

    prestamo["fecha_devolucion"] = input("Fecha de devolución (DD/MM/AAAA): ")
    for libro in libros:
        if libro["id"] == id_libro:
            libro["disponible"] = True
            break
    print("verde"," Libro devuelto con éxito.")

# Listados
def mostrar_libros(libros):
    print(" Lista de libros:")
    for libro in libros:
        estado = "Disponible" if libro["disponible"] else "Prestado"
        print(f"{libro['id']} - {libro['titulo']} ({estado})")

def mostrar_usuarios(usuarios):
    print(" Lista de usuarios:")
    for u in usuarios:
        print(f"{u['id']} - {u['nombre']} {u['apellido']} ({u['tipo']})")



def mostrar_prestamos_activos():
    # Cargar datos desde los archivos JSON
    libros = u.cargar_datos(ARCHIVO_LIBROS)
    usuarios = u.cargar_datos(ARCHIVO_USUARIOS)
    prestamos = u.cargar_datos(ARCHIVO_PRESTAMOS)

    # Convertimos libros y usuarios en diccionarios para acceso rápido 
    libros_dict = {libro['id']: libro for libro in libros}
    usuarios_dict = {usuario['id']: usuario for usuario in usuarios}

    print(" Listado de libros actualmente prestados:\n")

    prestamos_activos = [p for p in prestamos if p['fecha_devolucion'] is None or p['fecha_devolucion'] == ""]

    if not prestamos_activos:
        print("No hay libros prestados actualmente.")
        return

    for prestamo in prestamos_activos:
        libro = libros_dict.get(prestamo['id_libro'])
        usuario = usuarios_dict.get(prestamo['id_usuario'])

        if libro and usuario:
            print(f"📖 {libro['titulo']} - Prestado a: {usuario['nombre']} {usuario['apellido']}")


def menu():
    libros = u.cargar_datos(ARCHIVO_LIBROS)
    usuarios = u.cargar_datos(ARCHIVO_USUARIOS)
    prestamos = u.cargar_datos(ARCHIVO_PRESTAMOS)

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
            u.guardar_datos(ARCHIVO_LIBROS, libros)
            u.guardar_datos(ARCHIVO_USUARIOS, usuarios)
            u.guardar_datos(ARCHIVO_PRESTAMOS, prestamos)
            print("💾 Datos guardados. ¡Hasta luego!")
            break
        else:
            print(" Opción no válida. Intentá de nuevo.")

# Ejecutar menú
if __name__ == "__main__":
    menu()
