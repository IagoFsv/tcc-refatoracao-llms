def _show_room_name(room_data):
    return colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line

def _show_room_description(room_data):
    return room_data[idx_room_description]

def _show_user_prompts():
    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    promptIdx = random.randrange(0, len(user_prompts))
    return user_prompts[promptIdx] + new_line

def _show_room_actions(room_data):
    action_number = 1
    actions = []
    for action in room_data[idx_room_actions]:
        actions.append(str(action_number) + ". " + action[idx_action_name])
        action_number += 1
    return actions

def _show_quit_and_hint_options():
    return """
h: hint
q: quit
"""

def _show_input_prompt():
    return "Enter your choice: "

def _show_error(message):
    print(new_line + colorize("red", "regular", "high", message) + new_line)

def play_room(room_id, message_from_previous_room, isFirstRoom):
    # ...
    clear_screen()
    _show_room_name(room_data)
    if message_from_previous_room != "":
        print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
        time.sleep(1)
    _show_room_description(room_data)
    print("")
    _show_user_prompts()
    actions = _show_room_actions(room_data)
    print("\n".join(actions))
    print(_show_quit_and_hint_options())
    # ...
