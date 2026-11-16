def _show_room_actions(room_data):
    action_number = 1
    for action in room_data[idx_room_actions]:
        print (str(action_number) + ". " + action[idx_action_name])
        action_number += 1

def _handle_user_input(room_data, choice):
    try:
        choice = int(choice)
        if choice < 1 or choice > len(room_data[idx_room_actions]):
            show_error ("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
            move_cursor("up",4)
        else:
            return choice
    except:
        show_error ("")
        move_cursor("up",4)
        return None

def _get_action_from_choice(room_data, choice):
    choice -= 1
    action = room_data[idx_room_actions][choice]
    return action

def play_room(room_id, message_from_previous_room, isFirstRoom):
    ...
    # show room actions
    _show_room_actions(room_data)
    ...
    # stay in this room until player quits or goes to another room
    while True:
        ...
        # check if user wants to quit
        if choice == "q":
            return ["player_quits",""]
        ...
        choice = _handle_user_input(room_data, choice)
        if choice is None:
            continue
        action = _get_action_from_choice(room_data, choice)
        ...
        # if action leads to new room id, return room_id and action message
        if action[idx_action_new_room] != "":
            return [action[idx_action_new_room], action[idx_action_message]]
        ...
