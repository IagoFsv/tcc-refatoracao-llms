"""Cliente da API de bots de um aplicativo de mensagens: arquivos recebidos.

Ponto de entrada publico: executar(token). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import requests
from typing import List
from dataclasses import dataclass, field

@dataclass
class Document:
    file_id: str
    file_path: str

class TelegramBot:
    # function to initialize the class
    def  __init__(self, token):
        # set the token
        self.token = token

    def remove_file_duplicates(self, files: List[Document]) -> List[Document]:
        # create an empty list
        new_files: List[Document] = []
        # loop through the list
        for file in files:
            # if the user is not in the new list, append it
            if file not in new_files:
                new_files.append(file)
        # return the new list
        return new_files

    def get_tg_files(self) -> List[Document]:
        # get the telegram bot updates
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        # for each update, get the file id if it exists
        files: List[Document] = []
        for update in response.json()['result']:
            try:
                files.append(Document(file_id=update['message']['reply_to_message']['document']['file_id'], file_path=""))
            except KeyError:
                pass
            try:
                files.append(Document(file_id=update['message']['document']['file_id'], file_path=""))
            except KeyError:
                pass
        # call the remove_file_duplicates function to remove duplicate ids
        files = self.remove_file_duplicates(files)
        # for each file id, send a request to the telegram bot api to get the file path and store it in a list
        for i in range(len(files)):
            response = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(self.token, files[i].file_id))
            files[i].file_path = response.json()['result']['file_path']
        # return the file paths
        return files


def executar(token) -> List[Document]:
    """Devolve os caminhos dos arquivos recebidos pelo bot. Ponto de entrada publico desta unidade."""
    return TelegramBot(token).get_tg_files()
