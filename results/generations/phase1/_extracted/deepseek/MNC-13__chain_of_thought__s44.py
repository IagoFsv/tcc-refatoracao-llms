import requests
import datetime


class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_duplicates(self, users):
        new_users = []
        for i in users:
            if i not in new_users:
                new_users.append(i)
        return new_users

    def send_request(self, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        if endpoint == 'getMe':
            try:
                return self.parse_get_me_response(response)
            except KeyError:
                raise Exception('Error: {}'.format(response.text))
        elif endpoint == 'getUpdates':
            users = self.parse_get_updates_response(response)
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users

    def parse_get_me_response(self, response):
        result = response.json()['result']
        return result['username'], result['first_name'], result['id']

    def parse_get_updates_response(self, response):
        users = []
        for i in response.json()['result']:
            try:
                users.append((i['message']['from']['id'], i['message']['from']['username']))
            except KeyError:
                pass
        return users


def run(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
