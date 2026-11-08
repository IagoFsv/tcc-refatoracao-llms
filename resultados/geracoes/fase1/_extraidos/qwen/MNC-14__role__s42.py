import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def fetch_updates(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        return response.json()['result']

    def extract_file_ids(self, updates):
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

    def remove_file_duplicates(self, files):
        return list(dict.fromkeys(files))

    def get_file_paths(self, files):
        file_paths = []
        for file_id in files:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        updates = self.fetch_updates()
        file_ids = self.extract_file_ids(updates)
        file_ids = self.remove_file_duplicates(file_ids)
        file_paths = self.get_file_paths(file_ids)
        return file_paths

def executar(token):
    return TelegramBot(token).get_tg_files()
