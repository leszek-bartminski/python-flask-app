import random
import os
from flask import Flask, jsonify
from time import sleep
import json
import requests
import urllib
import google.auth.transport.requests
import google.oauth2.id_token

app = Flask(__name__)

def generate_task():
    url = 'https://us-central1-leszek-bartminski.cloudfunctions.net/function-2'
    req = urllib.request.Request(url)
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req,url)
    req.add_header("Authorization", f"Bearer {id_token}")
    response = urllib.request.urlopen(req)
    decoded_reponse = response.read().decode('utf-8')

    data = json.loads(decoded_reponse)
    number = data['number']

    if(os.getenv('ENV_TYPE') == 'test'):
        sleep_time = random.randint(0,2)
        tasks = [
            {
                'number': number,
                'title': u'TEST DISPLAY',
                'sleep_time': sleep_time,
                'pod_name' : os.getenv('MY_POD_NAME'),
                'node_name' : os.getenv('MY_NODE_NAME'),
                'env_type' : os.getenv('ENV_TYPE'),
                'login' : os.getenv('username'),
                'password': os.getenv('password')
            },
        ]
        return tasks
    else:
        sleep_time = random.randint(0,2)
        tasks = [
            {
                'calculation_result': random.randint(0, 100000),
                'title': u'TEST DISPLAY',
                'sleep_time': sleep_time
            },
        ]
        return tasks
	



@app.route('/get-item', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': generate_task()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
    