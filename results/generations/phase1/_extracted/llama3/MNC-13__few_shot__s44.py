"""Client of the bot API of a messaging app.

Public entry point: run(token, endpoint). Do not change its name or
signature; the rest of the file may be freely reorganized.
"""

import requests
import datetime


class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    # function to remove duplicates from a list
    def remove_duplicates(self, users):
        # create an empty list
        new_users = []
        # loop through the list
        for i in users:
            # if the user is not in the new list, append it
            if i not in new_users:
                new_users.append(i)
        # return the new list
        return new_users

    def send_request(self, endpoint):
        # send a request to the telegram bot api
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        # if the response is not 200, raise an exception
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        if endpoint == 'getMe':
            # Try to return the bot username, first name, username, and id
            try:
                return response.json()['result']
            except KeyError:
                raise Exception('Error: {}'.format(response.text))
        elif endpoint == 'getUpdates':
            # append the user id and username to a list
            users = []
            for i in response.json()['result']:
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


class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return f'User(id={self.id}, username={self.username})'


class TelegramUpdate:
    def __init__(self, users):
        self.users = [User(*user) for user in users]


def run(token, endpoint):
    """Sends the request to the endpoint and returns the result. Public entry point of this unit."""
    bot = TelegramBot(token)
    if endpoint == 'getMe':
        return bot.send_request(endpoint)
    elif endpoint == 'getUpdates':
        updates = bot.send_request(endpoint)
        return TelegramUpdate(updates)
    else:
        raise Exception('Invalid endpoint')
