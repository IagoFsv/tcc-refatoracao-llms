import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_duplicates(self, users):
        return list(set(users))

    def send_request(self, endpoint):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/{endpoint}')
        if response.status_code != 200:
            raise Exception(f'Error: {response.text}')
        if endpoint == 'getMe':
            return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
        elif endpoint == 'getUpdates':
            users = [(i['message']['from']['id'], i['message']['from']['username']) for i in response.json()['result'] if 'message' in i]
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users

def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
