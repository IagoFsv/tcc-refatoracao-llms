import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def _get_file_ids(self, response):
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

    def _get_file_paths(self, file_ids):
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        file_ids = self._get_file_ids(response.json())
        file_ids = list(set(file_ids))  # remove duplicates
        return self._get_file_paths(file_ids)

def run(token):
    return TelegramBot(token).get_tg_files()
