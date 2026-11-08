import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files):
        return list(set(files))

    def get_tg_files(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        files = self.get_files_from_updates(response.json()['result'])
        files = self.remove_file_duplicates(files)
        file_paths = self.get_file_paths(files)
        return file_paths

    def get_files_from_updates(self, updates):
        files = []
        for update in updates:
            files.extend(self.get_files_from_update(update))
        return files

    def get_files_from_update(self, update):
        files = []
        try:
            files.append(update['message']['reply_to_message']['document']['file_id'])
        except KeyError:
            pass
        try:
            files.append(update['message']['document']['file_id'])
        except KeyError:
            pass
        return files

    def get_file_paths(self, files):
        file_paths = []
        for file in files:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file))
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

def executar(token):
    return TelegramBot(token).get_tg_files()
