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

    def get_file_id(self, update):
        try:
            return update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            try:
                return update['message']['document']['file_id']
            except KeyError:
                return None

    def get_files(self):
        # get the telegram bot updates
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        # for each update, get the file id if it exists
        files = [self.get_file_id(i) for i in response.json()['result'] if self.get_file_id(i)]
        # call the remove_file_duplicates function to remove duplicate ids
        files = self.remove_file_duplicates(files)
        # for each file id, send a request to the telegram bot api to get the file path and store it in a list
        file_paths = []
        for i in files:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, i))
            file_paths.append(response.json()['result']['file_path'])
        # return the file paths
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_files()
