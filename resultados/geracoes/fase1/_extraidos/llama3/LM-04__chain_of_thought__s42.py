def show_room_name(room_data):
    print(colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line)

def show_message_from_previous_room(message_from_previous_room):
    if message_from_previous_room != "":
        print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
        time.sleep(1)

def show_room_description(room_data):
    if room_data[idx_room_description] != "":
        print(room_data[idx_room_description])
        time.sleep(0.5)

def show_user_prompts(isFirstRoom):
    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    if isFirstRoom:
        promptIdx = 0
    else:
        promptIdx = random.randrange(0, len(user_prompts))
    print(user_prompts[promptIdx] + new_line)

def show_room_actions(room_data):
    action_number = 1
    for action in room_data[idx_room_actions]:
        print(str(action_number) + ". " + action[idx_action_name])
        action_number += 1

def show_quit_and_hint_options():
    print("")
    print("h: hint")
    print("q: quit")
    print("")

def handle_user_input(room_data, isFirstRoom):
    choice_made = False
    while not choice_made:
        # clear previous input
        clear_to_end_of_line()

        # show input prompt
        choice = input("Enter your choice: ")

        clear_to_end_of_screen()

        # check if user wants to quit
        if choice == "q":
            return ["player_quits", ""]

        if choice == "h":
            print(new_line + colorize("green", "regular", "normal", room_data[idx_room_hint]))
            move_cursor("up", 3)
            continue

        # make sure input is a number between 1 and the number of options
        try:
            choice = int(choice)
            if choice < 1 or choice > len(room_data[idx_room_actions]):
                show_error("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
                move_cursor("up", 4)
            else:
                choice_made = True
        except:
            # ignore error
            show_error("")
            move_cursor("up", 4)

    # get info for selected action.  Subtract 1 from choice as list starts at 0
    action = room_data[idx_room_actions][choice-1]

    # if action leads to new room id, return room_id and action message
    if action[idx_action_new_room] != "":
        return [action[idx_action_new_room], action[idx_action_message]]

    # show action message in blue, if there is one
    if action[idx_action_message] != "":
        print("")
        print(colorize("blue", "regular", "high", action[idx_action_message]))
        # go back to input prompt
        move_cursor("up", 3)

def play_room(room_id, message_from_previous_room, isFirstRoom):
    room_data = get_room_data(room_id)

    if room_data == None:
        show_error("Program error: Room " + room_id + " not found.  Aborting game.")
        exit()

    clear_screen()

    show_room_name(room_data)
    show_message_from_previous_room(message_from_previous_room)
    show_room_description(room_data)
    show_user_prompts(isFirstRoom)
    show_room_actions(room_data)
    show_quit_and_hint_options()

    return handle_user_input(room_data, isFirstRoom)

def executar(sala, mensagem_anterior="", primeira_sala=False):
    """Joga a sala ate o jogador sair dela; devolve [proxima_sala, mensagem]. Ponto de entrada publico desta unidade."""
    return play_room(sala, mensagem_anterior, primeira_sala)
