from dataclasses import dataclass

@dataclass
class BotConfig:
    token: str

@dataclass
class Bot:
    config: BotConfig

    def __init__(self, config: BotConfig):
        self.config = config

    def remove_duplicates(self, users):
        new_users = []
        for i in users:
            if i not in new_users:
                new_users.append(i)
        return new_users

    def send_request(self, endpoint):
        response = requests.get(f'https://api.telegram.org/bot{self.config.token}/{endpoint}')
        if response.status_code != 200:
            raise Exception(f'Error: {response.text}')
        if endpoint == 'getMe':
            try:
                return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
            except KeyError:
                raise Exception(f'Error: {response.text}')
        elif endpoint == 'getUpdates':
            users = []
            for i in response.json()['result']:
                try:
                    users.append((i['message']['from']['id'], i['message']['from']['username']))
                except KeyError:
                    pass
            users = self.remove_duplicates(users)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open('users.log', 'a') as f:
                for username, user_id in users:
                    f.write(f'{now}, {self.config.token}, {username}, {user_id}\n')
            return users

def executar(token, endpoint):
    return Bot(BotConfig(token)).send_request(endpoint)
