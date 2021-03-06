import requests
import json
from pprint import pprint

user = input('enter account name: ')
psw = input('enter password: ')

web = 'https://api.github.com/user/repos'
response = requests.get(web, auth=(user, psw))
response = response.json()
with open('lesson_1_t1.json', 'w', encoding='utf8') as f:
    json.dump(response, f, indent=2) #indent for beauty code

for repo in response:
    print(f'{repo["name"]} - {repo["description"]}')
