def display_description(room_data):
    print(colorize("cyan","underline","high",(room_data[idx_room_name]).upper()) + new_line)
    if room_data[idx_room_description] != "":
        print(room_data[idx_room_description])
        time.sleep(0.5)

def ask_user_to_do(room_data, isFirstRoom):
    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    if isFirstRoom:
        promptIdx = 0
    else:
        promptIdx = random.randrange(0,len(user_prompts))
    print(user_prompts[promptIdx] + new_line)
    return promptIdx

def process_user_choice(room_data, promptIdx):
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
        # make sure input is a number between 1 and the number of options
        try:
            # convert choice to integer 
            choice = int(choice)
            # check if number is out of range
            if choice < 1 or choice > len(room_data[idx_room_actions]):
                show_error("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
                move_cursor("up",4)
            else:
                choice_made = True
        except:
            # ignore error
            show_error("")
            move_cursor("up",4)
    return choice

def check_action(action):
    if action[idx_action_new_room] != "":
        return [action[idx_action_new_room], action[idx_action_message]]
    return None

def display_message(action):
    if action[idx_action_message] != "":
        print("")
        print(colorize("blue","regular","high", action[idx_action_message]))

def play_room(room_id, message_from_previous_room, isFirstRoom):
    room_data = get_room_data(room_id)
    if room_data == None:
        show_error("Program error: Room " + room_id + " not found.  Aborting game.")
        exit()
    clear_screen()
    display_description(room_data)
    if message_from_previous_room != "":
        print(colorize("yellow","regular","normal", message_from_previous_room) + new_line)
        time.sleep(1)
    promptIdx = ask_user_to_do(room_data, isFirstRoom)
    choice = process_user_choice(room_data, promptIdx)
    action = room_data[idx_room_actions][choice-1]
    result = check_action(action)
    if result is not None:
        return result
    display_message(action)
    return play_room(room_id, message_from_previous_room, isFirstRoom)
