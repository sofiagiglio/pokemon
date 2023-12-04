import requests
import tkinter as tk
from tkinter import messagebox
import io
from PIL import Image, ImageTk
import random

highest_score = 0  
current_streak = 0  
lives = 3  
current_pokemon = None
score = 0  

def get_pokemon_list():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1000'  

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_names = [pokemon['name'] for pokemon in data['results']]
        return pokemon_names
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de Pokémon")
        return []

current_pokemon = None

def get_random_pokemon():
    global current_pokemon, current_streak  
    current_streak = 0
    result_label.config(text="")

    
    current_pokemon = random.choice(pokemon_list)
    url = f'https://pokeapi.co/api/v2/pokemon/{current_pokemon}/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        image_url = data['sprites']['front_default']

        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img = ImageTk.PhotoImage(img, width=100, height=70)
        image_label.config(image=img, compound=tk.CENTER)
        image_label.image = img

def restart_game():
    global score, lives, current_pokemon
    score = 0
    lives = 3
    get_random_pokemon()
    score_label.config(text=f"Puntuación: {score}")
    lives_label.config(text=f"Vidas: {lives}")
    result_label.config(text="")
    entry.delete(0, tk.END)

def check_guess():
    global score, lives, highest_score, current_streak  
    if current_pokemon is not None:
        guess = entry.get().lower()
        if guess == current_pokemon:
            score += 1
            current_streak += 1
            if score > highest_score:
                highest_score = score
            display_pokemon_info(current_pokemon)
            score_label.config(text=f"Puntuación: {score}")
            if current_streak == 5:
                messagebox.showinfo("Logro desbloqueado", "¡Has alcanzado una racha de 5 Pokémon adivinados!")
        else:
            lives -= 1
            current_streak = 0  
            if lives > 0:
                messagebox.showerror("Incorrecto", f"Inténtalo de nuevo. Te quedan {lives} vidas.")
            else:
                messagebox.showinfo("Juego terminado", f"Perdiste todas tus vidas. Tu puntuación final es: {score}")
                restart_game()
    lives_label.config(text=f"Vidas: {lives}")
    highest_score_label.config(text=f"Puntuación más alta: {highest_score}")

def display_pokemon_info(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        
        altura_cm = data['height'] * 10
        
        peso_kg = data['weight'] / 10
        
        pokemon_info = f"Nombre: {data['name'].capitalize()}\n" \
                       f"ID: {data['id']}\n" \
                       f"Altura: {altura_cm} cm\n" \
                       f"Peso: {peso_kg} kg\n" \
                       "Tipos: " + ", ".join([t['type']['name'] for t in data['types']])
        result_label.config(text=pokemon_info)
    else:
        result_label.config(text="Información del Pokémon no disponible")

pokemon_list = get_pokemon_list()

app = tk.Tk()
app.title("Adivina el Pokémon")# Crear una etiqueta para mostrar la puntuación más alta


background_image = Image.open('pokedex.jpg')  
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label = tk.Label(app, text="¿Quién es ese Pokémon?:")
label.pack()

entry = tk.Entry(app)
entry.pack()

check_button = tk.Button(app, text="Comprobar", command=check_guess)
check_button.pack()
# Crear una etiqueta para mostrar la puntuación más alta

get_random_pokemon_button = tk.Button(app, text="Siguiente Pokémon", command=get_random_pokemon)
get_random_pokemon_button.pack()

image_label = tk.Label(app)
image_label.pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.geometry("400x400")  
score_label = tk.Label(app, text=f"Puntuación: {score}")
score_label.pack()
lives_label = tk.Label(app, text=f"Vidas: {lives}")
lives_label.pack()
highest_score_label = tk.Label(app, text=f"Puntuación más alta: {highest_score}")
highest_score_label.pack()
app.mainloop()