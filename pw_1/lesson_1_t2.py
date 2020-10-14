import requests
from pprint import pprint
from tokens import access_token
import json

response = requests.get(
    f'https://api.vk.com/method/groups.get?v=5.52&access_token={access_token}')
response = response.json()
with open('lesson_1_t2.json', 'w', encoding='utf8') as f:
    json.dump(response, f, indent=2)

pprint(response['response']['items'])
