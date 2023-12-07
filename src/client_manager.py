from flask import Flask, request
from datetime import datetime
from DAO import DAO
from models import ClientModel
from proxy_assigners import random_proxy_assigner


app = Flask(__name__)

def find_or_create_client(dao, client_ip):
    
    client = dao.find_client(client_ip)
    if not client:
        print('did not find, doing a search')
        new_client = ClientModel(client_ip, datetime.now(), 0)
        dao.add_client(new_client)
    client.request_count += 1
    dao.update_client(client)
    return client

@app.route('/', methods=['GET'])
def index():
    dao = DAO()
    client_ip = request.remote_addr
    client = find_or_create_client(dao, client_ip)
    result = f'Client IP: {client.first_request} Request Count: {client.request_count} '

    proxies = dao.get_proxies()
    proxy = random_proxy_assigner(dao, client, proxies)
    result += f"Proxy Url: {proxy.url} "

    dao.add_connection(proxy, client)
    result += "CONNECTION CREATED"
    return result


def client_manager_server():
    app.run(debug=True, host="0.0.0.0", port=5001)
