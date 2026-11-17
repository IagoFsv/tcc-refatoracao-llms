"""Client of the bot API of a messaging app.

Public entry point: run(token, endpoint). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import requests
import datetime
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str


class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    # function to remove duplicates from a list
    def remove_duplicates(self, users: List[User]) -> List[User]:
        # create an empty list
        new_users: List[User] = []
        # loop through the list
        for user in users:
            # if the user is not in the new list, append it
            if user not in new_users:
                new_users.append(user)
        # return the new list
        return new_users

    def send_request(self, endpoint: str) -> str:
        # send a request to the telegram bot api
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        # if the response is not 200, raise an exception
        if response.status_code != 200:
            raise Exception('Error:  {}'.format(response.text))
        if endpoint == 'getMe':
            # Try to return the bot username, first name, username, and id
            try:
                return response.json()['result']['username'], response.json()['result']['first_name'],\
                    response.json()['result']['id']
            except KeyError:
                raise Exception('Error:  {}'.format(response.text))
        elif endpoint == 'getUpdates':
            # append the user id and username to a list
            users: List[User] = []
            for i in response.json()['result']:
                try:
                    users.append(User(i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            # call a function to remove duplicates
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
            with open('users.log', 'a') as f:
                for user in users:
                    f.write(f'{now},  {self.token},  {user.username},  {user.id}\n')
            return users


def run(token: str, endpoint: str) -> str:
    """Sends the request to the endpoint and returns the result. Public entry point of this unit."""
    return TelegramBot(token).send_request(endpoint)
