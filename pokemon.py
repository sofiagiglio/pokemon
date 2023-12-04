# Importa la biblioteca "requests" para realizar solicitudes HTTP a la API de Pokémon.
# "requests" es una biblioteca que permite realizar solicitudes HTTP en Python.
import requests  

# Importa la biblioteca "tkinter" y la renombra como "tk" para crear la interfaz gráfica de usuario (GUI).
# "tkinter" es una biblioteca estándar de Python para crear interfaces gráficas.
import tkinter as tk  

# Importa la función "messagebox" de tkinter para mostrar ventanas emergentes de mensajes de error o información.
# "messagebox" es una función que proporciona ventanas emergentes para mostrar mensajes al usuario.
from tkinter import messagebox  

# Importa la biblioteca "io" para trabajar con datos en memoria, utilizada para procesar datos de imágenes.
# "io" es una biblioteca que proporciona herramientas para trabajar con flujos de datos en memoria.
import io  

# Importa la biblioteca "PIL" (Python Imaging Library) y sus módulos "Image" e "ImageTk" para trabajar con imágenes y mostrarlas en la GUI.
# "PIL" es una biblioteca para trabajar con imágenes en Python.
from PIL import Image, ImageTk  

# Importa la biblioteca "random" para generar números aleatorios y seleccionar un Pokémon al azar.
# "random" es una biblioteca que proporciona funciones para trabajar con números aleatorios en Python.
import random  


# Inicializa una variable para realizar un seguimiento del puntaje más alto.
mayor_puntaje = 0  

# Inicializa una variable para realizar un seguimiento de la racha actual de Pokémon adivinados.
racha_actual = 0  

# Inicializa una variable para realizar un seguimiento de las vidas del jugador.
vidas = 3  

# Inicializa una variable para realizar un seguimiento de la puntuación actual.
puntuacion = 0  


# Función para obtener una lista de nombres de Pokémon desde pokeapi.
def pokelista():
    # Define la URL de la API de Pokémon para obtener la lista de Pokémon.
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1000'  

    # Realiza una solicitud HTTP a la API para obtener la información.
    response = requests.get(url)  

    # Comprueba si la solicitud fue exitosa.
    if response.status_code == 200:  
        # Procesa la respuesta de la API y la convierte en un objeto Python.
        data = response.json()  
        
        # Extrae los nombres de los Pokémon de los datos de la API.
        pokenombres = [pokemon['name'] for pokemon in data['results']]  
        
        # Devuelve la lista de nombres de Pokémon.
        return pokenombres  
    else:
        # Muestra un mensaje de error si la solicitud falla.
        messagebox.showerror("Error", "No se pudo obtener la lista de Pokémon")  
        
        # Devuelve una lista vacía en caso de error.
        return []  


# Llama a la función para obtener la lista de nombres de Pokémon y almacena los nombres en la variable "pokelista".
pokelista = pokelista()  

# Inicializa una lista para realizar un seguimiento de los Pokémon adivinados.
pokemon_adivinados = []  


# Función para seleccionar un Pokémon al azar y mostrarlo en el juego.
def pokerandom():
    # Indica que se utilizarán variables globales en la función.
    global pokemon_actual, racha_actual, pokemon_adivinados  
    
    # Restablece la racha de Pokémon adivinados.
    racha_actual = 0  
    
    # Borra el texto en un widget llamado "result_label".
    result_label.config(text="")  
    
    # Inicia un bucle infinito
    while True: 
        # Selecciona un Pokémon al azar que no ha sido adivinado previamente.
        pokemon_actual = random.choice(pokelista)  
        
        # Verifica si el Pokémon seleccionado no ha sido adivinado.
        if pokemon_actual not in pokemon_adivinados:  
            break  # Sale del bucle si el Pokémon es nuevo (no ha sido adivinado).

    # Crea una URL para obtener información sobre el Pokémon seleccionado.
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_actual}/'  
    
    # Realiza una solicitud HTTP para obtener información sobre el Pokémon.
    response = requests.get(url)  

    # Comprueba si la solicitud fue exitosa.
    if response.status_code == 200:  
        # Procesa la respuesta de la API y la convierte en un objeto Python.
        data = response.json()  

        # Obtiene la URL de la imagen del Pokémon.
        image_url = data['sprites']['front_default']  

        # Realiza una segunda solicitud para obtener los datos de la imagen.
        response = requests.get(image_url)  
        
        # Obtiene los datos de la imagen.
        img_data = response.content  

        # Crea una imagen a partir de los datos.
        img = Image.open(io.BytesIO(img_data))  

        # Convierte la imagen en un objeto para mostrar en la GUI.
        img = ImageTk.PhotoImage(img, width=100, height=70)  

        # Configura la imagen en un widget llamado "image_label".
        image_label.config(image=img, compound=tk.CENTER)  
        
        # Asigna la imagen al widget.
        image_label.image = img  


