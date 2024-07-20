import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear la ventana principal antes de cargar las imágenes
ventana = ctk.CTk()
ventana.title("Sistema de Reservas de Cine")
ventana.geometry("500x600")

# Variables globales
usuario_actual = None

# Función para mostrar la pantalla de login
def mostrar_login():
    def verificar_credenciales():
        global usuario_actual
        usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()
        
        if contrasena == "limonada":
            usuario_actual = usuario
            if usuario == "Admin":
                messagebox.showinfo("Bienvenido", "Bienvenido Administrador")
                frame_login.pack_forget()
                mostrar_frame_admin_peliculas()
            else:
                messagebox.showinfo("Bienvenido", f"Bienvenido {usuario}")
                frame_login.pack_forget()
                mostrar_pelicula_frame()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
    
    frame_login = ctk.CTkFrame(ventana)
    frame_login.pack(expand=True, fill='both')
    
    etiqueta_usuario = ctk.CTkLabel(frame_login, text="Usuario:")
    etiqueta_usuario.pack(pady=10)
    
    entrada_usuario = ctk.CTkEntry(frame_login)
    entrada_usuario.pack(pady=10)
    
    etiqueta_contrasena = ctk.CTkLabel(frame_login, text="Contraseña:")
    etiqueta_contrasena.pack(pady=10)
    
    entrada_contrasena = ctk.CTkEntry(frame_login, show='*')
    entrada_contrasena.pack(pady=10)
    
    boton_login = ctk.CTkButton(frame_login, text="Iniciar Sesión", command=verificar_credenciales)
    boton_login.pack(pady=20)

# Función para redimensionar imágenes
def cargar_imagen(ruta, tamaño=(75, 75)):
    pil_image = Image.open(ruta)
    pil_image_resized = pil_image.resize(tamaño)
    return ImageTk.PhotoImage(pil_image_resized)

# Cargar imágenes de cada película
image_haikyuu_path = "C:\\Users\\LENOVO\\Downloads\\haikyuu.jpg"
image_batman_path = "C:\\Users\\LENOVO\\Downloads\\batman.jpg"
image_superman_path = "C:\\Users\\LENOVO\\Downloads\\superman.jfif"
image_it_path = "C:\\Users\\LENOVO\\Downloads\\it.jpg"
image_starwars_path = "C:\\Users\\LENOVO\\Downloads\\starwars.jpeg"
# Cargar y redimensionar las imágenes
tkimage_haikyuu = cargar_imagen(image_haikyuu_path)
tkimage_batman = cargar_imagen(image_batman_path)
tkimage_superman = cargar_imagen(image_superman_path)
tkimage_it = cargar_imagen(image_it_path)
tkimage_starwars = cargar_imagen(image_starwars_path)

# Matriz para almacenar el estado de los asientos (Libre: 'L', Ocupado: 'O')
estado_asientos = [['L' for _ in range(5)] for _ in range(5)]
# Matriz para almacenar referencias a los botones de los asientos
botones_asientos = [[None for _ in range(5)] for _ in range(5)]

# Función para buscar el mejor asiento disponible
def buscar_mejor_asiento():
    for fila in range(5):
        if 'L' in estado_asientos[fila]:
            mejores_asientos = [3, 2, 4, 1, 5]
            for asiento in mejores_asientos:
                if estado_asientos[fila][asiento - 1] == 'L':
                    return fila, asiento
    return None, None

# Función para cambiar el color y texto del botón seleccionado
def cambiar_color_y_texto(boton, fila, columna):
    boton.configure(fg_color="green", text="O")
    estado_asientos[fila][columna] = 'O'

