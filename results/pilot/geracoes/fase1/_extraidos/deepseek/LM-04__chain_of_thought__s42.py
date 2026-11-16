def show_actions(room_data, action_number):
    for action in room_data[idx_room_actions]:
        print(str(action_number) + ". " + action[idx_action_name])
    return action_number + len(room_data[idx_room_actions])

def handle_user_choice(room_data, user_prompts, isFirstRoom):
    choice_made = False
    while not choice_made:
        # clear previous input
        clear_to_end_of_line()
        # show input prompt
        choice = input("Enter your choice: ")
        clear_to_end_of_screen()
        # check if user wants to quit
        if choice == "q":
            return ["player_quits",""]
        if choice == "h":
            print(new_line + colorize("green","regular","normal", room_data[idx_room_hint]))
            move_cursor("up",3)
            continue
        try:
            choice = int(choice)
            if choice < 1 or choice > len(room_data[idx_room_actions]):
                show_error("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
                move_cursor("up",4)
            else:
                choice_made = True
        except:
            show_error("")
            move_cursor("up",4)
    action = room_data[idx_room_actions][choice-1]
    if action[idx_action_new_room] != "":
        return [action[idx_action_new_room], action[idx_action_message]]
    if action[idx_action_message] != "":
        print("")
        print(colorize("blue","regular","high", action[idx_action_message]))
        move_cursor("up",3)

def play_room(room_id, message_from_previous_room, isFirstRoom):
    room_data = get_room_data(room_id)
    if room_data == None:
        show_error("Program error: Room " + room_id + " not found.  Aborting game.")
        exit()
    clear_screen()
    print(colorize("cyan","underline","high",(room_data[idx_room_name]).upper()) + new_line)
    if message_from_previous_room != "":
        print(colorize("yellow","regular","normal", message_from_previous_room) + new_line)
        time.sleep(1)
    if room_data[idx_room_description] != "":
        print(room_data[idx_room_description])
        time.sleep(0.5)
    print("")
    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    if isFirstRoom:
        promptIdx = 0
    else:
        promptIdx = random.randrange(0,len(user_prompts))
    print(user_prompts[promptIdx] + new_line)
    action_number = show_actions(room_data, 1)
    print("")
    print("h: hint")
    print("q: quit")
    print("")
    while True:
        result = handle_user_choice(room_data, user_prompts, isFirstRoom)
        if result is not None:
            return result
