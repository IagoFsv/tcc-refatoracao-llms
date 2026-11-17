"""Client of the bot API of a messaging app: received files.

Public entry point: run(token). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import requests


class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files):
        # create an empty list
        new_files = []
        # loop through the list
        for file in files:
            # if the file is not in the new list, append it
            if file not in new_files:
                new_files.append(file)
        # return the new list
        return new_files

    def get_file_ids(self, updates):
        # get the file ids from the updates
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
        # get the file paths from the file ids
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        # get the telegram bot updates
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = response.json()['result']
        # get the file ids
        file_ids = self.get_file_ids(updates)
        # remove duplicate file ids
        file_ids = self.remove_file_duplicates(file_ids)
        # get the file paths
        file_paths = self.get_file_paths(file_ids)
        # return the file paths
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