def mostrar_sala():
    sala_frame.pack_forget()
    frame_asientos = ctk.CTkFrame(ventana)
    frame_asientos.pack(expand=True, fill='both')
    frame_asientos.pack_propagate(False)

    # Crear y posicionar los botones
    for fila in range(5):
        for columna in range(5):
            boton = ctk.CTkButton(frame_asientos, text="L", width=80, height=50, 
                                  fg_color="gray", hover_color="yellow")
            boton.grid(row=fila + 1, column=columna + 1, pady=(0, 20), padx=(5, 5))
            boton.configure(command=lambda btn=boton, f=fila, c=columna: cambiar_color_y_texto(btn, f, c))
            botones_asientos[fila][columna] = boton  # Guardar referencia del botón

    # Función para manejar el evento del botón de búsqueda
    def buscar_mejor_asiento_handler():
        fila, columna = buscar_mejor_asiento()
        if fila is not None and columna is not None:
            # Seleccionar y marcar el mejor asiento disponible visualmente
            boton_seleccionado = botones_asientos[fila][columna - 1]
            boton_seleccionado.configure(fg_color="green", text="O")
            estado_asientos[fila][columna - 1] = 'O'

    boton_buscar_asiento = ctk.CTkButton(frame_asientos, text="Buscar Mejor Asiento", command=buscar_mejor_asiento_handler)
    boton_buscar_asiento.grid(row=7, column=0, columnspan=7, pady=(20, 100))
    return frame_asientos  

def seleccionar_pelicula(pelicula):
    pelicula_var.set(pelicula)
    if pelicula:
        pelicula_frame.pack_forget()
        if usuario_actual == "Admin":
            mostrar_frame_admin_horarios()
        else:
            horario_frame.pack(expand=True, fill='both')
    else:
        messagebox.showwarning("Error", "Seleccione una película.")

def seleccionar_horario(horario):
    horario_var.set(horario)
    if horario:
        horario_frame.pack_forget()
        if usuario_actual == "Admin":
            mostrar_frame_admin_salas()
        else:
            sala_frame.pack(expand=True, fill='both')
    else:
        messagebox.showwarning("Error", "Seleccione un horario.")

def seleccionar_sala(sala):
    sala_var.set(sala)
    if sala:
        sala_frame.pack_forget()
        mostrar_sala()
    else:
        messagebox.showwarning("Error", "Seleccione una sala.")

def mostrar_pelicula_frame():
    pelicula_frame.pack(expand=True, fill='both')
    # Mostrar el botón "Volver" solo si el usuario es "Admin"
    if usuario_actual == "Admin":
        boton_volver_peliculas.pack(pady=10)
    else:
        boton_volver_peliculas.pack_forget()

# Funciones para mostrar los frames administrativos
def mostrar_frame_admin_peliculas():
    frame_admin_peliculas.pack(expand=True, fill='both')

def mostrar_frame_admin_horarios():
    frame_admin_horarios.pack(expand=True, fill='both')

def mostrar_frame_admin_salas():
    frame_admin_salas.pack(expand=True, fill='both')

# Gestiones administrativas
def agregar_pelicula():
    nueva_pelicula = entry_pelicula.get()
    if nueva_pelicula not in peliculas:
        peliculas.append(nueva_pelicula)
        messagebox.showinfo("Éxito", f"Película '{nueva_pelicula}' agregada.")

        #Nuevo boton de la pelicula agregada
        ctk.CTkButton(pelicula_frame, text=nueva_pelicula, command=lambda: seleccionar_pelicula(nueva_pelicula)).pack(pady=5)
        
        #limpia el Entry
        entry_pelicula.delete(0, tk.END)
    elif nueva_pelicula in peliculas:
        messagebox.showerror("Error", "La película ya existe.")
    else:
        messagebox.showerror("Error", "El campo de la película está vacío.")
    entry_pelicula.delete(0, tk.END)

def eliminar_pelicula():
    pelicula_a_eliminar = entry_pelicula.get()
    if pelicula_a_eliminar in peliculas:
        peliculas.remove(pelicula_a_eliminar)
        messagebox.showinfo("Éxito", f"Película '{pelicula_a_eliminar}' eliminada.")
        # Eliminar el botón correspondiente
        for widget in pelicula_frame.winfo_children():
            if widget.cget("text") == pelicula_a_eliminar:
                widget.destroy()
    else:
        messagebox.showerror("Error", "La película no existe.")
    entry_pelicula.delete(0, tk.END)

def agregar_horario():
    nuevo_horario = entry_horario.get()
    if nuevo_horario not in horarios:
        horarios.append(nuevo_horario)
        messagebox.showinfo("Éxito", f"Horario '{nuevo_horario}' agregado.")
        ctk.CTkButton(horario_frame, text=nuevo_horario, command=lambda: seleccionar_horario(nuevo_horario)).grid(row=2, column=0, columnspan=6, pady=5)
    elif nuevo_horario in horarios:
        messagebox.showerror("Error", "El horario ya existe.")
    else:
        messagebox.showerror("Error", "El campo del horario está vacío.")
    entry_horario.delete(0, tk.END)

