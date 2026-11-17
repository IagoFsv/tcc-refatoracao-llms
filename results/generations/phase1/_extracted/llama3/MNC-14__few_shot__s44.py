"""Client of the bot API of a messaging app: received files.

Public entry point: run(token). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import requests
from typing import List

class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def get_file_ids(self, updates):
        file_ids = []
        for update in updates:
            try:
                file_ids.append(update['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            try:
                file_ids.append(update['message']['document']['file_id'])
            except KeyError:
                pass
        return file_ids

    def get_file_paths(self, file_ids):
        file_paths = []
        for file_id in file_ids:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def remove_file_duplicates(self, file_ids):
        new_file_ids = []
        for file_id in file_ids:
            if file_id not in new_file_ids:
                new_file_ids.append(file_id)
        return new_file_ids

    def get_tg_files(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        updates = response.json()['result']
        file_ids = self.get_file_ids(updates)
        file_ids = self.remove_file_duplicates(file_ids)
        return self.get_file_paths(file_ids)

def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
