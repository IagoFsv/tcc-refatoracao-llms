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

    def fetch_bot_info(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getMe')
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response.json()['result']

    def fetch_updates(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response.json()['result']

    def process_updates(self, updates):
        users = []
        for update in updates:
            try:
                user_id = update['message']['from']['id']
                username = update['message']['from']['username']
                users.append((user_id, username))
            except KeyError:
                pass
        return users

    def log_users(self, users):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {self.token}, {username}, {user_id}\n')

    def send_request(self, endpoint):
        if endpoint == 'getMe':
            return self.fetch_bot_info()
        elif endpoint == 'getUpdates':
            updates = self.fetch_updates()
            users = self.process_updates(updates)
            users = self.remove_duplicates(users)
            self.log_users(users)
            return users


def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
