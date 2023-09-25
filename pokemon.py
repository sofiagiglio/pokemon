import requests
import tkinter as tk
from tkinter import messagebox
import io
from PIL import Image, ImageTk

def get_pokemon_info():
    pokemon_name = entry.get().lower()
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        pokemon_info = f"Nombre: {data['name'].capitalize()}\n" \
                       f"ID: {data['id']}\n" \
                       f"Altura: {data['height']}\n" \
                       f"Peso: {data['weight']}\n" \
                       "Tipos: " + ", ".join([t['type']['name'] for t in data['types']])
        result_label.config(text=pokemon_info)

        # Obtener la URL de la imagen del Pokémon
        image_url = data['sprites']['front_default']

        # Descargar la imagen y mostrarla en el Label de la imagen
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(io.BytesIO(img_data))
        img.thumbnail((300, 300))  # Ajusta el tamaño de la imagen
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img
    else:
        result_label.config(text="Pokemon no encontrado")
        messagebox.showerror("Error", "Pokemon no encontrado")

# Crear la ventana de la aplicación
app = tk.Tk()
app.title("¿Quién es ese Pokémon?")

# Crear elementos de la interfaz gráfica
label = tk.Label(app, text="Ingresa el nombre o ID del Pokémon:")
label.pack()

entry = tk.Entry(app)
entry.pack()

search_button = tk.Button(app, text="Buscar", command=get_pokemon_info)
search_button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

# Crear un Label para la imagen del Pokémon
image_label = tk.Label(app)
image_label.pack()

app.geometry("")
app.mainloop()
