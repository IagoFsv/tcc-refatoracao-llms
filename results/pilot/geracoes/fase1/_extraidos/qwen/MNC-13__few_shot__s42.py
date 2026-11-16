import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_duplicates(self, users):
        new_users = []
        for user in users:
            if user not in new_users:
                new_users.append(user)
        return new_users

    def get_bot_info(self, response):
        try:
            return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
        except KeyError:
            raise Exception('Error: {}'.format(response.text))

    def get_updates(self, response):
        users = []
        for update in response.json()['result']:
            try:
                users.append((update['message']['from']['id'], update['message']['from']['username']))
            except KeyError:
                pass
        return users

    def log_users(self, users):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as file:
            for username, user_id in users:
                file.write(f'{now}, {self.token}, {username}, {user_id}\n')

    def send_request(self, endpoint):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/{endpoint}')
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        if endpoint == 'getMe':
            return self.get_bot_info(response)
        elif endpoint == 'getUpdates':
            users = self.get_updates(response)
            users = self.remove_duplicates(users)
            self.log_users(users)
            return users

def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
