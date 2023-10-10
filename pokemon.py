import requests
import tkinter as tk
from tkinter import messagebox
import io
from PIL import Image, ImageTk
import random

mayor_puntaje = 0
racha_actual = 0
vidas = 3
pokemon_actual = None
puntuacion = 0

def pokelista():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1000'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokenombres = [pokemon['name'] for pokemon in data['results']]
        return pokenombres
    else:
        messagebox.showerror("Error", "No se pudo obtener la lista de Pokémon")
        return []

pokemon_actual = None

def pokerandom():
    global pokemon_actual, racha_actual
    racha_actual = 0
    result_label.config(text="")

    pokemon_actual = random.choice(pokelista)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_actual}/'

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

def reiniciar_juego():
    global puntuacion, vidas, pokemon_actual
    puntuacion = 0
    vidas = 3
    pokerandom()
    puntuacion_label.config(text=f"Puntuación: {puntuacion}")
    vidas_label.config(text=f"Vidas: {vidas}")
    result_label.config(text="")
    entry.delete(0, tk.END)

def pokecomprobar():
    global puntuacion, vidas, mayor_puntaje, racha_actual, pokemon_actual
    if pokemon_actual is not None:
        guess = entry.get().lower()
        if guess == pokemon_actual:
            puntuacion += 1
            racha_actual += 1
            if puntuacion > mayor_puntaje:
                mayor_puntaje = puntuacion
            pokeinfo(pokemon_actual)
            puntuacion_label.config(text=f"Puntuación: {puntuacion}")
            if racha_actual == 5:
                messagebox.showinfo("Logro desbloqueado", "¡Has alcanzado una racha de 5 Pokémon adivinados!")
        else:
            vidas -= 1
            racha_actual = 0
            if vidas >= 0:
                if vidas == 0:
                    # Mostrar el nombre del Pokémon en la ventana de mensaje cuando se pierde la última vida
                    messagebox.showinfo("Juego terminado", f"Perdiste todas tus vidas. El Pokémon era: {pokemon_actual}. Tu puntuación final es: {puntuacion}")
                    # Reiniciar el juego
                    reiniciar_juego()
                else:
                    # Mostrar el nombre del Pokémon en la ventana de mensaje cuando se pierde una vida
                    messagebox.showerror("Incorrecto", f"Inténtalo de nuevo. Te quedan {vidas} vidas. El Pokémon era: {pokemon_actual}")
                # Cambiar el Pokémon actual solo si quedan vidas
                if vidas >= 0:
                    pokerandom()
    vidas_label.config(text=f"Vidas: {vidas}")
    mayor_puntaje_label.config(text=f"Puntuación más alta: {mayor_puntaje}")

def pokeinfo(pokemon_name):
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

pokelista = pokelista()

app = tk.Tk()
app.title("Adivina el Pokémon")

background_image = Image.open('pokedex.jpg')
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label = tk.Label(app, text="¿Quién es ese Pokémon?:")
label.pack()

entry = tk.Entry(app)
entry.pack()

check_button = tk.Button(app, text="Comprobar", command=pokecomprobar)
check_button.pack()

pokerandom_button = tk.Button(app, text="Siguiente Pokémon", command=pokerandom)
pokerandom_button.pack()

image_label = tk.Label(app)
image_label.pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.geometry("400x400")
puntuacion_label = tk.Label(app, text=f"Puntuación: {puntuacion}")
puntuacion_label.pack()
vidas_label = tk.Label(app, text=f"Vidas: {vidas}")
vidas_label.pack()

mayor_puntaje_label = tk.Label(app, text=f"Puntuación más alta: {mayor_puntaje}")
mayor_puntaje_label.pack()
app.mainloop()