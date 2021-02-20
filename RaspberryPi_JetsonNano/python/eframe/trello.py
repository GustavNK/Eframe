import requests
import json

class TrelloCard():
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        return self.name == other.name




def getTrelloCards():
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

    todo_list = json.loads(response.text)

    todo_cards_name = []

    for card in todo_list:
        thisCard = TrelloCard(card['name'])
        todo_cards_name.append(thisCard)

    return todo_cards_name




def splitName(card):
    string = list(card.name)
    space_break = 0
    for n in range(24, 10, -1):
        if (string[n] == ' '):
            space_break = n
            break
    string = []
    string.append(card.name[0:space_break])
    string.append(card.name[space_break+1:space_break+20])

    return string