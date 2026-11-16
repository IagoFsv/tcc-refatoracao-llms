def show_room_name(room_name):
    print(colorize("cyan", "underline", "high", room_name.upper()) + new_line)

def show_previous_message(message):
    if message != "":
        print(colorize("yellow", "regular", "normal", message) + new_line)
        time.sleep(1)

def show_room_description(room_description):
    if room_description != "":
        print(room_description)
        time.sleep(0.5)

def show_user_prompt(prompt):
    print(prompt + new_line)

def show_room_actions(room_actions):
    action_number = 1
    for action in room_actions:
        print(str(action_number) + ". " + action[idx_action_name])
        action_number += 1

def show_quit_and_hint_options():
    print("")
    print("h: hint")
    print("q: quit")
    print("")

def show_error(message):
    print(new_line + colorize("red", "regular", "high", message) + new_line)
