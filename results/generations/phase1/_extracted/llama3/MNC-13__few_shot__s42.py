"""Client of the bot API of a messaging app.

Public entry point: run(token, endpoint). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

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

    def _parse_get_me_response(self, response):
        try:
            return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
        except KeyError:
            raise Exception('Error: {}'.format(response.text))

    def _parse_get_updates_response(self, response):
        users = []
        for message in response.json()['result']:
            try:
                users.append((message['message']['from']['id'], message['message']['from']['username']))
            except KeyError:
                pass
        return users

    def send_request(self, endpoint):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/{endpoint}')
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        if endpoint == 'getMe':
            return self._parse_get_me_response(response)
        elif endpoint == 'getUpdates':
            users = self._parse_get_updates_response(response)
            self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for user_id, username in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users


def run(token, endpoint):
    """Sends the request to the endpoint and returns the result. Public entry point of this unit."""
    return TelegramBot(token).send_request(endpoint)
