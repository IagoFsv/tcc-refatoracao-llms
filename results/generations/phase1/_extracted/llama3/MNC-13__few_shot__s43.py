import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def _remove_duplicates(self, users):
        new_users = []
        for user in users:
            if user not in new_users:
                new_users.append(user)
        return new_users

    def _get_updates(self, response):
        users = []
        for update in response.json()['result']:
            try:
                users.append((update['message']['from']['id'], update['message']['from']['username']))
            except KeyError:
                pass
        return users

    def _log_users(self, users):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {self.token}, {username}, {user_id}\n')

    def send_request(self, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        if endpoint == 'getMe':
            return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
        elif endpoint == 'getUpdates':
            users = self._get_updates(response)
            users = self._remove_duplicates(users)
            self._log_users(users)
            return users

def run(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
