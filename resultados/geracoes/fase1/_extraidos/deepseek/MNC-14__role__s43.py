import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files):
        return list(set(files))

    def get_tg_files(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        files = []
        for i in response.json()['result']:
            try:
                files.append(i['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            try:
                files.append(i['message']['document']['file_id'])
            except KeyError:
                pass
        files = self.remove_file_duplicates(files)
        file_paths = [requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, i)).json()['result']['file_path'] for i in files]
        return file_paths

def executar(token):
    return TelegramBot(token).get_tg_files()
