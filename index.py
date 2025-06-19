
import tkinter
from tkinter import messagebox, ttk  # Para los cuadros de mensaje y los widgets tipo combobox
import json  # Para manejar datos en formato JSON
import os  # Para manejar archivos y directorios
from PIL import Image, ImageTk  # Para manejar imágenes

# Definición de archivos para usuarios y turnos
archivo_usuarios = "usuarios_gym.json"
archivo_turnos = "turnos.json"
usuario_autenticado = None  # Variable global para almacenar el usuario autenticado se usa para saber si el usuario está autenticado o no
imagen_fondo = "images/background.jpg"

# Crear archivos JSON si no existen
for archivo in [archivo_usuarios, archivo_turnos]:
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            f.write("{}" if archivo == archivo_usuarios else "[]")

# Función para cargar la imagen de fondo en el canvas
def cargar_fondo(ventana, canvas):
    try:
        img = Image.open(imagen_fondo).resize((ventana.winfo_width(), ventana.winfo_height()), Image.LANCZOS) #esto lo que hace es abrir la imagen de fondo y redimensionarla al tamaño de la ventana, usando el filtro LANCZOS que es de la librería PIL para redimensionar imágenes y lo que hace es que la imagen se vea bien al redimensionarla
        imagen_cargada = ImageTk.PhotoImage(img) #esto se hace para que el tipo de imagen sea compatible con tkinter
        canvas.create_image(0, 0, anchor="nw", image=imagen_cargada) #esto lo que hace es crear una imagen en el canvas, anclada a la esquina noroeste (nw) del canvas
        canvas.image = imagen_cargada  # esto lo que hace es mantener una referencia a la imagen porque la imagen se pierde si no se mantiene una referencia a ella
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")

