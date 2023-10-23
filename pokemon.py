import requests  # Importa la biblioteca "requests" para hacer solicitudes HTTP a la API de Pokémon.
import tkinter as tk  # Importa la biblioteca "tkinter" y la renombra como "tk" para crear la interfaz gráfica de usuario (GUI).
from tkinter import messagebox  # Importa la función "messagebox" de tkinter para mostrar ventanas emergentes de mensajes de error o información.
import io  # Importa la biblioteca "io" para trabajar con datos en memoria, que se utiliza para procesar datos de imágenes.
from PIL import Image, ImageTk  # Importa la biblioteca "PIL" (Python Imaging Library) y sus módulos "Image" y "ImageTk" para trabajar con imágenes y mostrarlas en la GUI.
import random  # Importa la biblioteca "random" para generar números aleatorios y seleccionar Pokémon al azar.

mayor_puntaje = 0  # Inicializa una variable para realizar un seguimiento del puntaje más alto.
racha_actual = 0  # Inicializa una variable para realizar un seguimiento de la racha actual de Pokémon adivinados.
vidas = 3  # Inicializa una variable para realizar un seguimiento de las vidas del jugador.
puntuacion = 0  # Inicializa una variable para realizar un seguimiento de la puntuación actual.

# Función para obtener una lista de nombres de Pokémon desde una página web.
def pokelista():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1000'  # Define la URL de la API de Pokémon para obtener la lista de Pokémon.
    response = requests.get(url)  # Realiza una solicitud HTTP a la API para obtener la información.

    if response.status_code == 200:  # Comprueba si la solicitud fue exitosa.
        data = response.json()  # Procesa la respuesta de la API y la convierte en un objeto Python.
        pokenombres = [pokemon['name'] for pokemon in data['results']]  # Extrae los nombres de los Pokémon de los datos de la API.
        return pokenombres  # Devuelve la lista de nombres de Pokémon.
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de Pokémon")  # Muestra un mensaje de error si la solicitud falla.
        return []  # Devuelve una lista vacía en caso de error.

pokelista = pokelista()  # Llama a la función para obtener la lista de nombres de Pokémon y almacena los nombres en la variable "pokelista".
pokemon_adivinados = []  # Inicializa una lista para realizar un seguimiento de los Pokémon adivinados.

# Función para seleccionar un Pokémon al azar y mostrarlo en el juego.
def pokerandom():
    global pokemon_actual, racha_actual, pokemon_adivinados  # Indica que se utilizarán variables globales en la función.
    racha_actual = 0  # Restablece la racha de Pokémon adivinados.
    result_label.config(text="")  # Borra el texto en un widget llamado "result_label".

    while True:
        pokemon_actual = random.choice(pokelista)  # Selecciona un Pokémon al azar que no ha sido adivinado previamente.
        if pokemon_actual not in pokemon_adivinados:  # Verifica si el Pokémon seleccionado no ha sido adivinado.
            break

    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_actual}/'  # Crea una URL para obtener información sobre el Pokémon seleccionado.
    response = requests.get(url)  # Realiza una solicitud HTTP para obtener información sobre el Pokémon.

    if response.status_code == 200:  # Comprueba si la solicitud fue exitosa.
        data = response.json()  # Procesa la respuesta de la API y la convierte en un objeto Python.

        image_url = data['sprites']['front_default']  # Obtiene la URL de la imagen del Pokémon.

        response = requests.get(image_url)  # Realiza una segunda solicitud para obtener los datos de la imagen.
        img_data = response.content  # Obtiene los datos de la imagen.

        img = Image.open(io.BytesIO(img_data))  # Crea una imagen a partir de los datos.
        img = ImageTk.PhotoImage(img, width=100, height=70)  # Convierte la imagen en un objeto para mostrar en la GUI.

        image_label.config(image=img, compound=tk.CENTER)  # Configura la imagen en un widget llamado "image_label".
        image_label.image = img  # Asigna la imagen al widget.

# Función para reiniciar el juego.
def pokereiniciar():
    global puntuacion, vidas, pokemon_actual  # Indica que se utilizarán variables globales en la función.
    puntuacion = 0  # Restablece la puntuación a 0.
    vidas = 3  # Restablece las vidas a 3.
    pokemon_adivinados.clear()  # Borra la lista de Pokémon adivinados.
    pokerandom()  # Llama a la función "pokerandom" para seleccionar un nuevo Pokémon al azar.
    puntuacion_label.config(text=f"Puntuación: {puntuacion}")
    vidas_label.config(text=f"Vidas: {vidas}")
    result_label.config(text="")
    entry.delete(0, tk.END)

