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
        for i in files:
            # if the user is not in the new list, append it
            if i not in new_files:
                new_files.append(i)
        # return the new list
        return new_files

    def get_file_id_from_update(self, update):
        try:
            return update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            return None

    def get_file_id_from_message(self, update):
        try:
            return update['message']['document']['file_id']
        except KeyError:
            return None

    def get_file_ids(self, updates):
        files = []
        for update in updates:
            file_id = self.get_file_id_from_update(update)
            if file_id:
                files.append(file_id)
            file_id = self.get_file_id_from_message(update)
            if file_id:
                files.append(file_id)
        return files

    def get_file_paths(self, file_ids):
        file_paths = []
        for file_id in file_ids:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        # get the telegram bot updates
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        updates = response.json()['result']
        # get the file ids
        file_ids = self.get_file_ids(updates)
        # remove duplicate ids
        file_ids = self.remove_file_duplicates(file_ids)
        # get the file paths
        file_paths = self.get_file_paths(file_ids)
        # return the file paths
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
