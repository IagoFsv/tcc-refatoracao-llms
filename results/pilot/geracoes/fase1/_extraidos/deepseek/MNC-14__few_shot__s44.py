import requests
from typing import List
from dataclasses import dataclass, field

@dataclass
class File:
    id: str
    path: str

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files: List[File]) -> List[File]:
        new_files = []
        for i in files:
            if i not in new_files:
                new_files.append(i)
        return new_files

    def get_tg_files(self) -> List[str]:
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        files = []
        for i in response.json()['result']:
            try:
                files.append(File(i['message']['reply_to_message']['document']['file_id'], i['message']['reply_to_message']['document']['file_path']))
            except KeyError:
                pass
        for i in response.json()['result']:
            try:
                files.append(File(i['message']['document']['file_id'], i['message']['document']['file_path']))
            except KeyError:
                pass
        files = self.remove_file_duplicates(files)
        file_paths = [file.path for file in files]
        return file_paths


def executar(token: str) -> List[str]:
    return TelegramBot(token).get_tg_files()
