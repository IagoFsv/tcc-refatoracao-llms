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
        response = self.send_telegram_request(endpoint)
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response.json()['result']

    def send_telegram_request(self, endpoint):
        return requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))

    def process_response(self, endpoint, result):
        if endpoint == 'getMe':
            return self.handle_getMe(result)
        elif endpoint == 'getUpdates':
            return self.handle_getUpdates(result)
        else:
            raise Exception('Unsupported endpoint')

    def handle_getMe(self, result):
        try:
            return result['username'], result['first_name'], result['id']
        except KeyError:
            raise Exception('Error: {}'.format(result))

    def handle_getUpdates(self, result):
        users = []
        for i in result:
            try:
                users.append((i['message']['from']['id'], i['message']['from']['username']))
            except KeyError:
                pass
        users = self.remove_duplicates(users)
        return users

    def log_users(self, users):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {self.token}, {username}, {user_id}\n')


def executar(token, endpoint):
    return TelegramBot(token).process_response(endpoint, TelegramBot(token).send_request(endpoint))
