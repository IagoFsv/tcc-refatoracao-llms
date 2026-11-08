from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bot:
    token: str

    def __init__(self, token: str):
        self.token = token

    def remove_duplicates(self, users: list) -> list:
        new_users = []
        for i in users:
            if i not in new_users:
                new_users.append(i)
        return new_users

    def send_request(self, endpoint: str) -> list:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/{endpoint}')
        if response.status_code != 200:
            raise Exception(f'Error: {response.text}')
        if endpoint == 'getMe':
            try:
                return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
            except KeyError:
                raise Exception(f'Error: {response.text}')
        elif endpoint == 'getUpdates':
            users = []
            for i in response.json()['result']:
                try:
                    users.append((i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            users = self.remove_duplicates(users)
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users

def executar(token: str, endpoint: str) -> list:
    return Bot(token).send_request(endpoint)
