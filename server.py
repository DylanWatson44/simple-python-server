import json
import requests
import socketio
import eventlet


# from flask import Flask, request, abort, jsonify
# import requests

# app = Flask(__name__)


print("Starting server1")
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
print("Starting server2")
def serveTweets():
    print("Getting stream")
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAADuJVAEAAAAATYInirTCiVqAwq%2FBLiQ01qhhqP4%3Drq1TdI2zfj8jyRY7BdAyQILyOJgYTtc5BBVnYScXe6LmOmWKle"}
    response = requests.get('https://api.twitter.com/2/tweets/search/stream?tweet.fields=context_annotations&expansions=author_id', headers=headers, stream=True)
    while True:
        print("possible response recieved")
        if response.encoding is None:
            response.encoding = 'utf-8'

        for line in response.iter_lines():

            # filter out keep-alive new lines
            if line:
                decoded_line = line.decode('utf-8')
                data = json.loads(decoded_line)
                print('got some data, ', data)

                sio.emit('tweet', data)


@sio.event
def connect(sid, environ, auth):
    print('connected ', sid)
    serveTweets()

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('*')
def catch_all(event, sid, data):
    print("I landed in the catch-all")

if __name__ == '__main__':
    print("Starting server3")
    # socketio.run(app,host='',port=3001)
    eventlet.wsgi.server(eventlet.listen(('', 3001)), app)
