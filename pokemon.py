import tkinter as tk
from json import tk
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/pokemon/<name_or_id>', methods=['GET'])
def get_pokemon_info(name_or_id):

    url = f'https://pokeapi.co/api/v2/pokemon/{name_or_id}/'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        pokemon_info = {
            'name': data['name'],
            'id': data['id'],
            'height': data['height'],
            'weight': data['weight'],
            'types': [t['type']['name'] for t in data['types']],
        }
        return jsonify(pokemon_info)
    else:
        return jsonify({'error': 'Pokemon no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)



