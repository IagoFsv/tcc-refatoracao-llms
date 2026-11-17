"""Client of the bot API of a messaging app: received files.

Public entry point: run(token). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import requests
from typing import List, Optional

class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files: List[str]) -> List[str]:
        # create an empty set
        new_files = set()
        # loop through the list
        for file in files:
            # if the file is not in the set, add it
            if file not in new_files:
                new_files.add(file)
        # return the new list
        return list(new_files)

    def get_file_id(self, update: dict) -> Optional[str]:
        try:
            return update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            return None

    def get_file_id_from_message(self, update: dict) -> Optional[str]:
        try:
            return update['message']['document']['file_id']
        except KeyError:
            return None

    def get_file_paths(self, file_ids: List[str]) -> List[str]:
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        # get the telegram bot updates
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = response.json()['result']
        
        # extract file ids
        files = []
        for update in updates:
            file_id = self.get_file_id(update)
            if file_id:
                files.append(file_id)
            file_id = self.get_file_id_from_message(update)
            if file_id:
                files.append(file_id)
        
        # remove duplicate ids
        files = self.remove_file_duplicates(files)
        
        # get file paths
        file_paths = self.get_file_paths(files)
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
