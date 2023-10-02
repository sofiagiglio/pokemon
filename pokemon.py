import requests
import tkinter as tk
from tkinter import messagebox
import io
from PIL import Image, ImageTk
import random

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
    global current_pokemon
    # Borra la información del Pokémon anterior
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
    if current_pokemon is not None:
        guess = entry.get().lower()
        if guess == current_pokemon:
            # Mostrar la información del Pokémon en el Label de resultado
            display_pokemon_info(current_pokemon)
        else:
            messagebox.showerror("Incorrecto", f"Inténtalo de nuevo. El Pokémon no es {guess.capitalize()}.")

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
app.mainloop()

