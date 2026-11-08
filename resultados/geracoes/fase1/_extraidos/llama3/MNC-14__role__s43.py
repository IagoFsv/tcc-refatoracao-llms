import requests


class TelegramBot:
    def __init__(self, token):
        self.token = token

    def get_tg_files(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        files = []
        for update in response.json().get('result', []):
            try:
                files.append(update.get('message', {}).get('reply_to_message', {}).get('document', {}).get('file_id'))
            except (KeyError, TypeError):
                pass
            try:
                files.append(update.get('message', {}).get('document', {}).get('file_id'))
            except (KeyError, TypeError):
                pass
        files = list(set(files))  # Remove duplicates
        file_paths = []
        for file_id in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json().get('result', {}).get('file_path'))
        return file_paths


def executar(token):
    return TelegramBot(token).get_tg_files()
