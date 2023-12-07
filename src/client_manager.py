from flask import Flask, request
from DAO import DAO
from models import ClientModel
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    dao = DAO()
    client_ip = request.remote_addr

    client = dao.find_client(client_ip)
    if not client:
        print('did not find, doing a search')
        new_client = ClientModel(client_ip, datetime.now(), 0)
        dao.add_client(new_client)
        client = dao.find_client(client_ip)

    return f'Client IP: {client.first_request} \nResult: {client.first_request}'

def client_manager_server():
    app.run(debug=True, host="0.0.0.0", port=5001)