def eliminar_horario():
    horario_a_eliminar = entry_horario.get()
    if horario_a_eliminar in horarios:
        horarios.remove(horario_a_eliminar)
        messagebox.showinfo("Éxito", f"Horario '{horario_a_eliminar}' eliminado.")
        # Eliminar el botón correspondiente
        for widget in horario_frame.winfo_children():
            if widget.cget("text") == horario_a_eliminar:
                widget.destroy()
    else:
        messagebox.showerror("Error", "El horario no existe.")
    entry_horario.delete(0, tk.END)

def agregar_sala():
    nueva_sala = entry_sala.get()
    if nueva_sala not in salas:
        salas.append(nueva_sala)
        messagebox.showinfo("Éxito", f"Sala '{nueva_sala}' agregada.")
        ctk.CTkButton(sala_frame, text=nueva_sala, command=lambda: seleccionar_sala(nueva_sala)).grid(row=2, column=0, columnspan=6, pady=5)
    elif nueva_sala in salas:
        messagebox.showerror("Error", "La sala ya existe.")
    else:
        messagebox.showerror("Error", "El campo de la sala está vacío.")
    entry_sala.delete(0, tk.END)

def eliminar_sala():
    sala_a_eliminar = entry_sala.get()
    if sala_a_eliminar in salas:
        salas.remove(sala_a_eliminar)
        messagebox.showinfo("Éxito", f"Sala '{sala_a_eliminar}' eliminada.")
        # Eliminar el botón correspondiente
        for widget in sala_frame.winfo_children():
            if widget.cget("text") == sala_a_eliminar:
                widget.destroy()
    else:
        messagebox.showerror("Error", "La sala no existe.")
    entry_sala.delete(0, tk.END)

# Datos de ejemplo
peliculas = ["BATMAN", "SUPERMAN", "HAIKYUU", "IT", "STAR WARS"]
horarios = ["12:00", "15:00", "18:00"]
salas = ["Sala 1", "Sala 2", "Sala 3"]

pelicula_var = tk.StringVar()
horario_var = tk.StringVar()
sala_var = tk.StringVar()
salas_var = tk.StringVar()

# Pantalla de selección de películas
pelicula_frame = ctk.CTkFrame(ventana)
pelicula_frame.pack_propagate(False)
ctk.CTkLabel(pelicula_frame, text="Seleccione una película:").pack(pady=10)

# Crear botones separados para cada película con imágenes y comando para seleccionar película
ctk.CTkButton(pelicula_frame, text="BATMAN", image=tkimage_batman, command=lambda: seleccionar_pelicula("BATMAN")).pack(pady=5)
ctk.CTkButton(pelicula_frame, text="SUPERMAN", image=tkimage_superman, command=lambda: seleccionar_pelicula("SUPERMAN")).pack(pady=5)
ctk.CTkButton(pelicula_frame, text="HAIKYUU", image=tkimage_haikyuu, command=lambda: seleccionar_pelicula("HAIKYUU")).pack(pady=5)
ctk.CTkButton(pelicula_frame, text="IT", image=tkimage_it, command=lambda: seleccionar_pelicula("IT")).pack(pady=5)
ctk.CTkButton(pelicula_frame, text="STAR WARS", image=tkimage_starwars, command=lambda: seleccionar_pelicula("STAR WARS")).pack(pady=5)
# Botón "Volver" en el frame de selección de películas
boton_volver_peliculas = ctk.CTkButton(pelicula_frame, text="Volver", command=lambda: [pelicula_frame.pack_forget(), mostrar_frame_admin_peliculas()])

# Pantalla de selección de horarios
horario_frame = ctk.CTkFrame(ventana)
horario_frame.pack_propagate(False)
ctk.CTkLabel(horario_frame, text="Seleccione un horario:").grid(row=0, column=0, columnspan=3, pady=10)

for i, horario in enumerate(horarios):
    ctk.CTkButton(horario_frame, text=horario, command=lambda h=horario: seleccionar_horario(h)).grid(row=1, column=i, padx=5, pady=5)

