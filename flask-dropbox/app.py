from flask import Flask, request, redirect, url_for
import json
import os
from dropbox_operations import *

app = Flask(__name__)

TOKEN_FILE = 'tokens.json'

@app.route('/')
def home():
    tokens = load_tokens(TOKEN_FILE)
    if tokens and not tokens_expired(tokens):
        return 'Tokens are valid. No need to re-authorize.'
    return redirect(url_for('authorize'))

@app.route('/authorize')
def authorize():
    auth_url = (
        f"https://www.dropbox.com/oauth2/authorize"
        f"?client_id={APP_KEY}"
        f"&response_type=code"
        f"&token_access_type=offline"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route('/oauth2/callback')
def oauth2_callback():
    code = request.args.get('code')

    token_info = exchange_code_for_token(code)
    
    if 'access_token' in token_info:
        save_tokens(token_info['access_token'], token_info['refresh_token'], token_info['expires_in'], TOKEN_FILE)
        return 'Authorization successful and tokens saved.'
    else:
        return f"Error: {token_info.get('error_description', 'Unknown error')}"

@app.route('/account')
def account():
    account_info = get_current_account(TOKEN_FILE)
    return json.dumps(account_info, indent=4)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request.'

    file = request.files['file']
    file_path = os.path.join(app.root_path, 'uploads', file.filename)
    file.save(file_path)

    upload_result = upload_file(file_path, file.filename, TOKEN_FILE)
    os.remove(file_path)

    return json.dumps(upload_result, indent=4)

@app.route('/delete/<filename>')
def delete(filename):
    delete_result = delete_file(filename, TOKEN_FILE)
    return json.dumps(delete_result, indent=4)

@app.route('/exists/<filename>')
def exists(filename):
    file_exists = check_file_exists(filename, TOKEN_FILE)
    return str(file_exists)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
