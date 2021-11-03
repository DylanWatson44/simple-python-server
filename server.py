# import eventlet
# eventlet.monkey_patch()
import json
import requests
import traceback
from threading import Thread, Event
from flask import Flask, request, abort, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit

print("Starting server")
app = Flask(__name__)
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*',
                    logger=True, engineio_logger=True, async_mode="threading", always_connect=True)

# todo get from env
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAADuJVAEAAAAA1l87uzCkygNEtgdWFus0SnmUJfs%3D4hvD9Jy4sHRNgU6pxvfYnqj5iE9WkXEUMswxbQIMRu6hugNe8Q"

thread = Thread()
thread_stop_event = Event()

tweetDict = {}
sidList = []


def serveTweets():
    print("Getting stream")
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    with requests.get(
            'https://api.twitter.com/2/tweets/search/stream?tweet.fields=context_annotations,text&expansions=author_id&user.fields=profile_image_url', headers=headers, stream=True) as response:

        print("stream response received")
        if response.encoding is None:
            response.encoding = 'utf-8'

        for line in response.iter_lines():
            if(thread_stop_event.isSet()):
                break

            # filter out keep-alive new lines
            if line:
                try:
                    decoded_line = line.decode('utf-8')
                    data = json.loads(decoded_line)
                    if "errors" in data:
                        socketio.emit('error', data)
                    else:
                        tweetId = data["data"]["id"]
                        if(tweetId not in tweetDict):
                            tweetDict[tweetId] = True
                            tweetText = data["data"]["text"]
                            if tweetText.startswith('RT'):
                                continue

                            socketio.emit('tweet', data)
                except Exception as err:
                    print("An exception occurred", err)
                    traceback.print_exc()


@socketio.on('connect')
def connected(auth):
    socketio.emit('connected with sid', request.sid)
    sidList.append(request.sid)
    global thread
    print('Client connected')
    thread_stop_event.clear()
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(serveTweets)


@socketio.on('disconnect')
def disconnect():
    sidList.remove(request.sid)
    if(len(sidList) <= 0):
        thread_stop_event.set()
        delete_rule("red-team")
        delete_rule("blue-team")
    print('Client disconnected')


@app.route('/api/rules', methods=['POST'])
@cross_origin()
def add_rule():
    if not request.json:
        error_message = json.dumps({"error": "Missing body"})
        print("Returning error to client", error_message)
        abort(Response(error_message, 401))

    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "Content-Type": "application/json"}

    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers, data=json.dumps(request.json))
    return {"body": response.json()}


@app.route('/api/rules/<team>', methods=['DELETE'])
@cross_origin()
def delete_rule(team):
    print("delete started for team", team)
    if not team:
        error_message = json.dumps({"error": "Missing team in path"})
        print("Returning error to client", error_message)
        abort(Response(error_message, 401))

    rules = get_rules()
    print('rules acquired', rules)

    rulesTodelete = [x["id"]
                     for x in rules["body"]["data"] if x["tag"] == team]

    payload = {"delete": {"ids": rulesTodelete}}

    print("payload", payload)

    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "Content-Type": "application/json"}

    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers, data=json.dumps(payload))
    print('post response', response, response.json())
    return {"body": response.json()}


@app.route('/api/rules', methods=['get'])
def get_rules():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers)
    return {"body": response.json()}


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3001)
