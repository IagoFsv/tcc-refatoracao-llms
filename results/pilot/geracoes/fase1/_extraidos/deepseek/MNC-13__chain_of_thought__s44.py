import requests
import datetime

class TelegramBot:
    def __init__(self, token):
        self.token = token

    def remove_duplicates(self, users):
        new_users = []
        for i in users:
            if i not in new_users:
                new_users.append(i)
        return new_users

class TelegramBotRequest:
    @staticmethod
    def send_request(bot, endpoint):
        response = requests.get('https://api.telegram.org/bot{}/{}'.format(bot.token, endpoint))
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        return response

class TelegramBotGetMe:
    @staticmethod
    def get_info(response):
        try:
            return response.json()['result']['username'], response.json()['result']['first_name'],\
                response.json()['result']['id']
        except KeyError:
            raise Exception('Error: {}'.format(response.text))

class TelegramBotGetUpdates:
    @staticmethod
    def get_updates(bot, response):
        users = []
        for i in response.json()['result']:
            try:
                users.append((i['message']['from']['id'], i['message']['from']['username']))
            except KeyError:
                pass
        users = bot.remove_duplicates(users)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {bot.token}, {username}, {user_id}\n')
        return users

def executar(token, endpoint):
    bot = TelegramBot(token)
    response = TelegramBotRequest.send_request(bot, endpoint)
    if endpoint == 'getMe':
        return TelegramBotGetMe.get_info(response)
    elif endpoint == 'getUpdates':
        return TelegramBotGetUpdates.get_updates(bot, response)
