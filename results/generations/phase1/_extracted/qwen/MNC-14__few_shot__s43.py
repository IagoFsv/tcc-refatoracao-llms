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

    def get_tg_files(self):
        # get the telegram bot updates
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        # extract file ids from updates
        file_ids = self.extract_file_ids(response.json())
        # remove duplicate file ids
        file_ids = self.remove_file_duplicates(file_ids)
        # get file paths for each file id
        file_paths = self.get_file_paths(file_ids)
        # return the file paths
        return file_paths

    def extract_file_ids(self, response):
        # initialize an empty list for file ids
        file_ids = []
        # loop through the updates
        for update in response['result']:
            # try to get file id from reply_to_message
            try:
                file_ids.append(update['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            # try to get file id from message
            try:
                file_ids.append(update['message']['document']['file_id'])
            except KeyError:
                pass
        # return the list of file ids
        return file_ids

    def get_file_paths(self, file_ids):
        # initialize an empty list for file paths
        file_paths = []
        # loop through the file ids
        for file_id in file_ids:
            # get the file path and append it to the list
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        # return the list of file paths
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
