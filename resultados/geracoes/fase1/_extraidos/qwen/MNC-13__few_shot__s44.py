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

    def send_request(self, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))

        if endpoint == 'getMe':
            try:
                return response.json()['result']['username'], response.json()['result']['first_name'],\
                    response.json()['result']['id']
            except KeyError:
                raise Exception('Error: {}'.format(response.text))

        elif endpoint == 'getUpdates':
            users = []
            for item in response.json()['result']:
                try:
                    users.append((item['message']['from']['id'], item['message']['from']['username']))
                except KeyError:
                    pass
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users


def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
