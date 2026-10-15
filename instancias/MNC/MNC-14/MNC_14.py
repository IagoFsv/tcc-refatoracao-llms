"""Cliente da API de bots de um aplicativo de mensagens: arquivos recebidos.

Ponto de entrada publico: executar(token). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import requests


class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files):
        # create an empty list
        new_files = []
        # loop through the list
        for i in files:
            # if the user is not in the new list, append it
            if i not in new_files:
                new_files.append(i)
        # return the new list
        return new_files

    def get_tg_files(self):
            # get the telegram bot updates
            response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
            # for each update, get the file id if it exists
            files = []
            for i in response.json()['result']:
                try:
                    files.append(i['message']['reply_to_message']['document']['file_id'])
                except KeyError:
                    pass
            # for each update, get the file id if it exists
            for i in response.json()['result']:
                try:
                    files.append(i['message']['document']['file_id'])
                except KeyError:
                    pass
            # call the remove_file_duplicates function to remove duplicate ids
            files = self.remove_file_duplicates(files)
            # for each file id, send a request to the telegram bot api to get the file path and store it in a list
            file_paths = []
            for i in files:
                response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, i))
                file_paths.append(response.json()['result']['file_path'])
            # return the file paths
            return file_paths


def executar(token):
    """Devolve os caminhos dos arquivos recebidos pelo bot. Ponto de entrada publico desta unidade."""
    return TelegramBot(token).get_tg_files()