# Función para reiniciar el juego.
def pokereiniciar():
    # Indica que se utilizarán variables globales en la función.
    global puntuacion, vidas, pokemon_actual  
    
    # Restablece la puntuación a 0.
    puntuacion = 0  
    
    # Restablece las vidas a 3.# Importa la biblioteca "random" para generar números aleatorios y seleccionar un Pokémon al azar.
# "random" es una biblioteca que proporciona
    
    # Llama a la función "pokerandom" para seleccionar un nuevo Pokémon al azar.
    pokerandom()  
    
    # Actualiza el texto de la etiqueta de puntuación con el valor de la variable "puntuacion".
    puntuacion_label.config(text=f"Puntuación: {puntuacion}")  
    
    # Actualiza el texto de la etiqueta de vidas con el valor de la variable "vidas".
    vidas_label.config(text=f"Vidas: {vidas}")  
    
    # Borra el texto en la etiqueta "result_label" estableciéndolo como una cadena vacía.
    result_label.config(text="")  
    
    # Borra el contenido del campo de entrada de texto, desde el índice 0 hasta el final (tk.END).
    entry.delete(0, tk.END)  


# Función para comprobar si el Pokémon adivinado es correcto.
def pokecomprobar():
    # Indica que se utilizarán variables globales en la función.
    global puntuacion, vidas, mayor_puntaje, racha_actual, pokemon_actual, pokemon_adivinados  
    
    # Verifica si hay un Pokémon actual seleccionado.
    if pokemon_actual is not None:  
        # Obtiene la conjetura del jugador y la convierte a minúsculas.
        guess = entry.get().lower()  

        # Comprueba si la conjetura es correcta y no ha sido adivinada antes.
        if guess == pokemon_actual and guess not in pokemon_adivinados:  
            # Aumenta la puntuación si es correcta.
            puntuacion += 1  
            
            # Aumenta la racha actual de Pokémon adivinados.
            racha_actual += 1  

            # Actualiza el puntaje más alto si es necesario.
            if puntuacion > mayor_puntaje:  
                mayor_puntaje = puntuacion  

            # Agrega el Pokémon a la lista de adivinados.
            pokemon_adivinados.append(pokemon_actual)  
            
            # Obtiene información adicional del Pokémon.
            pokeinfo(pokemon_actual)  

            # Actualiza la etiqueta de puntuación en la GUI.
            puntuacion_label.config(text=f"Puntuación: {puntuacion}")  

            # Muestra un mensaje si se alcanza una racha de 5 Pokémon adivinados.
            if racha_actual == 5:  
                # Aparece una ventana cuando llegas a los 5 pokemones adivinados, mostrando los que tiene escrito ahí.
                messagebox.showinfo("Logro desbloqueado", "¡Has alcanzado una racha de 5 Pokémon adivinados!")  

        else:
            # Reduce una vida si la conjetura es incorrecta.
            vidas -= 1  
            
            # Restablece la racha de Pokémon adivinados a 0.
            racha_actual = 0  

            # Muestra un mensaje si se pierden todas las vidas.
            if vidas >= 0:
                if vidas == 0:
                    # Aparece una ventana diciendo que perdiste, el nombre del pokemon que tenías que adivinar y tu puntuación final.
                    messagebox.showinfo("Juego terminado", f"Perdiste todas tus vidas. El Pokémon era: {pokemon_actual}. Tu puntuación final es: {puntuacion}")  
                    # Reinicia el juego cuando se pierden todas las vidas.
                    pokereiniciar()  

                elif guess != pokemon_actual and guess not in pokemon_adivinados:
                    # Esto asegura que el jugador no ha adivinado previamente el mismo Pokémon incorrectamente.
                    # Aparece una ventana cuando pierdes una vida, el nombre del pokemon que tenías que adivinar y cuántas vidas te quedan.
                    messagebox.showerror("Incorrecto", f"Inténtalo de nuevo. Te quedan {vidas} vidas. El Pokémon era: {pokemon_actual}")  

                    # Llama a "pokerandom" para seleccionar un nuevo Pokémon.
                    if vidas >= 0:  
                        pokerandom()  


    # Actualiza el texto de la etiqueta "vidas_label" con la cantidad de vidas actual (variable "vidas").
    vidas_label.config(text=f"Vidas: {vidas}")  
    
    # Actualiza el texto de la etiqueta "mayor_puntaje_label" con el puntaje más alto actual (variable "mayor_puntaje").
    mayor_puntaje_label.config(text=f"Puntuación más alta: {mayor_puntaje}")  


