import time
import random

closet_action = ("Oh oh. An old vacuum at the bottom of the closet suddenly comes to life.  "
                 "Its hose lifts magically into the air\nand wraps itself around your neck! "
                 "It sucks you in and - poof! You're gone.  You didn't make it.")

piano_action = "Most of the piano keys are broken. But as you play, a click can be heard by the front door!"

# variables to make it easier to read and access list data
idx_room_id = 0
idx_room_name = 1
idx_room_description = 2
idx_room_actions = 3
idx_room_hint = 4

idx_action_name = 0
idx_action_message = 1
idx_action_new_room = 2

new_line = "\r\n"

def _action(name, message, new_room):
    return [name, message, new_room]

def _get_room_data(room_id):
    for room in room_data:
        if room[idx_room_id] == room_id:
            return room
    return None

def _play_room(room_data, message_from_previous_room, isFirstRoom):
    clear_screen()

    print(colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line)

    if message_from_previous_room != "":
        print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
        time.sleep(1)

    if room_data[idx_room_description] != "":
        print(room_data[idx_room_description])
        time.sleep(0.5)

    print("")

    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    if isFirstRoom:
        promptIdx = 0
    else:
        promptIdx = random.randrange(0, len(user_prompts))

    print(user_prompts[promptIdx] + new_line)

    action_number = 1
    for action in room_data[idx_room_actions]:
        print(str(action_number) + ". " + action[idx_action_name])
        action_number += 1

    print("")
    print("h: hint")
    print("q: quit")
    print("")

    while True:
        choice_made = False
        while not choice_made:
            clear_to_end_of_line()
            choice = input("Enter your choice: ")
            clear_to_end_of_screen()

            if choice == "q":
                return ["player_quits", ""]

            if choice == "h":
                print(new_line + colorize("green", "regular", "normal", room_data[idx_room_hint]))
                move_cursor("up", 3)
                continue

            try:
                choice = int(choice)
                if choice < 1 or choice > len(room_data[idx_room_actions]):
                    show_error("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
                    move_cursor("up", 4)
                else:
                    choice_made = True
            except:
                show_error("")
                move_cursor("up", 4)

        action = room_data[idx_room_actions][choice - 1]

        if action[idx_action_new_room] != "":
            return [action[idx_action_new_room], action[idx_action_message]]

        if action[idx_action_message] != "":
            print("")
            print(colorize("blue", "regular", "high", action[idx_action_message]))
            move_cursor("up", 3)

def executar(sala, mensagem_anterior="", primeira_sala=False):
    room_data = _get_room_data(sala)
    if room_data is None:
        show_error("Program error: Room " + sala + " not found.  Aborting game.")
        exit()

    return _play_room(room_data, mensagem_anterior, primeira_sala)
