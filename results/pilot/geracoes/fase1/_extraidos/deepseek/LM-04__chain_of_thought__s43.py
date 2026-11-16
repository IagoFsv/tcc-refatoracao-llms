"""Aventura de texto: uma sala do jogo, com descricao, acoes e dica.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import time
import random

# Restante do código omitido para brevidade...

def get_user_choice(room_data):
    """Lê a escolha do usuário e retorna a ação escolhida."""
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
            # check if number is out of range
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
    action = room_data[idx_room_actions][choice - 1]
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
    # Restante do código omitido para brevidade...

    # show room actions
    action_number = 1
    for action in room_data[idx_room_actions]:
        print(str(action_number) + ". " + action[idx_action_name])
        action_number += 1

    # show quit and hint options
    print("")
    print("h: hint")
    print("q: quit")
    print("")

    # stay in this room until player quits or goes to another room
    while True:
        result = get_user_choice(room_data)
        if result[0] != "":
            return result
        # get info for selected action.  Subtract 1 from choice as list starts at 0
        action = room_data[idx_room_actions][choice - 1]
        # if action leads to new room id, return room_id and action message
        if action[idx_action_new_room] != "":
            return [action[idx_action_new_room], action[idx_action_message]]
        # show action message in blue, if there is one
        if action[idx_action_message] != "":
            print("")
            print(colorize("blue", "regular", "high", action[idx_action_message]))
            # go back to input prompt
            move_cursor("up", 3)

# Restante do código omitido para brevidade...
