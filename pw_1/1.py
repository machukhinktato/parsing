import requests
import json
from pprint import pprint


web = 'https://api.github.com/users/machukhinktato/repos'
response = requests.get(web)
with open('lesson_1.json', 'w', encoding='utf8') as f:
    json.dump(response.text , f)