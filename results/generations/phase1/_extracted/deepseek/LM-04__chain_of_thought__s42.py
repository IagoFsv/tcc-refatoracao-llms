"""Text adventure: one room of the game, with description, actions and hint.

Public entry point: run(room, previous_message="", first_room=False). Do not
change its name or signature; the rest of the file may be freely reorganized.
"""

import time
import random

# ... rest of the code ...

def handle_user_input(room_data):
    """Handles user input for the room."""
    # make sure input is a number between 1 and the number of options
    while True:
        # get user input
        choice = input("Enter your choice: ")

        # check if user wants to quit
        if choice == "q":
            return ["player_quits",""]

        if choice == "h":
            print(new_line + colorize("green","regular","normal", room_data[idx_room_hint]))
            move_cursor("up",3)
            continue

        # check if number is out of range
        try:
            choice = int(choice)
            if choice < 1 or choice > len(room_data[idx_room_actions]):
                show_error("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
                move_cursor("up",4)
            else:
                return room_data[idx_room_actions][choice-1]
        except:
            # ignore error
            show_error("")
            move_cursor("up",4)

def play_room(room_id, message_from_previous_room, isFirstRoom):
    """Plays the room until the player leaves it; returns [next_room, message]. Public entry point of this unit."""
    # get room data
    room_data = get_room_data(room_id)

    # if room not found, show error and end game
    if room_data is None:
        show_error("Program error: Room " + room_id + " not found.  Aborting game.")
        exit()

    clear_screen()

    # show room name
    print(colorize("cyan","underline","high",(room_data[idx_room_name]).upper()) + new_line)

    # show message from previous room if there is one
    if message_from_previous_room != "":
        print(colorize("yellow","regular","normal", message_from_previous_room) + new_line)
        time.sleep(1)

    # show room description 
    if room_data[idx_room_description] != "":
        print(room_data[idx_room_description])
        time.sleep(0.5)

    print("")

    # ask user what to do
    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    if isFirstRoom:
        promptIdx = 0
    else:
        promptIdx = random.randrange(0,len(user_prompts))

    print(user_prompts[promptIdx] + new_line)

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
        action = handle_user_input(room_data)

        # if action leads to new room id, return room_id and action message
        if action[idx_action_new_room] != "":
            return [action[idx_action_new_room], action[idx_action_message]]

        # show action message in blue, if there is one
        if action[idx_action_message] != "":
            print("")
            print(colorize("blue","regular","high", action[idx_action_message]))
            # go back to input prompt
            move_cursor("up",3)

def run(room, previous_message="", first_room=False):
    """Plays the room until the player leaves it; returns [next_room, message]. Public entry point of this unit."""
    return play_room(room, previous_message, first_room)
