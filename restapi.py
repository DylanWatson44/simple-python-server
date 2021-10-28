
#todo get from env
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADuJVAEAAAAATYInirTCiVqAwq%2FBLiQ01qhhqP4%3Drq1TdI2zfj8jyRY7BdAyQILyOJgYTtc5BBVnYScXe6LmOmWKle"

@app.route('/api/rules', methods=['POST'])
def add_rule():
    if not request.json:
        abort(400)
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAADuJVAEAAAAATYInirTCiVqAwq%2FBLiQ01qhhqP4%3Drq1TdI2zfj8jyRY7BdAyQILyOJgYTtc5BBVnYScXe6LmOmWKle"}
    response = requests.post("https://api.twitter.com/2/tweets/search/stream/rules", headers=headers, data=request.json)
    return response

@app.route('/api/rules', methods=['get'])
def get_rules():
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAADuJVAEAAAAATYInirTCiVqAwq%2FBLiQ01qhhqP4%3Drq1TdI2zfj8jyRY7BdAyQILyOJgYTtc5BBVnYScXe6LmOmWKle"}
    response = requests.get("https://api.twitter.com/2/tweets/search/stream/rules", headers=headers, data=request.json)
    return response

if __name__ == '__main__':
    app.run(host='', port=3001, debug=True)