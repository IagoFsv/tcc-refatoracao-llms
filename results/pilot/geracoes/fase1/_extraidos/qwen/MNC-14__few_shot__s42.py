import requests
from typing import List, Dict

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files: List[str]) -> List[str]:
        return list(dict.fromkeys(files))

    def get_tg_updates(self) -> List[Dict]:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        return response.json().get('result', [])

    def get_file_ids(self, updates: List[Dict]) -> List[str]:
        file_ids = []
        for update in updates:
            try:
                file_ids.append(update['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            try:
                file_ids.append(update['message']['document']['file_id'])
            except KeyError:
                pass
        return file_ids

    def get_file_paths(self, file_ids: List[str]) -> List[str]:
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self) -> List[str]:
        updates = self.get_tg_updates()
        file_ids = self.get_file_ids(updates)
        unique_file_ids = self.remove_file_duplicates(file_ids)
        return self.get_file_paths(unique_file_ids)

def executar(token):
    return TelegramBot(token).get_tg_files()
