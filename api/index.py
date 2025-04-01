from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
import string
from datetime import datetime, timedelta
import os
import requests

app = Flask(__name__)
CORS(app)

# Caminho do arquivo JSON para armazenar as chaves
KEYS_FILE = 'keys.json'

# Token do bot e chat_id do Telegram
BOT_TOKEN = '7950073092:AAGIF-CiHHFG79wiCpsw-xnQRXiPllrKCTs'
CHAT_ID = '5650303115'

# Função para gerar chaves aleatórias
def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Função para carregar as chaves do arquivo JSON
def load_keys():
    try:
        with open(KEYS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Função para salvar as chaves no arquivo JSON
def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

@app.route('/')
def home():
    return jsonify({"message": "API funcionando na Vercel!"})

@app.route('/generate_key', methods=['POST'])
def generate_key_api():
    data = request.json
    validity_days = int(data.get('validity_days', 1))  # Padrão: 1 dia
    expiration_date = datetime.now() + timedelta(days=validity_days)
    expiration_str = expiration_date.strftime('%d/%m/%Y')

    new_key = generate_key()
    keys = load_keys()

    keys.append({
        'key': new_key,
        'created_at': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'expires_at': expiration_str
    })

    save_keys(keys)
    return jsonify({"message": "Key generated successfully", "key": new_key, "expires_at": expiration_str})

@app.route('/get_keys', methods=['GET'])
def get_keys():
    return jsonify(load_keys())

# Adaptador para Vercel
def handler(event, context):
    return app
