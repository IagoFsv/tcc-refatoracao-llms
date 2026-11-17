"""Client of the bot API of a messaging app: received files.

Public entry point: run(token). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import requests
from typing import List, Dict, Any

class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files: List[str]) -> List[str]:
        # create an empty set to store unique file ids
        new_files = set()
        for file_id in files:
            new_files.add(file_id)
        return list(new_files)

    def extract_file_ids(self, updates: List[Dict[str, Any]]) -> List[str]:
        files = []
        for update in updates:
            message = update.get('message', {})
            reply_to_message = message.get('reply_to_message', {})
            document = reply_to_message.get('document', {})
            if document:
                files.append(document['file_id'])
            document = message.get('document', {})
            if document:
                files.append(document['file_id'])
        return files

    def get_tg_files(self):
        # get the telegram bot updates
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = response.json().get('result', [])
        # extract file ids from updates
        files = self.extract_file_ids(updates)
        # remove duplicate file ids
        files = self.remove_file_duplicates(files)
        # get file paths
        file_paths = []
        for file_id in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        # return the file paths
        return file_paths


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