# Función para comprobar si el Pokémon adivinado es correcto.
def pokecomprobar():
    global puntuacion, vidas, mayor_puntaje, racha_actual, pokemon_actual, pokemon_adivinados  # Indica que se utilizarán variables globales en la función.

    if pokemon_actual is not None:  # Verifica si hay un Pokémon actual seleccionado.
        guess = entry.get().lower()  # Obtiene la conjetura del jugador y la convierte a minúsculas.

        if guess == pokemon_actual and guess not in pokemon_adivinados:  # Comprueba si la conjetura es correcta y no ha sido adivinada antes.
            puntuacion += 1  # Aumenta la puntuación si es correcta.
            racha_actual += 1  # Aumenta la racha actual de Pokémon adivinados.

            if puntuacion > mayor_puntaje:  # Actualiza el puntaje más alto si es necesario.
                mayor_puntaje = puntuacion

            pokemon_adivinados.append(pokemon_actual)  # Agrega el Pokémon a la lista de adivinados.
            pokeinfo(pokemon_actual)  # Obtiene información adicional del Pokémon.

            puntuacion_label.config(text=f"Puntuación: {puntuacion}")  # Actualiza la etiqueta de puntuación en la GUI.

            if racha_actual == 5:  # Muestra un mensaje si se alcanza una racha de 5 Pokémon adivinados.
                messagebox.showinfo("Logro desbloqueado", "¡Has alcanzado una racha de 5 Pokémon adivinados!")

        else:
            vidas -= 1  # Reduce una vida si la conjetura es incorrecta.
            racha_actual = 0  # Restablece la racha de Pokémon adivinados a 0.

            if vidas >= 0:
                if vidas == 0:
                    messagebox.showinfo("Juego terminado", f"Perdiste todas tus vidas. El Pokémon era: {pokemon_actual}. Tu puntuación final es: {puntuacion}")
                    pokereiniciar()  # Reinicia el juego cuando se pierden todas las vidas.

                elif guess != pokemon_actual and guess not in pokemon_adivinados:
                    messagebox.showerror("Incorrecto", f"Inténtalo de nuevo. Te quedan {vidas} vidas. El Pokémon era: {pokemon_actual}")

                if vidas >= 0:
                    pokerandom()  # Llama a "pokerandom" para seleccionar un nuevo Pokémon.

    vidas_label.config(text=f"Vidas: {vidas}")
    mayor_puntaje_label.config(text=f"Puntuación más alta: {mayor_puntaje}")

# Función para obtener información detallada del Pokémon.
def pokeinfo(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'  # Crea una URL para obtener información del Pokémon.
    response = requests.get(url)  # Realiza una solicitud HTTP para obtener información.

    if response.status_code == 200:  # Comprueba si la solicitud fue exitosa.
        data = response.json()  # Procesa los datos de la API.

        altura_cm = data['height'] * 10  # Calcula la altura en centímetros.
        peso_kg = data['weight'] / 10  # Calcula el peso en kilogramos.

        # Crea una cadena de texto con información del Pokémon.
        pokemon_info = f"Nombre: {data['name'].capitalize()}\n" \
                       f"ID: {data['id']}\n" \
                       f"Altura: {altura_cm} cm\n" \
                       f"Peso: {peso_kg} kg\n" \
                       "Tipos: " + ", ".join([t['type']['name'] for t in data['types']])
        result_label.config(text=pokemon_info)  # Muestra la información en un widget llamado "result_label".
    else:
        result_label.config(text="Información del Pokémon no disponible")  # Muestra un mensaje si la información no está disponible.

# Creación de la ventana del juego.
app = tk.Tk()  # Crea una ventana principal de la GUI.
app.title("Adivina el Pokémon")  # Establece el título de la ventana.

background_image = Image.open('pokedex.jpg')  # Abre una imagen de fondo.
background_photo = ImageTk.PhotoImage(background_image)  # Convierte la imagen en un objeto compatible con tkinter.

background_label = tk.Label(app, image=background_photo)  # Crea una etiqueta para mostrar la imagen de fondo.
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ajusta la posición y el tamaño de la etiqueta en la ventana.

label = tk.Label(app, text="¿Quién es ese Pokémon?:")  # Crea una etiqueta con un texto.
label.pack()  # Coloca la etiqueta en la ventana.

entry = tk.Entry(app)  # Crea un campo de entrada de texto.
entry.pack()  # Coloca el campo de entrada en la ventana.

check_button = tk.Button(app, text="Comprobar", command=pokecomprobar)  # Crea un botón para comprobar la conjetura.
check_button.pack()  # Coloca el botón en la ventana.

pokerandom_button = tk.Button(app, text="Siguiente Pokémon", command=pokerandom)  # Crea un botón para pasar al siguiente Pokémon.
pokerandom_button.pack()  # Coloca el botón en la ventana.

image_label = tk.Label(app)  # Crea una etiqueta para mostrar la imagen del Pokémon.
image_label.pack()  # Coloca la etiqueta en la ventana.

result_label = tk.Label(app, text="")  # Crea una etiqueta para mostrar información del Pokémon.
result_label.pack()  # Coloca la etiqueta en la ventana.

app.geometry("400x400")  # Establece el tamaño de la ventana.

puntuacion_label = tk.Label(app, text=f"Puntuación: {puntuacion}")  # Crea una etiqueta para mostrar la puntuación actual.
puntuacion_label.pack()  # Coloca la etiqueta en la ventana.

vidas_label = tk.Label(app, text=f"Vidas: {vidas}")  # Crea una etiqueta para mostrar la cantidad de vidas.
vidas_label.pack()  # Coloca la etiqueta en la ventana.

mayor_puntaje_label = tk.Label(app, text=f"Puntuación más alta: {mayor_puntaje}")  # Crea una etiqueta para mostrar el puntaje más alto.
mayor_puntaje_label.pack()  # Coloca la etiqueta en la ventana.

app.mainloop()  # Inicia la aplicación y muestra la ventana principal.
