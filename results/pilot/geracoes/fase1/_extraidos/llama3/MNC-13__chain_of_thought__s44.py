import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def send_telegram_request(self, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response.json()

    def process_telegram_response(self, response):
        if endpoint == 'getMe':
            try:
                return response['result']['username'], response['result']['first_name'], response['result']['id']
            except KeyError:
                raise Exception('Error: {}'.format(response.text))
        elif endpoint == 'getUpdates':
            users = []
            for i in response['result']:
                try:
                    users.append((i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            return users

    def write_users_log(self, users):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {self.token}, {username}, {user_id}\n')

    def send_request(self, endpoint):
        response = self.send_telegram_request(endpoint)
        if endpoint == 'getUpdates':
            users = self.process_telegram_response(response)
            self.write_users_log(users)
            return users
        else:
            return self.process_telegram_response(response)

def executar(token, endpoint):
    return TelegramBot(token).send_request(endpoint)
