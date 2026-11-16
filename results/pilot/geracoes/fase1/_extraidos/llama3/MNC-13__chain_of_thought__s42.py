class TelegramBot:
    # function to initialize the class
    def __init__(self, token):
        # set the token
        self.token = token

    # function to remove duplicates from a list
    def remove_duplicates(self, users):
        # create an empty list
        new_users = []
        # loop through the list
        for i in users:
            # if the user is not in the new list, append it
            if i not in new_users:
                new_users.append(i)
        # return the new list
        return new_users

    def get_bot_info(self):
        # send a request to the telegram bot api
        response = requests.get('https://api.telegram.org/bot{}/getMe'.format(self.token))
        # if the response is not 200, raise an exception
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        try:
            return response.json()['result']['username'], response.json()['result']['first_name'], response.json()['result']['id']
        except KeyError:
            raise Exception('Error: {}'.format(response.text))

    def get_updates(self):
        # send a request to the telegram bot api
        response = requests.get('https://api.telegram.org/bot{}/getUpdates'.format(self.token))
        # if the response is not 200, raise an exception
        if response.status_code != 200:
            raise Exception('Error: {}'.format(response.text))
        users = []
        for i in response.json()['result']:
            try:
                users.append((i['message']['from']['id'], i['message']['from']['username']))
            except KeyError:
                pass
        # call a function to remove duplicates
        users = self.remove_duplicates(users)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('users.log', 'a') as f:
            for username, user_id in users:
                f.write(f'{now}, {self.token}, {username}, {user_id}\n')
        return users

    def send_request(self, endpoint):
        if endpoint == 'getMe':
            return self.get_bot_info()
        elif endpoint == 'getUpdates':
            return self.get_updates()
        else:
            raise Exception('Endpoint not supported')
