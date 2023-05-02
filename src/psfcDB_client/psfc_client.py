import json
import requests

def send_request(request):
    url = 'http://localhost:8080/'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=request, headers=headers)
    return response.text

def add_node(id, type, latitude, longitude, name):
    request = {
        'command': 'addNode',
        'id': id,
        'type': type,
        'latitude': latitude,
        'longitude': longitude,
        'name': name
    }
    return send_request(json.dumps(request))

def flush_all():
    request = {
        'command': 'flushAll'
    }
    return send_request(json.dumps(request))

def find_nodes_device(top_left, bottom_right):
    request = {
        'command': 'findNodes_device',
        'topLeft': top_left,
        'bottomRight': bottom_right
    }
    return send_request(json.dumps(request))

def num_pages():
    request = {
        'command': 'numPages'
    }
    return send_request(json.dumps(request))

# Usage examples

response = add_node(1, 2, 37.7749, -122.4194, 'Node1')
print('Add Node response:', response)

response = find_nodes_device([38.0, -122.5], [37.0, -122.0])
print('Find Nodes response:', response)

response = num_pages()
print('Num Pages response:', response)

response = flush_all()
print('Flush All response:', response)