# Configuración para centrar los botones
horario_frame.grid_columnconfigure(0, weight=1)
horario_frame.grid_columnconfigure(1, weight=1)
horario_frame.grid_columnconfigure(2, weight=1)
horario_frame.grid_rowconfigure(0, weight=1)
horario_frame.grid_rowconfigure(1, weight=1)

# Pantalla de selección de salas
sala_frame = ctk.CTkFrame(ventana)
sala_frame.pack_propagate(False)
ctk.CTkLabel(sala_frame, text="Seleccione una sala:").grid(row=0, column=0, columnspan=3, pady=10)

for j, sala in enumerate(salas):
    ctk.CTkButton(sala_frame, text=sala, command=lambda s=sala: seleccionar_sala(s)).grid(row=1, column=j, padx=5, pady=5)

# Frames administrativos
frame_admin_peliculas = ctk.CTkFrame(ventana)
frame_admin_peliculas.pack_propagate(False)
ctk.CTkLabel(frame_admin_peliculas, text="Administrar Películas").pack(pady=10)
entry_pelicula = ctk.CTkEntry(frame_admin_peliculas)
entry_pelicula.pack(pady=5)
ctk.CTkButton(frame_admin_peliculas, text="Agregar Película", command=agregar_pelicula).pack(pady=5)
ctk.CTkButton(frame_admin_peliculas, text="Eliminar Película", command=eliminar_pelicula).pack(pady=5)
ctk.CTkButton(frame_admin_peliculas, text="Siguiente", command=lambda: [frame_admin_peliculas.pack_forget(), mostrar_pelicula_frame()]).pack(pady=20)
#ctk.CTkButton(frame_admin_peliculas, text="Volver", command=mostrar_login).pack(pady=5)

frame_admin_horarios = ctk.CTkFrame(ventana)
frame_admin_horarios.pack_propagate(False)
ctk.CTkLabel(frame_admin_horarios, text="Administrar Horarios").pack(pady=10)
entry_horario = ctk.CTkEntry(frame_admin_horarios)
entry_horario.pack(pady=5)
ctk.CTkButton(frame_admin_horarios, text="Agregar Horario", command=agregar_horario).pack(pady=5)
ctk.CTkButton(frame_admin_horarios, text="Eliminar Horario", command=eliminar_horario).pack(pady=5)
ctk.CTkButton(frame_admin_horarios, text="Siguiente", command=lambda: [frame_admin_horarios.pack_forget(), horario_frame.pack(expand=True, fill='both')]).pack(pady=20)
ctk.CTkButton(frame_admin_horarios, text="Volver", command=lambda: [frame_admin_horarios.pack_forget(), mostrar_frame_admin_peliculas()]).pack(pady=5)

frame_admin_salas = ctk.CTkFrame(ventana)
frame_admin_salas.pack_propagate(False)
ctk.CTkLabel(frame_admin_salas, text="Administrar Salas").pack(pady=10)
entry_sala = ctk.CTkEntry(frame_admin_salas)
entry_sala.pack(pady=5)
ctk.CTkButton(frame_admin_salas, text="Agregar Sala", command=agregar_sala).pack(pady=5)
ctk.CTkButton(frame_admin_salas, text="Eliminar Sala", command=eliminar_sala).pack(pady=5)
ctk.CTkButton(frame_admin_salas, text="Siguiente", command=lambda: [frame_admin_salas.pack_forget(), sala_frame.pack(expand=True, fill='both')]).pack(pady=20)
ctk.CTkButton(frame_admin_salas, text="Volver", command=lambda: [frame_admin_salas.pack_forget(), mostrar_frame_admin_horarios()]).pack(pady=5)

# Botones de "Volver"
def volver_a_peliculas():
    for frame in (horario_frame, sala_frame):
        frame.pack_forget()
    mostrar_pelicula_frame()

def volver_a_horarios():
    sala_frame.pack_forget()
    horario_frame.pack(expand=True, fill='both')

# Agregar botones de "Volver"
ctk.CTkButton(horario_frame, text="Volver", command=volver_a_peliculas).grid(row=2, column=0, columnspan=3, pady=10)
ctk.CTkButton(sala_frame, text="Volver", command=volver_a_horarios).grid(row=2, column=0, columnspan=3, pady=10)

# Mostrar la pantalla de login al iniciar
mostrar_login()

ventana.mainloop()