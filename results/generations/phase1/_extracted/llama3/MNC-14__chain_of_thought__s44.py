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

    def get_tg_files(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        files = []
        for update in response.json()['result']:
            message = update.get('message')
            if message:
                reply_to_message = message.get('reply_to_message')
                if reply_to_message and 'document' in reply_to_message:
                    files.append(reply_to_message['document']['file_id'])
                if 'document' in message:
                    files.append(message['document']['file_id'])
        files = self.remove_file_duplicates(files)
        file_paths = []
        for file_id in files:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        # return the file paths
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
