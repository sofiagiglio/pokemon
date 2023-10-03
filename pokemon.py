import requests
import tkinter as tk
from tkinter import messagebox
import io
from PIL import Image, ImageTk
import random

# Variables para realizar un seguimiento de los récords y logros
highest_score = 0  # Puntuación más alta
current_streak = 0  # Racha actual de Pokémon adivinados
lives = 3  # Número inicial de vidas
current_pokemon = None
score = 0  # Variable para realizar un seguimiento de la puntuación del jugador

def get_pokemon_list():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1000'  # Obtén una lista de 1000 Pokémon

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        return pokemon_names
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de Pokémon")
        return []

# Variable para realizar un seguimiento del Pokémon actual
current_pokemon = None

def get_random_pokemon():
    global current_pokemon, current_streak  # Agregar una referencia a la variable global current_streak
    # Reiniciar la racha al obtener un nuevo Pokémon aleatorio
    current_streak = 0
    result_label.config(text="")

    # Obtener un Pokémon aleatorio de la lista
    current_pokemon = random.choice(pokemon_list)
    url = f'https://pokeapi.co/api/v2/pokemon/{current_pokemon}/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Obtener la URL de la imagen del Pokémon
        image_url = data['sprites']['front_default']

        # Descargar la imagen y mostrarla en el Label de la imagen
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img = ImageTk.PhotoImage(img, width=100, height=70)
        image_label.config(image=img, compound=tk.CENTER)
        image_label.image = img

def check_guess():
    global score, lives, highest_score, current_streak  # Agregar referencias a las variables globales
    if current_pokemon is not None:
        guess = entry.get().lower()
        if guess == current_pokemon:
            # Incrementar la puntuación cuando el jugador adivina correctamente
            score += 1
            # Incrementar la racha de Pokémon adivinados
            current_streak += 1
            # Actualizar la puntuación más alta si es necesario
            if score > highest_score:
                highest_score = score
            # Mostrar la información del Pokémon en el Label de resultado
            display_pokemon_info(current_pokemon)
            # Actualizar la etiqueta de la puntuación
            score_label.config(text=f"Puntuación: {score}")
            # Verificar si se ha alcanzado un logro (por ejemplo, una racha de 5 Pokémon adivinados)
            if current_streak == 5:
                messagebox.showinfo("Logro desbloqueado", "¡Has alcanzado una racha de 5 Pokémon adivinados!")
        else:
            # Restar una vida en caso de adivinanza incorrecta
            lives -= 1
            current_streak = 0  # Reiniciar la racha en caso de adivinanza incorrecta
            if lives > 0:
                messagebox.showerror("Incorrecto", f"Inténtalo de nuevo. Te quedan {lives} vidas.")
            else:
                messagebox.showinfo("Juego terminado", f"Perdiste todas tus vidas. Tu puntuación final es: {score}")
                app.quit()  # Cerrar la aplicación cuando se quedan sin vidas
    lives_label.config(text=f"Vidas: {lives}")
    # Actualizar la etiqueta de la puntuación más alta
    highest_score_label.config(text=f"Puntuación más alta: {highest_score}")


def display_pokemon_info(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Convertir la altura de decímetros a centímetros
        altura_cm = data['height'] * 10
        
        # Convertir el peso de hectogramos a kilogramos
        peso_kg = data['weight'] / 10
        
        pokemon_info = f"Nombre: {data['name'].capitalize()}\n" \
                       f"ID: {data['id']}\n" \
                       f"Altura: {altura_cm} cm\n" \
                       f"Peso: {peso_kg} kg\n" \
                       "Tipos: " + ", ".join([t['type']['name'] for t in data['types']])
        result_label.config(text=pokemon_info)
    else:
        result_label.config(text="Información del Pokémon no disponible")
# Obtener la lista de nombres de Pokémon desde la API
pokemon_list = get_pokemon_list()

# Crear la ventana de la aplicación
app = tk.Tk()
app.title("Adivina el Pokémon")

# Cargar la imagen de fondo
background_image = Image.open('pokedex.jpg')  # Reemplaza 'tu_imagen_de_fondo.png' con la ruta de tu imagen de fondo
background_photo = ImageTk.PhotoImage(background_image)

# Crear un Label para la imagen de fondo
background_label = tk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear elementos de la interfaz gráfica
label = tk.Label(app, text="¿Quién es ese Pokémon?:")
label.pack()

entry = tk.Entry(app)
entry.pack()

check_button = tk.Button(app, text="Comprobar", command=check_guess)
check_button.pack()

get_random_pokemon_button = tk.Button(app, text="Siguiente Pokémon", command=get_random_pokemon)
get_random_pokemon_button.pack()

# Crear un Label para la imagen del Pokémon
image_label = tk.Label(app)
image_label.pack()

# Crear un Label para mostrar la información del Pokémon adivinado
result_label = tk.Label(app, text="")
result_label.pack()

app.geometry("400x400")  # Tamaño inicial de la ventana
# Crear una etiqueta para mostrar la puntuación
score_label = tk.Label(app, text=f"Puntuación: {score}")
score_label.pack()
# Crear una etiqueta para mostrar las vidas restantes
lives_label = tk.Label(app, text=f"Vidas: {lives}")
lives_label.pack()
# Crear una etiqueta para mostrar la puntuación más alta
highest_score_label = tk.Label(app, text=f"Puntuación más alta: {highest_score}")
highest_score_label.pack()
app.mainloop()