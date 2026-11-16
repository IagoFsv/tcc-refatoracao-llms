import requests

class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files):
        # create an empty set to store unique file ids
        unique_files = set()
        for file in files:
            unique_files.add(file)
        # return the list of unique file ids
        return list(unique_files)

    def get_file_ids(self, updates):
        # initialize an empty list to store file ids
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

    def get_file_paths(self, file_ids):
        # initialize an empty list to store file paths
        file_paths = []
        for file_id in file_ids:
            response = requests.get(f'https://api.telegram.org/bot{self.token}/getFile?file_id={file_id}')
            file_paths.append(response.json()['result']['file_path'])
        return file_paths

    def get_tg_files(self):
        # get the telegram bot updates
        response = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates')
        updates = response.json()['result']
        # get unique file ids
        file_ids = self.get_file_ids(updates)
        # remove duplicate file ids
        file_ids = self.remove_file_duplicates(file_ids)
        # get file paths
        file_paths = self.get_file_paths(file_ids)
        # return the file paths
        return file_paths


def executar(token):
    """Devolve os caminhos dos arquivos recebidos pelo bot. Ponto de entrada publico desta unidade."""
    return TelegramBot(token).get_tg_files()
