import requests


class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    # ...

    def get_file_id(self, update):
        try:
            return update['message']['reply_to_message']['document']['file_id']
        except KeyError:
            return None

    def get_file_ids(self, updates):
        return [self.get_file_id(update) for update in updates if self.get_file_id(update)]

    def get_file_paths(self, file_ids):
        file_paths = []
        for file_id in file_ids:
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, file_id))
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        updates = response.json()['result']
        file_ids = self.get_file_ids(updates)
        return self.get_file_paths(file_ids)


def executar(token):
    """Devolve os caminhos dos arquivos recebidos pelo bot. Ponto de entrada publico desta unidade."""
    return TelegramBot(token).get_tg_files()
