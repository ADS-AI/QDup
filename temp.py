import requests

headers = {
    'accept': 'application/json',
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
}

json_data = {
    'content': 'when mercury ii chloride is treated with excess of stannous chloride the products obtained are',
}

response = requests.post('http://localhost:8000/gettaxonomy', headers=headers, json=json_data)
print(response.text)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{  "content": "first three nearest neighbour distances for primitive cubic lattice are respectively edge length of unit cell a"\n}'
#response = requests.post('http://localhost:8000/gettaxonomy', headers=headers, data=data)