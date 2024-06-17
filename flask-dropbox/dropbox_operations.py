import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

APP_KEY = os.getenv('APP_KEY')
APP_SECRET = os.getenv('APP_SECRET')
#this is the redirect url - http://localhost:5000/oauth2/callback ( configured in dropbox UI App)
REDIRECT_URI = os.getenv('REDIRECT_URI')

def save_tokens(access_token, refresh_token, expires_in, token_file):
    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_at': (datetime.now() + timedelta(seconds=expires_in)).isoformat()
    }
    with open(token_file, 'w') as f:
        json.dump(tokens, f)

def load_tokens(token_file):
    try:
        with open(token_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def tokens_expired(tokens):
    expires_at = datetime.fromisoformat(tokens['expires_at'])
    return datetime.now() >= expires_at

def refresh_access_token(refresh_token):
    token_url = 'https://api.dropbox.com/oauth2/token'
    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()

    if 'access_token' in token_info:
        return token_info
    else:
        return None

def exchange_code_for_token(code):
    token_url = 'https://api.dropbox.com/oauth2/token'
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': APP_KEY,
        'client_secret': APP_SECRET,
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(token_url, data=data)
    return response.json()

def get_current_account(token_file):
    tokens = load_tokens(token_file)
    if not tokens or tokens_expired(tokens):
        return 'Tokens are expired or not available.'

    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}'
    }
    response = requests.post('https://api.dropboxapi.com/2/users/get_current_account', headers=headers)
    return response.json()

def upload_file(file_path, file_name, token_file):
    tokens = load_tokens(token_file)
    if not tokens or tokens_expired(tokens):
        return 'Tokens are expired or not available.'

    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/octet-stream',
        'Dropbox-API-Arg': json.dumps({
            'path': f'/{file_name}',
            'mode': 'add',
            'autorename': True,
            'mute': False
        })
    }

    with open(file_path, 'rb') as f:
        content = f.read()
        response = requests.post('https://content.dropboxapi.com/2/files/upload', headers=headers, data=content)

    return response.json()

def delete_file(file_name, token_file):
    tokens = load_tokens(token_file)
    if not tokens or tokens_expired(tokens):
        return 'Tokens are expired or not available.'

    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/json'
    }

    data = {
        'path': f'/{file_name}'
    }

    response = requests.post('https://api.dropboxapi.com/2/files/delete_v2', headers=headers, json=data)
    return response.json()

def check_file_exists(file_name, token_file):
    tokens = load_tokens(token_file)
    if not tokens or tokens_expired(tokens):
        return 'Tokens are expired or not available.'

    headers = {
        'Authorization': f'Bearer {tokens["access_token"]}',
        'Content-Type': 'application/json'
    }

    data = {
        'path': f'/{file_name}'
    }

    response = requests.post('https://api.dropboxapi.com/2/files/get_metadata', headers=headers, json=data)

    if response.status_code == 200:
        return True
    elif response.status_code == 409:
        return False
    else:
        return f'Error checking file existence: {response.json()}'
