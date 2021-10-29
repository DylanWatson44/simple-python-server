import json
import requests

from flask import Flask, request, abort, jsonify
from flask_socketio import SocketIO, send, emit

print("Starting server1")
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*',
                    logger=True, engineio_logger=True, async_mode="threading")

# todo get from env
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADuJVAEAAAAA%2FBVcOBmnzqmrMpuZfa6NiF3GMoM%3Duh6ufL1I9E46gKu9soqbFQXfJQEIwREONF9ZjZMWwDyOSL3EmO"


# def serveTweets():


@socketio.on('connect')
def connected(auth):

    print("Getting stream")
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    with requests.get(
        'https://api.twitter.com/2/tweets/search/stream?tweet.fields=context_annotations&expansions=author_id', headers=headers, stream=True) as response:

        print("possible response received")
        if response.encoding is None:
            response.encoding = 'utf-8'

        # for i in range(3):
        #     socketio.emit('tweet', {'data': {'author_id': '1206873813088178178', 'context_annotations': [{'domain': {'id': '10', 'name': 'Person', 'description': 'Named people in the world like Nelson Mandela'}, 'entity': {'id': '1270337060797202433', 'name': 'Shehnaaz Kaur Gill'}}, {'domain': {'id': '54', 'name': 'Musician', 'description': 'A musician in the world, like Adele or Bob Dylan'}, 'entity': {'id': '1270337060797202433', 'name': 'Shehnaaz Kaur Gill'}}], 'id': '1454028042079064064', 'text': 'RT @asjadnazir: What beautiful song Tu Yaheen Hai is and so wonderfully sung by @ishehnaaz_gill - you can really feel the emotion. 😭😭😭😭\n#Tu…'}, 'includes': {'users': [{'id': '1206873813088178178', 'name': 'Uma Nagar', 'username': 'UmaNagar3'}, {'id': '177983944', 'name': 'Asjad Nazir', 'username': 'asjadnazir'}, {'id': '1189446547622125571', 'name': 'Shehnaaz Gill', 'username': 'ishehnaaz_gill'}]}, 'matching_rules': [{'id': '1454026382070239237','tag': ''}]})

        for line in response.iter_lines():
            print("for line", line)
            # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                print("decoded_line", decoded_line)
                data = json.loads(decoded_line)
                print('got some data, ')

                socketio.emit('tweet', data)

                # break
        

    #serveTweets()

    # socketio.emit('tweet', {'data': {'author_id': '1206873813088178178', 'context_annotations': [{'domain': {'id': '10', 'name': 'Person', 'description': 'Named people in the world like Nelson Mandela'}, 'entity': {'id': '1270337060797202433', 'name': 'Shehnaaz Kaur Gill'}}, {'domain': {'id': '54', 'name': 'Musician', 'description': 'A musician in the world, like Adele or Bob Dylan'}, 'entity': {'id': '1270337060797202433', 'name': 'Shehnaaz Kaur Gill'}}], 'id': '1454028042079064064', 'text': 'RT @asjadnazir: What beautiful song Tu Yaheen Hai is and so wonderfully sung by @ishehnaaz_gill - you can really feel the emotion. 😭😭😭😭\n#Tu…'}, 'includes': {'users': [{'id': '1206873813088178178', 'name': 'Uma Nagar', 'username': 'UmaNagar3'}, {'id': '177983944', 'name': 'Asjad Nazir', 'username': 'asjadnazir'}, {'id': '1189446547622125571', 'name': 'Shehnaaz Gill', 'username': 'ishehnaaz_gill'}]}, 'matching_rules': [{'id': '1454026382070239237','tag': ''}]})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          


@ socketio.on('disconnect')
def disconnect():
    print('Client disconnected')


@ socketio.on('*')
def catch_all():
    print("I landed in the catch-all")


@ app.route('/api/rules', methods = ['POST'])
def add_rule():
    if not request.json:
        abort(400)
    headers={"Authorization": f"Bearer {BEARER_TOKEN}",
               "Content-Type": "application/json"}
    print("posted data", type(request.json), request.json)
    response=requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers = headers, data = json.dumps(request.json))
    print('post response', response, response.json())
    return {"body": response.json()}


@ app.route('/api/rules', methods = ['get'])
def get_rules():
    headers={"Authorization": f"Bearer {BEARER_TOKEN}"}
    response=requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers = headers, data = request.json)
    print('get response', response, response.json())
    return {"body": response.json()}


if __name__ == '__main__':
    # serveTweets()
    socketio.run(app, port = 3001)
    # eventlet.wsgi.server(eventlet.listen(('', 3001)), app)
