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
        # create an empty set
        new_files = set()
        # add each file to the set
        for file in files:
            new_files.add(file)
        # return the new set
        return new_files

    def get_file_id(self, update):
        # try to get the file id from the update
        try:
            return update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            return None
        except TypeError:
            return None

    def get_file_id_from_message(self, update):
        # try to get the file id from the update
        try:
            return update['message']['document']['file_id']
        except KeyError:
            return None
        except TypeError:
            return None

    def get_file_paths(self, files):
        # for each file id, send a request to the telegram bot api to get the file path and store it in a list
        file_paths = []
        for file_id in files:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        # return the file paths
        return file_paths

    def get_tg_files(self):
            # get the telegram bot updates
            response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
            # get the file ids from the updates
            files = []
            for update in response.json()['result']:
                file_id = self.get_file_id(update)
                if file_id:
                    files.append(file_id)
                file_id = self.get_file_id_from_message(update)
                if file_id:
                    files.append(file_id)
            # call the remove_file_duplicates function to remove duplicate ids
            files = self.remove_file_duplicates(files)
            # get the file paths
            file_paths = self.get_file_paths(files)
            # return the file paths
            return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
