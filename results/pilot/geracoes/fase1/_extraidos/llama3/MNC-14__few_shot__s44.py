from typing import List

class TelegramBot:
    def __init__(self, token: str):
        self.token = token

    def get_update_files(self, response: dict) -> List[str]:
        files = []
        for update in response.get('result', []):
            try:
                files.append(update.get('message', {}).get('reply_to_message', {}).get('document', {}).get('file_id'))
            except (KeyError, AttributeError):
                pass
            try:
                files.append(update.get('message', {}).get('document', {}).get('file_id'))
            except (KeyError, AttributeError):
                pass
        return files

    def remove_file_duplicates(self, files: List[str]) -> List[str]:
        new_files = []
        for file in files:
            if file not in new_files:
                new_files.append(file)
        return new_files

    def get_tg_files(self) -> List[str]:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        files = self.get_update_files(response.json())
        files = self.remove_file_duplicates(files)
        file_paths = []
        for file_id in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

def executar(token: str) -> List[str]:
    return TelegramBot(token).get_tg_files()
