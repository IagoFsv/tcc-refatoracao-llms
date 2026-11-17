"""Client of the bot API of a messaging app.

Public entry point: run(token, endpoint). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import requests
import datetime
from typing import List, Tuple

class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    # function to remove duplicates from a list
    def remove_duplicates(self, users: List[Tuple[int, str]]) -> List[Tuple[int, str]]:
        # use a set to remove duplicates
        return list(set(users))

    def send_request(self, endpoint: str) -> dict:
        # send a request to the telegram bot api
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        # if the response is not 200, raise an exception
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response.json()['result']

    def get_me_info(self) -> Tuple[str, str, int]:
        # Try to return the bot username, first name, username, and id
        result = self.send_request('getMe')
        return result['username'], result['first_name'], result['id']

    def get_updates(self) -> List[Tuple[int, str]]:
        # append the user id and username to a list
        users = []
        result = self.send_request('getUpdates')
        for i in result:
            try:
                users.append((i['message']['from']['id'], i['message']['from']['username']))
            except KeyError:
                pass
        # call a function to remove duplicates
        users = self.remove_duplicates(users)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {self.token}, {username}, {user_id}\n')
        return users


def run(token: str, endpoint: str) -> dict:
    """Sends the request to the endpoint and returns the result. Public entry point of this unit."""
    bot = TelegramBot(token)
    if endpoint == 'getMe':
        return bot.get_me_info()
    elif endpoint == 'getUpdates':
        return bot.get_updates()
