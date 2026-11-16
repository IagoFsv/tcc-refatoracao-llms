import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def send_request(self, endpoint):
        response = self.handle_response(requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint)))
        if endpoint == 'getMe':
            return self.process_get_me(response)
        elif endpoint == 'getUpdates':
            users = self.process_get_updates(response)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users

    def handle_response(self, response):
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response.json()

    def process_get_me(self, response):
        try:
            return response['result']['username'], response['result']['first_name'], response['result']['id']
        except KeyError:
            raise Exception('Error: {}'.format(response.text))

    def process_get_updates(self, response):
        users = []
        for i in response['result']:
            try:
                users.append((i['message']['from']['id'], i['message']['from']['username']))
            except KeyError:
                pass
        users = self.remove_duplicates(users)
        return users

    def remove_duplicates(self, users):
        new_users = []
        for i in users:
            if i not in new_users:
                new_users.append(i)
        return new_users

def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
