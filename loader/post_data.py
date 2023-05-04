import json
import requests

def post_data(data, agent_name, url="http://localhost:5050/logging/"):
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost'
    }

    json_data = json.dumps({"data": data}, sort_keys=True, indent=4)
    requests.post(f"{url}{agent_name}", headers=headers, json=json.loads(json_data))
