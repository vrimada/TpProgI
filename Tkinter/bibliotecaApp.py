import tkinter as tk
from tkinter import messagebox, simpledialog
import Tkinter.funciones as funciones

# Archivos JSON para almacenar los datos
ARCHIVO_LIBROS = "libros.json"
ARCHIVO_USUARIOS = "usuarios.json"
ARCHIVO_PRESTAMOS = "prestamos.json"


class BibliotecaApp(tk.Tk):
    # Biblioteca con INTERFAz GRAFICA TKINTER 
    def __init__(self):
        super().__init__()
        self.title("Gestión de Biblioteca Escolar") #Titulo
        self.geometry("700x500")  #Tamaño de la ventana
        self.configure(bg="#f4f4f4")  #Color de fondo

        #Cargamos en variables los datos de los archivos JSON
        self.libros = funciones.cargar_datos(ARCHIVO_LIBROS)
        self.usuarios = funciones.cargar_datos(ARCHIVO_USUARIOS)
        self.prestamos = funciones.cargar_datos(ARCHIVO_PRESTAMOS)
        
        #Creamos los widgets de la interfaz
        self.crear_widgets()

    def crear_widgets(self):
        # Coleccion de botones para las diferentes acciones
        botones = [
            ("Agregar libro", self.agregar_libro),
            ("Agregar usuario", self.agregar_usuario),
            ("Registrar préstamo", self.registrar_prestamo),
            ("Devolver libro", self.devolver_libro),
            ("Mostrar libros", self.mostrar_libros),
            ("Mostrar usuarios", self.mostrar_usuarios),
            ("Libros actualmente prestados", self.mostrar_prestamos_activos),
            ("Salir y guardar", self.guardar_y_salir),
        ]
        # Primero esta el titulo y luego el comando en el arreglo de Botones
        for texto, comando in botones:
            btn = tk.Button(self, text=texto, command=comando, width=30, height=2, bg="#e0e0e0") #Creo un boton con el texto y el comando
            btn.pack(pady=5) # Agrego el boton a la ventana 

        # Area de texto para mostrar la lista de libros, usuarios o prestamos
        self.lista = tk.Text(self, height=20, wrap="word", bg="#ffffff")
        self.lista.pack(padx=10, pady=10, fill="both", expand=True)

    def agregar_libro(self):
        # Pedimos los datos del libro al usuario mediante cuadros de dialogo (simpledialog)
        libro = {
            "id": simpledialog.askstring("ID", "ID del libro:"),
            "titulo": simpledialog.askstring("Título", "Título del libro:"),
            "autor": simpledialog.askstring("Autor", "Autor del libro:"),
            "editorial": simpledialog.askstring("Editorial", "Editorial del libro:"),
            "anio": simpledialog.askstring("Año", "Año de publicación:"),
            "genero": simpledialog.askstring("Género", "Género del libro:"),
            "disponible": True
        }
        self.libros.append(libro)
        messagebox.showinfo("Exito", "Libro agregado con éxito.")

    def agregar_usuario(self):
        usuario = {
            "id": simpledialog.askstring("ID", "ID del usuario:"),
            "nombre": simpledialog.askstring("Nombre", "Nombre del usuario:"),
            "apellido": simpledialog.askstring("Apellido", "Apellido del usuario:"),
            "tipo": simpledialog.askstring("Tipo", "Tipo (alumno/docente):").lower()
        }
        self.usuarios.append(usuario)
        messagebox.showinfo("Exito", "Usuario agregado con éxito.")

    def registrar_prestamo(self):
        id_libro = simpledialog.askstring("ID Libro", "ID del libro a prestar:")
        id_usuario = simpledialog.askstring("ID Usuario", "ID del usuario:")
        libro = next((l for l in self.libros if l["id"] == id_libro and l["disponible"]), None)
        if not libro:
            messagebox.showerror("Error", "Libro no disponible o no existe.")
            return
        if not any(u for u in self.usuarios if u["id"] == id_usuario):
            messagebox.showerror("Error", "Usuario no encontrado.")
            return
        prestamo = {
            "id_libro": id_libro,
            "id_usuario": id_usuario,
            "fecha_prestamo": simpledialog.askstring("Fecha", "Fecha de préstamo (DD/MM/AAAA):"),
            "fecha_devolucion": ""
        }
        self.prestamos.append(prestamo)
        libro["disponible"] = False
        messagebox.showinfo("Éxito", "Préstamo registrado con éxito.")

    def devolver_libro(self):
        id_libro = simpledialog.askstring("ID Libro", "ID del libro a devolver:")
        prestamo = next((p for p in self.prestamos if p["id_libro"] == id_libro and not p["fecha_devolucion"]), None)
        if not prestamo:
            messagebox.showerror("Error", "No se encontró préstamo activo para ese libro.")
            return
        prestamo["fecha_devolucion"] = simpledialog.askstring("Fecha", "Fecha de devolución (DD/MM/AAAA):")
        for libro in self.libros:
            if libro["id"] == id_libro:
                libro["disponible"] = True
                break
        messagebox.showinfo("Éxito", "Libro devuelto con éxito.")

    def mostrar_libros(self):
        self.lista.delete("1.0", tk.END)
        self.lista.insert(tk.END, "Lista de libros:\n\n")
        for libro in self.libros:
            estado = "Disponible" if libro["disponible"] else "Prestado"
            self.lista.insert(tk.END, f"{libro['id']} - {libro['titulo']} ({estado})\n")

    def mostrar_usuarios(self):
        self.lista.delete("1.0", tk.END)
        self.lista.insert(tk.END, "Lista de usuarios:\n\n")
        for u in self.usuarios:
            self.lista.insert(tk.END, f"{u['id']} - {u['nombre']} {u['apellido']} ({u['tipo']})\n")

    def mostrar_prestamos_activos(self):
        # Convertimos libros y usuarios en diccionarios para acceso rápido 
        libros_dict = {libro['id']: libro for libro in self.libros}
        usuarios_dict = {usuario['id']: usuario for usuario in self.usuarios}

        self.lista.delete("1.0", tk.END)
        self.lista.insert(tk.END, "Listado de libros prestados:\n\n")
        for prestamo in self.prestamos:
            if prestamo["fecha_devolucion"] == "" or prestamo["fecha_devolucion"] is None: # Verifica si el libro está prestado
                titulo = libros_dict.get(prestamo['id_libro'], {}).get('titulo', 'Título no encontrado')
                usuarioNom = usuarios_dict.get(prestamo['id_usuario'], {}).get('nombre', 'Usuario no encontrado')
                usuarioApe = usuarios_dict.get(prestamo['id_usuario'], {}).get('apellido', 'Usuario no encontrado')
                self.lista.insert(tk.END, f"({ prestamo['id_libro'] }) {titulo} - Prestado a: {usuarioNom } {usuarioApe}\n")
       

    def guardar_y_salir(self):
        # Guardamos los datos en los archivos JSON
        funciones.guardar_datos(ARCHIVO_LIBROS, self.libros)
        funciones.guardar_datos(ARCHIVO_USUARIOS, self.usuarios)
        funciones.guardar_datos(ARCHIVO_PRESTAMOS, self.prestamos)
        messagebox.showinfo("Guardado", "Datos guardados. Cerrando aplicación.")
        self.destroy()
