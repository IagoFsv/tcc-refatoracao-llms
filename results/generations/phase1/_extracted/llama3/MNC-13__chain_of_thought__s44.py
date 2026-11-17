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
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(self.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))

        result = response.json()['result']
        if endpoint == 'getMe':
            try:
                return (result['username'], result['first_name'], result['id'])
            except KeyError:
                raise Exception('Error: {}'.format(response.text))
        elif endpoint == 'getUpdates':
            users = []
            for i in response.json()['result']:
                try:
                    user = i['message']['from']
                    users.append((user['id'], user['username']))
                except KeyError:
                    pass
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.token}, {username}, {user_id}\n')
            return users


def run(token, endpoint):
    """Sends the request to the endpoint and returns the result. Public entry point of this unit."""
    return TelegramBot(token).send_request(endpoint)
