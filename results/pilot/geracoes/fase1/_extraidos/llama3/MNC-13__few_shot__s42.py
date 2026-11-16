from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

@dataclass
class BotToken:
    token: str

@dataclass
class Bot:
    token: BotToken

    def __init__(self, token: BotToken):
        self.token = token

    def send_request(self, endpoint: str) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]]]:
        response = requests.get(f'https://api.telegram.org/bot{self.token.token}/{endpoint}')
        if response.status_code != 200:
            raise Exception(f'Error: {response.text}')
        if endpoint == 'getMe':
            return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
        elif endpoint == 'getUpdates':
            users = []
            for i in response.json()['result']:
                try:
                    users.append((i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            users = list(set(users))
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token.token}, {username}, {user_id}\n')
            return users

def executar(token: BotToken, endpoint: str) -> List[Tuple[int, str]]:
    return Bot(token).send_request(endpoint)
