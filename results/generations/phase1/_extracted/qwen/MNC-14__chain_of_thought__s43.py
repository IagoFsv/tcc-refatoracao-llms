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

    def extract_file_id(self, update):
        # Extract file_id from update if it exists
        try:
            return update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            return None

    def extract_file_id_from_message(self, update):
        # Extract file_id from update if it exists
        try:
            return update['message']['document']['file_id']
        except KeyError:
            return None

    def get_tg_files(self):
            # get the telegram bot updates
            response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
            # for each update, get the file id if it exists
            files = []
            for update in response.json()['result']:
                file_id = self.extract_file_id(update)
                if file_id:
                    files.append(file_id)
                file_id = self.extract_file_id_from_message(update)
                if file_id:
                    files.append(file_id)
            # call the remove_file_duplicates function to remove duplicate ids
            files = self.remove_file_duplicates(files)
            # for each file id, send a request to the telegram bot api to get the file path and store it in a list
            file_paths = []
            for file_id in files:
                response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
                file_paths.append(response.json()['result']['file_path'])
            # return the file paths
            return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
