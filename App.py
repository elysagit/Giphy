import os
from flask import Flask, render_template, request, redirect
import requests
from dotenv import load_dotenv

load_dotenv()
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        termo = request.form.get('query')
        return redirect(f"/search?query={termo}")
    # GET: buscar GIFs recomendados (trending)
    url = 'https://api.giphy.com/v1/gifs/trending'
    params = {
        'api_key': GIPHY_API_KEY,
        'limit': 10,
        'rating': 'g'
    }
    resp = requests.get(url, params=params)
    data = resp.json().get('data', [])
    gifs = [gif['images']['downsized_medium']['url'] for gif in data]
    return render_template('index.html', gifs=gifs)

@app.route('/search')
def search():
    termo = request.args.get('query')
    url = 'https://api.giphy.com/v1/gifs/search'
    params = {
        'api_key': GIPHY_API_KEY,
        'q': termo,
        'limit': 10,
        'rating': 'g'
    }
    resp = requests.get(url,params=params)
    data = resp.json().get('data', [])
    gifs = [gif['images']['downsized_medium']['url'] for gif in data]
    return render_template('results.html', gifs=gifs, termo=termo)

if __name__ == '__main__':
    app.run(debug=True)
