import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def send_request(self, endpoint):
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
            for update in response.json()['result']:
                try:
                    user_id = update['message']['from']['id']
                    username = update['message']['from']['username']
                    users.append((user_id, username))
                except KeyError:
                    pass
            users = list(set(users))
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for user_id, username in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users

def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
