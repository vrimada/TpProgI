import utiles as u
# Biblioteca Escolar - Gestión de Préstamos

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

def eliminar_libro(libros, id_libro):
    # Eliminar un libro por ID
    if(id_libro not in [libro["id"] for libro in libros]):
        print(u.error(" El libro no existe."))
        return
    else:
        libros = [libro for libro in libros if libro["id"] != id_libro]
        u.guardar_datos(ARCHIVO_LIBROS, libros)
        print(" Libro eliminado con éxito.")

def eliminar_usuario(usuarios):
    # Eliminar un usuario por ID
    id_usuario = u.pedir_string("ID del usuario a eliminar: ")
    if(id_usuario not in [usuario["id"] for usuario in usuarios]):
        print(u.error(" El usuario no existe."))
        return
    else:
        usuarios = [usuario for usuario in usuarios if usuario["id"] != id_usuario]
        u.guardar_datos(ARCHIVO_USUARIOS, usuarios)
        print(" Usuario eliminado con éxito.")

def menu():
    libros = u.cargar_datos(ARCHIVO_LIBROS)
    usuarios = u.cargar_datos(ARCHIVO_USUARIOS)
    prestamos = u.cargar_datos(ARCHIVO_PRESTAMOS)

    while True:
        print( u.info("\n📘 MENÚ BIBLIOTECA ESCOLAR\n"))
        print("1. Agregar libro")
        print("2. Agregar usuario")
        print("3. Registrar préstamo")
        print("4. Devolver libro")
        print("5. Mostrar libros")
        print("6. Mostrar usuarios")
        print("7. Imprimir listado de prestamos")
        print("8. Eliminar libro")
        print("9. Eliminar usuario")
        print("10. Salir\n")
        opcion = input("Elegí una opción: ")

      
        # Usar match-case para manejar las opciones
        match opcion:
                case "1":
                    agregar_libro(libros)
                case "2":
                    agregar_usuario(usuarios)
                case "3":
                    registrar_prestamo(prestamos, libros, usuarios)
                case "4":
                    devolver_libro(prestamos, libros)
                case "5":
                    mostrar_libros(libros)
                case "6":
                    mostrar_usuarios(usuarios)
                case "7":
                    mostrar_prestamos_activos()
                case "8":
                    eliminar_libro(libros, u.pedir_string("ID del libro a eliminar: "))
                case "9":
                    eliminar_usuario(usuarios)    
                case "10":
                    u.guardar_datos(ARCHIVO_LIBROS, libros)
                    u.guardar_datos(ARCHIVO_USUARIOS, usuarios)
                    u.guardar_datos(ARCHIVO_PRESTAMOS, prestamos)
                    print("💾 Datos guardados. ¡Hasta luego!")
                    break
                case _:
                    print("Opción no válida. Ingrese un numero del 1 al 10.")

# Ejecutar menú
if __name__ == "__main__":
    menu()
