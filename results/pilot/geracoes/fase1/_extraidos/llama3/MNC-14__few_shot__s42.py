from typing import List

class TelegramBot:
    def __init__(self, token: str):
        self.token = token

    def _get_file_ids(self, response: dict) -> List[str]:
        file_ids = []
        for update in response['result']:
            try:
                file_ids.append(update['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            try:
                file_ids.append(update['message']['document']['file_id'])
            except KeyError:
                pass
        return file_ids

    def _get_file_paths(self, file_ids: List[str]) -> List[str]:
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self) -> List[str]:
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        file_ids = self._get_file_ids(response.json())
        file_ids = list(set(file_ids))
        return self._get_file_paths(file_ids)

def executar(token: str) -> List[str]:
    return TelegramBot(token).get_tg_files()
