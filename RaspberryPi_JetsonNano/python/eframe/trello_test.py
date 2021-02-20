import requests
import json

list_id = '5de4f37bfc5a3c403cfd5167' #todo list
trello_url = "https://api.trello.com/1/lists/" + list_id + "/cards"

query = {
    'key' : 'c7ffc6ebf2d3c93ee02614068dbe6b81',
    'token' : '45a7b04cccf3a51acd5df97deb84411737f1838a3e02ae33acaf23ee7828a48c'
}

response = requests.request(
    "GET",
    trello_url,
    params=query
)

todo_list = json.loads(response.text)

todo_cards_name = []

for card in todo_list:
    todo_cards_name.append(card['name'])

print(todo_cards_name)