def get_room_data(room_id):
    # ...

def show_room_name(room_data):
    print(colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line)

def show_room_description(room_data):
    if room_data[idx_room_description] != "":
        print(room_data[idx_room_description])
        time.sleep(0.5)

def show_room_actions(room_data):
    action_number = 1
    for action in room_data[idx_room_actions]:
        print(str(action_number) + ". " + action[idx_action_name])
        action_number += 1

def show_user_prompts(is_first_room):
    if is_first_room:
        prompt_idx = 0
    else:
        prompt_idx = random.randrange(0, len(user_prompts))
    print(user_prompts[prompt_idx] + new_line)

def handle_user_input(room_data, is_first_room):
    # ...

def execute_action(action):
    # ...

def play_room(room_id, message_from_previous_room, is_first_room):
    room_data = get_room_data(room_id)
    # ...

    show_room_name(room_data)
    show_room_description(room_data)
    show_user_prompts(is_first_room)
    show_room_actions(room_data)

    while True:
        choice_made = False
        while not choice_made:
            # ...
            choice = input("Enter your choice: ")
            # ...

        choice_made = True
        action = room_data[idx_room_actions][choice-1]
        if action[idx_action_new_room] != "":
            return [action[idx_action_new_room], action[idx_action_message]]
        if action[idx_action_message] != "":
            print("")
            print(colorize("blue", "regular", "high", action[idx_action_message]))
            move_cursor("up", 3)
        # ...

def executar(sala, mensagem_anterior="", primeira_sala=False):
    """Joga a sala ate o jogador sair dela; devolve [proxima_sala, mensagem]. Ponto de entrada publico desta unidade."""
    return play_room(sala, mensagem_anterior, primeira_sala)
