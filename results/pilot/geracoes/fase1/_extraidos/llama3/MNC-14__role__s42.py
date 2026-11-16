import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def get_updates(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        return response.json()['result']

    def get_files(self, updates):
        files = []
        for update in updates:
            try:
                files.append(update['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            try:
                files.append(update['message']['document']['file_id'])
            except KeyError:
                pass
        return self.remove_file_duplicates(files)

    def remove_file_duplicates(self, files):
        new_files = []
        for i in files:
            if i not in new_files:
                new_files.append(i)
        return new_files

    def get_file_paths(self, files):
        file_paths = []
        for file_id in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        updates = self.get_updates()
        files = self.get_files(updates)
        return self.get_file_paths(files)

def executar(token):
    return TelegramBot(token).get_tg_files()
