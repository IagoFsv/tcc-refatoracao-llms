"""Text adventure: one room of the game, with description, actions and hint.

Public entry point: run(room, previous_message="", first_room=False). Do not
change its name or signature; the rest of the file may be freely reorganized.
"""

import time
import random

closet_action = ("Oh oh. An old vacuum at the bottom of the closet suddenly comes to life.  "
                 "Its hose lifts magically into the air\nand wraps itself around your neck!  "
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


basement_dark = ["basement_dark", "basement storage room",
                 "You're not sure how you got here. It is quite dark and there's water dripping in the distance.   "
                 "\nThere's a door to your left and a door to your right.  There's also a chest in the corner with a  "
                 "\nstrange hum coming from it.",
                 [_action("Open the left door", "The left door is locked.", ""),
                  _action("Open the right door", "The right door is locked.", ""),
                  _action("Open the chest", "The chest is locked.", ""),
                  _action("Flick the light switch on the wall", "The lights are now on.", "basement_light")],
                 "Any option is safe."]

upstairs_unlocked = ["upstairs_unlocked", "Upstairs Living Room", "",
                     [_action("Open the front door", "", "player_wins"),
                      _action("Check out the grandfather clock", "The clock appears to be broken.", ""),
                      _action("Open the closet", closet_action, "player_dies"),
                      _action("Go back downstairs", "You make your way back down the spiral stair case.", "basement_library_3"),
                      _action("Play the piano", piano_action, "")],
                     "A click by the front door?  You're almost there.  Only one thing left to do!"]

room_data = [basement_dark, upstairs_unlocked]


def move_cursor(direction, amount):
    if direction == "up":
        print("\033[" + str(amount) + "A", end="")
    elif direction == "down":
        print("\033[" + str(amount) + "B", end="")
    elif direction == "right":
        print("\033[" + str(amount) + "C", end="")
    elif direction == "left":
        print("\033[" + str(amount) + "D", end="")


def clear_screen():
    print("\033[2J\033[0;0f", end="")


def clear_to_end_of_screen():
    print("\033[J", end="")


def clear_to_end_of_line():
    print("\033[K", end="")


# Valid colors: black, red, green, yellow, blue, purple, cyan, white.
# Valid styles: regular, bold, underline.
# Valid intensities: normal, high.
def colorize(color, style, intensity, text):
    txt_colors = {
        # regular, high-intensity
        "black": ["30", "90"],
        "red": ["31", "91"],
        "green": ["32", "92"],
        "yellow": ["33", "93"],
        "blue": ["34", "94"],
        "purple": ["35", "95"],
        "cyan": ["36", "96"],
        "white": ["37", "97"]
    }
    txt_styles = {"regular": "0", "bold": "1", "underline": "4"}
    txt_intensities = {"normal": "0", "high": "1"}

    return "\033[{0};{1};{2}m{3}\033[0m".format(
        txt_intensities[intensity],
        txt_styles[style],
        txt_colors[color][int(txt_intensities[intensity])],
        text
    )


def show_error(message):
    print(new_line + colorize("red", "regular", "high", message) + new_line)


def get_room_data(room_id):
    for room in room_data:
        if room[idx_room_id] == room_id:
            return room
    return None


def play_room(room_id, message_from_previous_room, is_first_room):
    room_data = get_room_data(room_id)

    if room_data is None:
        show_error("Program error: Room " + room_id + " not found.  Aborting game.")
        exit()

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
    if is_first_room:
        prompt_idx = 0
    else:
        prompt_idx = random.randrange(0, len(user_prompts))

    print(user_prompts[prompt_idx] + new_line)

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


def run(room, previous_message="", first_room=False):
    """Plays the room until the player leaves it; returns [next_room, message]. Public entry point of this unit."""
    return play_room(room, previous_message, first_room)
