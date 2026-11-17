"""Client of the bot API of a messaging app: received files.

Public entry point: run(token). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import requests
from dataclasses import dataclass

@dataclass
class File:
    file_id: str
    file_path: str

@dataclass
class Update:
    message: 'Message'
    result: list

@dataclass
class Message:
    reply_to_message: 'Message'
    document: 'Document'

@dataclass
class Document:
    file_id: str

@dataclass
class TelegramBot:
    token: str

    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files):
        new_files = []
        for file in files:
            if file not in new_files:
                new_files.append(file)
        return new_files

    def get_file(self, file_id):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
        return File(file_id, response.json()['result']['file_path'])

    def get_tg_files(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = [Update(message=m, result=r) for m, r in zip(response.json()['result'], response.json()['result'][1:])]
        files = []
        for update in updates:
            try:
                files.append(update.message.reply_to_message.document.file_id)
            except AttributeError:
                pass
            try:
                files.append(update.message.document.file_id)
            except AttributeError:
                pass
        files = self.remove_file_duplicates(files)
        return [self.get_file(file_id) for file_id in files]


def run(token):
    """Returns the paths of the files received by the bot. Public entry point of this unit."""
    return TelegramBot(token).get_tg_files()
