"""Client of the bot API of a messaging app: received files.

Public entry point: run(token). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import requests
from typing import List
from dataclasses import dataclass, field

@dataclass
class Document:
    file_id: str
    file_path: str

@dataclass
class Message:
    reply_to_message: 'Message' = None
    document: Document = None

@dataclass
class Update:
    message: Message

@dataclass
class TelegramBot:
    # function to initialize the class
    def  __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files: List[str]) -> List[str]:
        # create an empty list
        new_files: List[str] = []
        # loop through the list
        for file in files:
            # if the user is not in the new list, append it
            if file not in new_files:
                new_files.append(file)
        # return the new list
        return new_files

    def get_tg_files(self) -> List[str]:
        # get the telegram bot updates
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        # for each update, get the file id if it exists
        files: List[str] = []
        updates: List[Update] = response.json()['result']
        for update in updates:
            try:
                files.append(update.message.reply_to_message.document.file_id)
            except AttributeError:
                pass
            try:
                files.append(update.message.document.file_id)
            except AttributeError:
                pass
        # call the remove_file_duplicates function to remove duplicate ids
        files = self.remove_file_duplicates(files)
        # for each file id, send a request to the telegram bot api to get the file path and store it in a list
        file_paths: List[str] = []
        for file in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file}')
            file_paths.append(response.json()['result']['file_path'])
        # return the file paths
        return file_paths


def run(token: str) -> List[str]:
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
