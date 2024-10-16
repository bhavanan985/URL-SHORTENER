from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

# A dictionary to hold the URL mappings
url_map = {}
counter = 1  # Simple counter for generating unique short URLs

def generate_short_url():
    global counter
    # Generate a unique short URL based on the counter
    short_url = base62_encode(counter)
    counter += 1
    return short_url

def base62_encode(num):
    """Convert a number to a base62 string."""
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(characters)
    short_url = []
    
    while num > 0:
        num, rem = divmod(num, base)
        short_url.append(characters[rem])
    
    return ''.join(reversed(short_url))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_url = generate_short_url()
    
    # Store the mapping
    url_map[short_url] = original_url
    
    return jsonify(short_url=short_url)

@app.route('/<short_url>')
def redirect_url(short_url):
    original_url = url_map.get(short_url)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
