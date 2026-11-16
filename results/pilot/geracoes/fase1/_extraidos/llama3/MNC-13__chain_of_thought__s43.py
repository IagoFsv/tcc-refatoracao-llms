import requests
import datetime

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def get_users(self, updates):
        users = []
        for update in updates:
            try:
                users.append(User(update['message']['from']['id'], update['message']['from']['username']))
            except KeyError:
                pass
        return users

    def send_request(self, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        if endpoint == 'getMe':
            # ...
        elif endpoint == 'getUpdates':
            users = self.get_users(response.json()['result'])
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for user in users:
                    f.write(f'{now}, {self.token}, {user.username}, {user.user_id}\n')
            return users

def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
