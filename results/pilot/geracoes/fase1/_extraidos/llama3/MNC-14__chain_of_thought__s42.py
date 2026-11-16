import requests


class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def get_file_ids(self, updates):
        files = []
        for i in updates:
            try:
                files.append(i['message']['reply_to_message']['document']['file_id'])
            except KeyError:
                pass
            try:
                files.append(i['message']['document']['file_id'])
            except KeyError:
                pass
        return files

    def remove_duplicates(self, files):
        new_files = []
        for i in files:
            if i not in new_files:
                new_files.append(i)
        return new_files

    def get_file_paths(self, files):
        file_paths = []
        for i in files:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={i}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = response.json()['result']
        file_ids = self.get_file_ids(updates)
        file_ids = self.remove_duplicates(file_ids)
        return self.get_file_paths(file_ids)


def executar(token):
    """Devolve os caminhos dos arquivos recebidos pelo bot. Ponto de entrada publico desta unidade."""
    return TelegramBot(token).get_tg_files()