# Función para obtener información detallada del Pokémon.
def pokeinfo(pokemon_name):
    # Crea una URL para obtener información del Pokémon.
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'  
    
    # Realiza una solicitud HTTP para obtener información.
    response = requests.get(url)  

    # Comprueba si la solicitud fue exitosa.
    if response.status_code == 200:  
        # Procesa los datos de la API.
        data = response.json()  

        # Calcula la altura en centímetros.
        altura_cm = data['height'] * 10  
        
        # Calcula el peso en kilogramos.
        peso_kg = data['weight'] / 10  

        # Crea una cadena de texto con información del Pokémon: Nombre, id, altura(cm), peso(kg) y tipo.
        pokemon_info = f"Nombre: {data['name'].capitalize()}\n" \
                       f"ID: {data['id']}\n" \
                       f"Altura: {altura_cm} cm\n" \
                       f"Peso: {peso_kg} kg\n" \
                       "Tipos: " + ", ".join([t['type']['name'] for t in data['types']])
        
        # Muestra la información en un widget llamado "result_label".
        result_label.config(text=pokemon_info)  

    else:
        # Muestra un mensaje si la información no está disponible.
        result_label.config(text="Información del Pokémon no disponible")  


# Función para mostrar una pista sobre el Pokémon actual.
def pokepista():
    # Verifica si hay un Pokémon actual seleccionado.
    if pokemon_actual is not None:  
        # Obtiene la primera letra del nombre del Pokémon y la convierte a mayúsculas.
        inicial = pokemon_actual[0].upper()  
        
        # Muestra una ventana emergente con la pista.
        messagebox.showinfo("Pista", f"El nombre del Pokémon empieza con: {inicial}")  


# Creación de la ventana del juego.
app = tk.Tk()  # Crea una ventana principal de la GUI.
app.title("Adivina el Pokémon")  # Establece el título de la ventana.

# Abre una imagen de fondo.
background_image = Image.open('pokedex.jpg')  

# Convierte la imagen en un objeto compatible con tkinter.
background_photo = ImageTk.PhotoImage(background_image)  

# Crea una etiqueta para mostrar la imagen de fondo.
background_label = tk.Label(app, image=background_photo)  

# Ajusta la posición y el tamaño de la etiqueta en la ventana.
background_label.place(x=0, y=0, relwidth=1, relheight=1)  

# Crea una etiqueta con un texto.
label = tk.Label(app, text="¿Quién es ese Pokémon?:")  

# Coloca la etiqueta en la ventana.
label.pack()  

# Crea un campo de entrada de texto.
entry = tk.Entry(app)  

# Coloca el campo de entrada en la ventana.
entry.pack()  

# Crea un botón para comprobar la conjetura.
check_button = tk.Button(app, text="Comprobar", command=pokecomprobar)  

# Coloca el botón en la ventana.
check_button.pack()  

# Crea un botón para pasar al siguiente Pokémon.
pokerandom_button = tk.Button(app, text="Siguiente Pokémon", command=pokerandom)  
# Coloca el botón en la ventana.
pokerandom_button.pack()  

# Crea una etiqueta para mostrar la imagen del Pokémon.
image_label = tk.Label(app)  

# Coloca la etiqueta en la ventana.
image_label.pack()  

# Crea una etiqueta para mostrar información del Pokémon.
result_label = tk.Label(app, text="")  

# Coloca la etiqueta en la ventana.
result_label.pack()  

# Establece el tamaño de la ventana.
app.geometry("400x400")  

# Crea una etiqueta para mostrar la puntuación actual.
puntuacion_label = tk.Label(app, text=f"Puntuación: {puntuacion}")  

# Coloca la etiqueta en la ventana.
puntuacion_label.pack()  

# Crea una etiqueta para mostrar la cantidad de vidas.
vidas_label = tk.Label(app, text=f"Vidas: {vidas}")  

# Coloca la etiqueta en la ventana.
vidas_label.pack()  

# Crea una etiqueta para mostrar el puntaje más alto.
mayor_puntaje_label = tk.Label(app, text=f"Puntuación más alta: {mayor_puntaje}")  

# Coloca la etiqueta en la ventana.
mayor_puntaje_label.pack()  

# Crea un botón con etiqueta "Pista" que llama a la función "pokepista".
pista_button = tk.Button(app, text="Pista", command=pokepista)  

# Coloca el botón en la ventana.
pista_button.pack()  

# Inicia la aplicación y muestra la ventana principal.
app.mainloop() 