from flask import Flask, jsonify, request, redirect


import random
import string

from datetime import datetime

from app.utils import generate_short_code, is_valid_url 

app = Flask(__name__)

# In-memory storage for URL mappings
url_mapping = {}

# this generates a random short code and stores it in the url_mapping dictionary
# the length of the short code is 6 characters
# the short code is a combination of letters and digits
# the short code is unique and can be used to redirect to the long url
# the short code is stored in the url_mapping dictionary
# the long url is stored in the url_mapping dictionary
# the short code is returned to the user
# the long url is returned to the user

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })


# posting the url and getting the short code


@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')

    
    if not long_url or not is_valid_url(long_url):
        return jsonify({
            "error": "Missing or invalid 'url' in request body"
        }), 400

    # Generate a unique short code
    short_code = generate_short_code()
    while short_code in url_mapping:
        short_code = generate_short_code()

    # mapping
    url_mapping[short_code] = {
        "long_url": long_url,
        "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        "clicks": 0
    }

    return jsonify({
        "short_code": short_code,
        "short_url": f"http://127.0.0.1:5000/{short_code}"
    }), 201


# redirections 


@app.route('/<short_code>' , methods = ['GET'])
def redirect_original(short_code):
    data = url_mapping.get(short_code)


    if not data:
        return jsonify({"error" : "Short code not Found ! "}) , 404

    
    data['clicks'] += 1 

    return redirect(data['long_url'])


# Statistical 
@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    data = url_mapping.get(short_code)

    if not data:
        return jsonify({"error": "Short code not found"}), 404

    return jsonify({
        "url": data["long_url"],
        "created_at": data["created_at"],
        "clicks": data["clicks"]
    }), 200




@app.route('/api/mappings', methods=['GET'])
def get_mappings():
    return jsonify(url_mapping)


# list of the 

# method 1: using requests library

# reponse = requests.post(
#     "http://127.0.0.1:5000/api/shorten",
#     json={"url": "https://www.google.com"}
# )

# # print(reponse.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



