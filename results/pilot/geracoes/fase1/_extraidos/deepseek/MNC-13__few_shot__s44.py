"""Cliente da API de bots de um aplicativo de mensagens.

Ponto de entrada publico: executar(token, endpoint). Nao altere o nome nem a
assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import requests
import datetime
from typing import List, Tuple

class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    # function to remove duplicates from a list
    def remove_duplicates(self, users: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        return list(set(users))

    def send_request(self, endpoint: str):
        # send a request to the telegram bot api
        response = requests.get(f'https://api.telegram.org/bot{self.token}/{endpoint}')
        # if the response is not 200, raise an exception
        if response.status_code != 200:
            raise Exception(f'Error: {response.text}')
        if endpoint == 'getMe':
            # Try to return the bot username, first name, username, and id
            try:
                return (response.json()['result']['username'], 
                        response.json()['result']['first_name'],
                        response.json()['result']['id'])
            except KeyError:
                raise Exception(f'Error: {response.text}')
        elif endpoint == 'getUpdates':
            # append the user id and username to a list
            users: List[Tuple[str, str]] = []
            for i in response.json()['result']:
                try:
                    users.append((i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            # call a function to remove duplicates
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users


def executar(token: str, endpoint: str):
    """Envia o pedido ao endpoint e devolve o resultado. Ponto de entrada publico desta unidade."""
    return TelegramBot(token).send_request(endpoint)
