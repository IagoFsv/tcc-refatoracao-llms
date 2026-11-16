import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files):
        return list(dict.fromkeys(files))

    def get_file_ids(self, updates):
        file_ids = []
        for update in updates:
            try:
                file_ids.append(update['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
        for update in updates:
            try:
                file_ids.append(update['message']['document']['file_id'])
            except KeyError:
                pass
        return file_ids

    def get_file_paths(self, file_ids):
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = response.json()['result']
        file_ids = self.get_file_ids(updates)
        file_ids = self.remove_file_duplicates(file_ids)
        file_paths = self.get_file_paths(file_ids)
        return file_paths

def executar(token):
    return TelegramBot(token).get_tg_files()
