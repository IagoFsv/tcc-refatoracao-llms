import requests
import datetime

class APIClient:
    def __init__(self, token):
        self.token = token

    def send_request(self, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response

class TelegramBot:
    def __init__(self, api_client):
        self.api_client = api_client

    def remove_duplicates(self, users):
        new_users = []
        for i in users:
            if i not in new_users:
                new_users.append(i)
        return new_users

    def send_request(self, endpoint):
        response = self.api_client.send_request(endpoint)
        if endpoint == 'getMe':
            try:
                return response.json()['result']['username'], response.json()['result']['first_name'],\
                    response.json()['result']['id']
            except KeyError:
                raise Exception('Error: {}'.format(response.text))
        elif endpoint == 'getUpdates':
            users = []
            for i in response.json()['result']:
                try:
                    users.append((i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now},  {self.api_client.token},  {username},  {user_id}\n')
            return users

def executar(token, endpoint):
    api_client = APIClient(token)
    return TelegramBot(api_client).send_request(endpoint)
