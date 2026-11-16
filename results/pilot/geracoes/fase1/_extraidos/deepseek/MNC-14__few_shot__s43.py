import requests
from typing import List
from dataclasses import dataclass

@dataclass
class Document:
    file_id: str
    file_path: str

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files: List[Document]) -> List[Document]:
        new_files = []
        for i in files:
            if i not in new_files:
                new_files.append(i)
        return new_files

    def get_tg_files(self) -> List[str]:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        files = []
        for i in response.json()['result']:
            try:
                files.append(Document(i['message']['reply_to_message']['document']['file_id'], None))
            except KeyError:
                pass
        for i in response.json()['result']:
            try:
                files.append(Document(i['message']['document']['file_id'], None))
            except KeyError:
                pass
        files = self.remove_file_duplicates(files)
        file_paths = []
        for i in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={i.file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

def executar(token: str) -> List[str]:
    return TelegramBot(token).get_tg_files()