# Función para crear una ventana
def crear_ventana(titulo, ancho=460, alto=350):
    ventana = tkinter.Tk()  # Crea una nueva ventana
    ventana.title(titulo)  # el título de la ventana
    x_pos = (ventana.winfo_screenwidth() // 2) - (ancho // 2)  # el calculo de la posición x para centrar la ventana en la pantalla
    y_pos = (ventana.winfo_screenheight() // 2) - (alto // 2)  # el calculo de la posición y para centrar la ventana en la pantalla
    ventana.geometry(f"{ancho}x{alto}+{x_pos}+{y_pos}")  # Define el tamaño y posición
    ventana.minsize(ancho, alto)  # Establece el tamaño minimo de la ventana
    ventana.resizable(False, False)  # Evita redimensionamiento (para que no pueda el usuario cambiar el tamaño de la ventana)
    ventana.config(bg="#f0f0f0")  #  color del fondo
    canvas = tkinter.Canvas(ventana, width=ancho, height=alto, bg="#f0f0f0", highlightthickness=0)  # Crea un canvas
    canvas.grid(row=0, column=0, sticky="nsew")  # Colocar el canvas
    cargar_fondo(ventana, canvas)  # Carga la imagen de fondo
    ventana.bind("<Configure>", lambda event: cargar_fondo(ventana, canvas))  # Recargar el fondo al redimensionar (no funciona bien pero lo dejo por si acaso)
    return ventana, canvas  # Retornar ventana y canvas

# Función para crear un botón
def crear_boton(frame, texto, comando):
    boton = tkinter.Button(frame, text=texto, command=comando, width=20, **button_style)  # Crea un botón
    boton.bind("<Enter>", lambda e: boton.config(bg="#45a049"))  # Cambia el color al pasar el mouse
    boton.bind("<Leave>", lambda e: boton.config(bg="#4CAF50"))  # Vuelve al color original al salir
    return boton

# Estilo de los botones
button_style = {
    'bg': '#4CAF50',
    'fg': 'white',
    'font': ('Helvetica', 12),
    'activebackground': '#45a049',
    'relief': 'raised'
}

# Función para cargar datos desde un archivo
def cargar_datos(archivo, es_json=True):
    try:
        with open(archivo, 'r') as f:
            return json.load(f) if es_json else f.read()  # Cargar datos como JSON o texto
    except (FileNotFoundError, json.JSONDecodeError):
        return [] if es_json else {}  # Retornar vacío si hay error

# Función para guardar datos en un archivo
def guardar_datos(archivo, datos):
    with open(archivo, 'w') as f:
        json.dump(datos, f)  # Guardar datos en formato JSON

# Función para iniciar sesión
def iniciar_sesion(entry_usuario, entry_contraseña, ventana_login):
    global usuario_autenticado
    usuario = entry_usuario.get()  # Obtiene el nombre de usuario
    contraseña = entry_contraseña.get()  # Obtiene la contraseña
    if not usuario or not contraseña:
        messagebox.showwarning("Error", "Debe completar usuario y contraseña")
        return
    usuarios = cargar_datos(archivo_usuarios)  # Cargar usuarios
    if usuario not in usuarios or usuarios[usuario] != contraseña:  # verifica si el usuario y contraseña son correctos
        messagebox.showerror("Error", "Usuario o contraseña incorrecta")
        return
    usuario_autenticado = usuario  # Lo que hace es asignar el usuario autenticado a la variable global
    messagebox.showinfo("Bienvenido", f"Hola {usuario}, has iniciado sesión")
    ventana_login.destroy()  # Cerrar ventana de login, basicamente destruye la ventana actual
    abrir_menu()  # Abrir menú principal

# Función para cerrar sesión
def cerrar_sesion(ventana_actual):
    global usuario_autenticado
    usuario_autenticado = None  # Esto sirve para reiniciar la variable global del usuario autenticado
    ventana_actual.destroy()  # Esto lo que hace es destruir la ventana actual
    abrir_login()  # Volver a abrir la ventana de login

# Función para abrir el menú principal
def abrir_menu():
    ventana_menu, _ = crear_ventana("Menú Principal")  #esto lo que hace es crear una ventana para el menú principal
    frame = tkinter.Frame(ventana_menu)  # Esto lo que hace es crear un contenedor para los widgets
    frame.grid(row=0, column=0, padx=50, pady=20)  # Esto acomoda el contenedor en la ventana
    tkinter.Label(frame, text=f"Bienvenido, {usuario_autenticado}", bg="#f0f0f0", font=("Helvetica", 14)).grid(row=0, column=0, padx=50, pady=20)  # Mensaje de bienvenida

    # Botones para reservar, modificar turnos y cerrar sesión
    crear_boton(frame, "Reservar Turno", lambda: [ventana_menu.destroy(), abrir_turnero()]).grid(row=1, column=0, padx=50, pady=5)
    crear_boton(frame, "Modificar Turno", lambda: [ventana_menu.destroy(), abrir_modificacion_turnos()]).grid(row=2, column=0, padx=50, pady=5)
    crear_boton(frame, "Cerrar Sesión", lambda: cerrar_sesion(ventana_menu)).grid(row=3, column=0, padx=50, pady=5)

    ventana_menu.mainloop()  # Iniciar el bucle de eventos, esto lo que hace es iniciar el bucle de eventos de la ventana, para que se mantenga abierta y pueda interactuar con ella

#Genera los horarios

def generar_horarios_disponibles(turnos_actuales):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    horarios = list(range(6, 12)) + list(range(14, 22))
    horarios_disponibles = []

    for dia in dias:
        for hora in horarios:
             horario_str = f"{dia} - {hora}:00 - {hora+1}:00"
             ocupados = sum(1 for turno in turnos_actuales if turno["horario"] == horario_str)
             if ocupados < 8:
                 horarios_disponibles.append(horario_str)
    return horarios_disponibles

# Función para abrir la ventana de reservas
# def abrir_turnero():
#     root, _ = crear_ventana("Turnero", alto=400)  # Crea la ventana de turnero
#     frame = tkinter.Frame(root)  # Crear el contenedor para los widgets
#     frame.grid(row=0, column=0, padx=50, pady=20)  # Acomoda el contenedor en la ventana
#     tkinter.Label(frame, text="Selecciona un turno:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=50, pady=20)  # Etiqueta de selección de turno

#     # Crear lista de horarios disponibles
#     horarios_disponibles = [f"{hora}:00 - {hora+1}:00" for hora in range(8, 23)] # este es el formato de los horarios disponibles, desde las 8:00 hasta las 22:00
#     combo_horario = ttk.Combobox(frame, values=horarios_disponibles, state="readonly")  # uso combobox para que el usuario pueda ver los horarios disponibles y seleccionar uno
#     combo_horario.grid(row=1, column=0, padx=50, pady=5)  # acomoda el horario en la ventana

#     lista_turnos = tkinter.Listbox(frame)  # Lista para mostrar turnos reservados
#     lista_turnos.grid(row=2, column=0, padx=50, pady=5)  # acomoda la lista en la ventana

#     # Botones para reservar y volver al menú
#     crear_boton(frame, "Reservar Turno", lambda: reservar_turno(combo_horario, lista_turnos)).grid(row=3, column=0, padx=50, pady=5)
#     crear_boton(frame, "Volver al menú", lambda: [root.destroy(), abrir_menu()]).grid(row=4, column=0, padx=50, pady=5)

#     root.mainloop()  # Esto lo que hace es iniciar el bucle de eventos de la ventana, para que se mantenga abierta y pueda interactuar con ella

#########################


def abrir_turnero():
    root, _ = crear_ventana("Turnero", alto=500)
    frame = tkinter.Frame(root)
    frame.grid(row=0, column=0, padx=50, pady=20)
    

    # tkinter.Label(frame, text="Selecciona un día:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=50, pady=5)
    # dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    # combo_dia = ttk.Combobox(frame, values=dias_semana, state="readonly")
    # combo_dia.grid(row=1, column=0, padx=50, pady=5)

    tkinter.Label(frame, text="Selecciona un horario:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=0, padx=50, pady=5)

    turnos_actuales = cargar_datos(archivo_turnos)
    horarios_disponibles = generar_horarios_disponibles(turnos_actuales)
    combo_horario = ttk.Combobox(frame, values=horarios_disponibles, state="readonly")
    combo_horario.grid(row=3, column=0, padx=50, pady=5)

    lista_turnos = tkinter.Listbox(frame)
    lista_turnos.grid(row=4, column=0, padx=50, pady=5)
    cargar_turnos_usuario(lista_turnos)##########

    def reservar():
        #dia = combo_dia.get()
        horario = combo_horario.get()
        if not horario: # if not dia or not horario:
            messagebox.showwarning("Error", "Debes seleccionar un día y un horario.")
            return
        turno_completo = f"{horario}" #turno_completo = f"{dia} - {horario}"
        turnos = cargar_datos(archivo_turnos)
        if any(turno["horario"] == turno_completo for turno in turnos):
            messagebox.showerror("Error", f"El turno de {turno_completo} ya está ocupado.")
            return
        turnos.append({"nombre": usuario_autenticado, "horario": turno_completo})
        guardar_datos(archivo_turnos, turnos)
        messagebox.showinfo("Éxito", f"Turno reservado: {turno_completo}.")
        cargar_turnos_usuario(lista_turnos)

    crear_boton(frame, "Reservar Turno", reservar).grid(row=5, column=0, padx=50, pady=5)
    crear_boton(frame, "Volver al menú", lambda: [root.destroy(), abrir_menu()]).grid(row=6, column=0, padx=50, pady=5)

    root.mainloop()


########################
# Función para reservar un turno
def reservar_turno(combo_horario, lista_turnos): # funcion que toma el horario seleccionado y la lista de turnos y lo que hace es reservar un turno
    horario_seleccionado = combo_horario.get()  # Obtener horario seleccionado, get es un método que obtiene el valor del combobox que seleccionó el usuario
    ########################
    cargar_turnos_usuario(lista_turnos) #############@
    ########################
    if sum(1 for turno in turnos if turno["horario"] == horario_seleccionado) >= 8:
        messagebox.showerror("Error", f"El turno de {horario_seleccionado} ya alcanzó el límite de 8 personas.")
        return
    if not horario_seleccionado:
        messagebox.showwarning("Error", "Selecciona un horario.")
        return
    turnos = cargar_datos(archivo_turnos)  # Cargar turnos
    if any(turno["horario"] == horario_seleccionado for turno in turnos):  # Verificar disponibilidad del turno
        messagebox.showerror("Error", f"El turno de {horario_seleccionado} ya está ocupado.")
        return
    turnos.append({"nombre": usuario_autenticado, "horario": horario_seleccionado})  # Añade el nuevo turno a la lista de turnos
    guardar_datos(archivo_turnos, turnos)  # Guardar turnos
    messagebox.showinfo("Éxito", f"Turno reservado: {horario_seleccionado}.")  # Mensaje de éxito
    cargar_turnos_usuario(lista_turnos)  # Actualizar lista de turnos
    combo_horario['values'] = generar_horarios_disponibles(cargar_datos(archivo_turnos))

# Función para cargar turnos del usuario en la lista
def cargar_turnos_usuario(lista_turnos):
    lista_turnos.delete(0, tkinter.END)  # esto lo que hace es limpiar la lista de turnos antes de cargar los nuevos para que no se repitan los turnos
    turnos = [turno["horario"] for turno in cargar_datos(archivo_turnos) if turno["nombre"] == usuario_autenticado]  # Obtener turnos del usuario para mostrar solo los turnos reservados por el usuario autenticado y no por todos los usuarios
    for turno in turnos:
        lista_turnos.insert(tkinter.END, turno)  # esto lo que hace es insertar los turnos en la lista de turnos, para que el usuario pueda ver los turnos que ha reservado

# Función para abrir la ventana de modificación de turnos
def abrir_modificacion_turnos():
    ventana_modificacion_turnos, _ = crear_ventana("Cambiar horario", alto=400)  # Crea la ventana de modificación de turnos
    frame = tkinter.Frame(ventana_modificacion_turnos)  # Crear el contenedor de widgets
    frame.grid(row=0, column=0, padx=50, pady=20)  # acomoda el contenedor en la ventana
    tkinter.Label(frame, text="Tus turnos:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=50, pady=20)  # Etiqueta de turnos

    lista_turnos = tkinter.Listbox(frame)  # Esta es la lista donde se muestran los turnos reservados por el usuario
    lista_turnos.grid(row=1, column=0, padx=50, pady=5)  # Acomoda la lista en la ventana
    cargar_turnos_usuario(lista_turnos)  # Carga los turnos del usuario en la lista de turnos

    # Botones para eliminar, cambiar y volver
    crear_boton(frame, "Eliminar Turno", lambda: eliminar_turno(lista_turnos)).grid(row=2, column=0, padx=50, pady=5) #lambda se pone para que se ejecute la función eliminar_turno cuando se presione el botón
    crear_boton(frame, "Cambiar Horario", lambda: modificar_turno(ventana_modificacion_turnos, lista_turnos)).grid(row=3, column=0, padx=50, pady=5)
    crear_boton(frame, "Volver al menú", lambda: [ventana_modificacion_turnos.destroy(), abrir_menu()]).grid(row=4, column=0, padx=50, pady=5)

    ventana_modificacion_turnos.mainloop()  # esto lo que hace es iniciar el bucle de eventos de la ventana, para que se mantenga abierta y pueda interactuar con ella

# Función para modificar un turno seleccionado
def modificar_turno(root, lista_turnos): # recibe la ventana actual y la lista de turnos para que el usuario pueda modificar un turno
    seleccionado = lista_turnos.curselection()  # Esto lo que hace es obtener el turno seleccionado por el usuario en la lista de turnos
    if not seleccionado: # Si no hay un turno seleccionado, cuando el usuario presione el botón de modificar turno, se mostrará un mensaje de advertencia
        messagebox.showwarning("Error", "Selecciona un turno para modificar.")
        return

    turno_actual = lista_turnos.get(seleccionado)  # Obtener turno actual para modificarlo

    ventana_modificar = tkinter.Toplevel(root)  # Crear ventana para modificar un turno
    ventana_modificar.title("Modificar Turno")  # Título de la ventana
    ventana_modificar.geometry("300x200")  # Tamaño de la ventana
    ventana_modificar.configure(bg="white")  # Color de fondo

    tkinter.Label(ventana_modificar, text=f"Turno actual: {turno_actual}", bg="white").grid(row=0, column=0, padx=50, pady=20)  # Etiqueta para mostrar el turno actual

    # Crear combobox de nuevos horarios
    ##################
    turnos_actuales = cargar_datos(archivo_turnos)
    horarios_disponibles = generar_horarios_disponibles(turnos_actuales)
    combo_horario = ttk.Combobox(ventana_modificar, values=horarios_disponibles, state="readonly")
    combo_horario.grid(row=1, column=0, padx=50, pady=5)
    ##################

    # horarios_disponibles = [f"{hora}:00 - {hora+1}:00" for hora in range(8, 23)] # esta lista contiene los horarios disponibles para que el usuario pueda seleccionar uno nuevo
    # combo_nuevo_horario = ttk.Combobox(ventana_modificar, values=horarios_disponibles, state="readonly") # Combobox para seleccionar nuevo horario
    # combo_nuevo_horario.grid(row=1, column=0, padx=50, pady=5) # Esto lo que hace es colocar el combobox en la ventana de modificación de turnos

    # Botones para confirmar cambio o cancelar
    tkinter.Button(ventana_modificar, text="Confirmar Cambio", command=lambda: actualizar_turno(turno_actual, combo_horario, ventana_modificar, lista_turnos)).grid(row=2, column=0, padx=50, pady=5)
    tkinter.Button(ventana_modificar, text="Cancelar", command=ventana_modificar.destroy).grid(row=3, column=0, padx=50, pady=5) # esto lo que hace es colocar el botón de cancelar en la ventana de modificación de turnos, para que el usuario pueda cancelar la modificación del turno

# Función para eliminar un turno seleccionado
def eliminar_turno(lista_turnos):
    seleccionado = lista_turnos.curselection()  # Obtiene el turno seleccionado en la lista de turnos por el usuario
    if not seleccionado:
        messagebox.showwarning("Error", "Selecciona un turno para eliminar.") #esto me asegura que el usuario seleccione un turno antes de intentar eliminarlo, si no hay un turno seleccionado, se mostrará un mensaje de advertencia
        return
    turnos = cargar_datos(archivo_turnos)  # esta es la función que carga los turnos desde el archivo JSON, para que pueda eliminar el turno seleccionado por el usuario
    turno_a_eliminar = lista_turnos.get(seleccionado)  # Obtiene el turno seleccionado para eliminarlo
    turnos = [turno for turno in turnos if turno["nombre"] != usuario_autenticado or turno["horario"] != turno_a_eliminar]  # Esto lo que hace es filtrar los turnos, eliminando el turno seleccionado por el usuario, si el turno pertenece al usuario autenticado
    guardar_datos(archivo_turnos, turnos)  # Guardar cambios
    cargar_turnos_usuario(lista_turnos)  # Actualiza la lista de turnos
    messagebox.showinfo("Éxito", "Turno eliminado correctamente.")  # Mensaje de éxito

# Función para actualizar un turno con un nuevo horario
def actualizar_turno(turno_actual, combo_nuevo_horario, ventana_modificar, lista_turnos): # esta funcion recibe el turno actual, el combobox con los nuevos horarios, la ventana de modificación y la lista de turnos
    nuevo_horario = combo_nuevo_horario.get()  # obtiene el nuevo horario seleccionado por el usuario
    if not nuevo_horario: # esto controla si el horario es el mismo que el actual, si no hay un nuevo horario seleccionado, se mostrará un mensaje de advertencia
        messagebox.showwarning("Error", "Selecciona un nuevo horario.")
        return

    turnos = cargar_datos(archivo_turnos)  # Carga los turnos desde el archivo JSON

    for turno in turnos: # Recorre los turnos para encontrar el que se va a modificar
        if turno["nombre"] == usuario_autenticado and turno["horario"] == turno_actual:  # esto lo que hace es buscar el turno del usuario autenticado que coincide con el turno actual
            turno["horario"] = nuevo_horario  # Aca se actualiza el horario del turno seleccionado por el usuario
            break                           # Esto se hace para salir del bucle una vez que se ha encontrado y modificado el turno

    guardar_datos(archivo_turnos, turnos)  # Guarda los cambios
    cargar_turnos_usuario(lista_turnos)  # Actualiza la lista

    messagebox.showinfo("Éxito", f"Turno cambiado a: {nuevo_horario}.", parent=ventana_modificar)  # Mensaje de éxito
    ventana_modificar.destroy()  # Cierra la ventana de modificación

# Función para abrir la ventana de inicio de sesión
def abrir_login():
    global usuario_autenticado # esto me sirve para acceder a la variable global usuario_autenticado, que se usa para saber si el usuario está autenticado o no
    if usuario_autenticado:
        return abrir_menu()  # Si ya está autenticado, abrir menú y si no está autenticado, se abre la ventana de inicio de sesión

    ventana_login, _ = crear_ventana("Inicio de Sesión")  # Crear ventana de login, el _ es para ignorar el segundo valor que retorna la función crear_ventana, que es el canvas, ya que no lo vamos a usar en esta ventana porque no vamos a usar un canvas en esta ventana
    frame = tkinter.Frame(ventana_login)  # Crear contenedor
    frame.grid(row=0, column=0, padx=20, pady=20)  # acomodar el contenedor en la ventana

    # Etiquetas y campos de texto para usuario y contraseña
    tkinter.Label(frame, text="Usuario:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_usuario = tkinter.Entry(frame)            #esto es un campo de texto para que el usuario ingrese su nombre de usuario
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    tkinter.Label(frame, text="Contraseña:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_contraseña = tkinter.Entry(frame, show="*")  # Esto es un campo de texto para que el usuario ingrese su contraseña, el show="*" es para que la contraseña se muestre como asteriscos
    entry_contraseña.grid(row=1, column=1, padx=10, pady=5)

    button_frame = tkinter.Frame(frame)  # esto es un contenedor para los botones de inicio de sesión y registro
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)  # esto acomoda el contenedor de botones en la ventana

    # Botones para iniciar sesión y registrarse
    crear_boton(button_frame, "Iniciar Sesión", lambda: iniciar_sesion(entry_usuario, entry_contraseña, ventana_login)).grid(row=0, column=0, padx=10) # esto lo que hace es iniciar sesión cuando el usuario presiona el botón de iniciar sesión, llamando a la función iniciar_sesion con los campos de usuario y contraseña y la ventana de inicio de sesión
    crear_boton(button_frame, "Registrarse", lambda: [ventana_login.destroy(), abrir_registro()]).grid(row=0, column=1, padx=10) # esto lo que hace es abrir la ventana de registro cuando el usuario presiona el botón de registrarse y destruir la ventana de inicio de sesión actual

    ventana_login.mainloop()  # esto lo que hace es iniciar el bucle de eventos de la ventana, para que se mantenga abierta y pueda interactuar con ella

# Función para abrir la ventana de registro
def abrir_registro():
    ventana_registro, _ = crear_ventana("Registro de Usuario", alto=300)  # Crear ventana de registro y el _ es para ignorar el segundo valor que retorna la función crear_ventana, que es el canvas, ya que no lo vamos a usar en esta ventana porque no vamos a usar un canvas en esta ventana
    frame = tkinter.Frame(ventana_registro)  # Crea el contenedor
    frame.grid(row=0, column=0, padx=20, pady=20)  # acomoda el contenedor en la ventana

    # Etiquetas y campos de texto para nombre de usuario, contraseña y confirmación
    tkinter.Label(frame, text="Nombre de Usuario:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_usuario = tkinter.Entry(frame) # esto sirve para que el usuario ingrese su nombre de usuario
    entry_usuario.grid(row=0, column=1, padx=10, pady=5)

    tkinter.Label(frame, text="Contraseña:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_contraseña = tkinter.Entry(frame, show="*") # Campo para ingresar contraseña y el show="*" es para que la contraseña se muestre como asteriscos
    entry_contraseña.grid(row=1, column=1, padx=10, pady=5)

    tkinter.Label(frame, text="Confirmar Contraseña:", bg="#f0f0f0", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_confirmar_contraseña = tkinter.Entry(frame, show="*")  # Campo para confirmar contraseña
    entry_confirmar_contraseña.grid(row=2, column=1, padx=10, pady=5)

    button_frame = tkinter.Frame(frame)  # Crear contenedor para botones
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)  # acomodar el contenedor de botones en la ventana
    # Botones para crear usuario y volver al login
    crear_boton(button_frame, "Crear Usuario", lambda: crear_usuario(entry_usuario, entry_contraseña, entry_confirmar_contraseña, ventana_registro)).grid(row=0, column=0, padx=10) #esto lo que hace es crear un nuevo usuario cuando el usuario presiona el botón de crear usuario, llamando a la función crear_usuario con los campos de usuario, contraseña y confirmar contraseña y la ventana de registro
    crear_boton(button_frame, "Volver", lambda: [ventana_registro.destroy(), abrir_login()]).grid(row=0, column=1, padx=10) #esto lo que hace es volver a la ventana de inicio de sesión cuando el usuario presiona el botón de volver y destruir la ventana de registro actual

    ventana_registro.mainloop()  #esto lo que hace es iniciar el bucle de eventos de la ventana, para que se mantenga abierta y pueda interactuar con ella

# Función para crear un nuevo usuario
def crear_usuario(entry_usuario, entry_contraseña, entry_confirmar_contraseña, ventana_registro): #esta función recibe los campos de usuario, contraseña y confirmar contraseña y la ventana de registro y lo que hace es crear un nuevo usuario si los datos son válidos
    usuario = entry_usuario.get()  # Obtener nombre de usuario que el usuario ingresó
    contraseña = entry_contraseña.get()  # Obtener contraseña que el usuario ingresó
    confirmar_contraseña = entry_confirmar_contraseña.get()  # Obtiene la confirmación de contraseña que el usuario ingresó

    if not usuario or not contraseña or not confirmar_contraseña: # esto lo que hace es verificar si los campos de usuario, contraseña y confirmar contraseña están vacíos, si alguno de ellos está vacío, se mostrará un mensaje de advertencia
        messagebox.showwarning("Error", "Debe completar todos los campos.")  # Advertencia si hay campos vacíos
        return

    if contraseña != confirmar_contraseña: #esto lo que hace es verificar si la contraseña y la confirmación de contraseña son iguales, si no son iguales, se mostrará un mensaje de advertencia
        messagebox.showwarning("Error", "Las contraseñas no coinciden.")  # Advertencia si las contraseñas no coinciden
        return

    usuarios = cargar_datos(archivo_usuarios)  # Esto lo que hace es darme los usuarios existentes desde el archivo JSON, para que pueda verificar si el usuario ya existe o no
    if usuario in usuarios: # Esto lo que hace es verificar si el usuario ya existe en el archivo JSON, si el usuario ya existe, se mostrará un mensaje de error
        messagebox.showerror("Error", "Ese usuario ya existe.")  # Advertencia si el usuario ya existe
        return

    usuarios[usuario] = contraseña  # si todos los datos son válidos, se agrega el nuevo usuario al diccionario de usuarios con su contraseña correspondiente
    guardar_datos(archivo_usuarios, usuarios)  # Guardar cambios de usuarios en el archivo JSON
    messagebox.showinfo("Registrado", "Usuario creado con éxito.")  # Mensaje de éxito
    ventana_registro.destroy()  # Cerrar ventana de registro destruye la ventana de registro actual
    abrir_login()  # Volver a la ventana de login para que el usuario pueda iniciar sesión

# Iniciar el programa abriendo la ventana de inicio de sesión
abrir_login()
