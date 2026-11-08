import requests
from typing import List, Optional

class TelegramBot:
    def __init__(self, token: str):
        self.token = token

    def fetch_updates(self) -> List[dict]:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        return response.json()['result']

    def extract_file_ids(self, updates: List[dict]) -> List[Optional[str]]:
        file_ids = []
        for update in updates:
            message = update.get('message')
            if message:
                reply_to_message = message.get('reply_to_message')
                if reply_to_message:
                    document = reply_to_message.get('document')
                    if document:
                        file_ids.append(document.get('file_id'))
                document = message.get('document')
                if document:
                    file_ids.append(document.get('file_id'))
        return file_ids

    def remove_file_duplicates(self, file_ids: List[Optional[str]]) -> List[str]:
        return list(dict.fromkeys(filter(None, file_ids)))

    def get_file_paths(self, file_ids: List[str]) -> List[str]:
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self) -> List[str]:
        updates = self.fetch_updates()
        file_ids = self.extract_file_ids(updates)
        unique_file_ids = self.remove_file_duplicates(file_ids)
        return self.get_file_paths(unique_file_ids)

def executar(token: str) -> List[str]:
    return TelegramBot(token).get_tg_files()
