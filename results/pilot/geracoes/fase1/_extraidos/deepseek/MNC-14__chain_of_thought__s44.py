import requests

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_file_duplicates(self, files):
        return list(set(files))

    def get_updates(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        return response.json()['result']

class Update:
    def __init__(self, update):
        self.update = update

    def get_file_id(self):
        try:
            return self.update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            try:
                return self.update['message']['document']['file_id']
            except KeyError:
                return None

class File:
    def __init__(self, token, file_id):
        self.token = token
        self.file_id = file_id

    def get_file_path(self):
        response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, self.file_id))
        return response.json()['result']['file_path']

def executar(token):
    """Devolve os caminhos dos arquivos recebidos pelo bot. Ponto de entrada publico desta unidade."""
    telegram_bot = TelegramBot(token)
    updates = telegram_bot.get_updates()
    files = []
    for update in updates:
        update_obj = Update(update)
        file_id = update_obj.get_file_id()
        if file_id:
            file_obj = File(token, file_id)
            files.append(file_obj)
    file_paths = [file.get_file_path() for file in files]
    return telegram_bot.remove_file_duplicates(file_paths)
