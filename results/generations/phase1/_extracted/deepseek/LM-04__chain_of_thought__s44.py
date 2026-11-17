def play_room(room_id, message_from_previous_room, isFirstRoom):
    # get room data
    room_data = get_room_data(room_id)

    # if room not found, show error and end game
    if room_data is None:
        show_error("Program error: Room " + room_id + " not found.  Aborting game.")
        exit()

    clear_screen()

    # show room name
    print(colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line)

    # show message from previous room if there is one
    if message_from_previous_room != "":
        print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
        time.sleep(1)

    # show room description 
    show_room_description(room_data)

    # ask user what to do
    user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
    if isFirstRoom:
        promptIdx = 0
    else:
        promptIdx = random.randrange(0,len(user_prompts))

    print(user_prompts[promptIdx] + new_line)

    # show room actions
    show_room_actions(room_data)

    # show quit and hint options
    print("")
    show_hint(room_data)
    show_quit_option()
    print("")

    # stay in this room until player quits or goes to another room
    while True:
        # get user input
        choice_made = False
        while not choice_made:
            # clear previous input
            clear_to_end_of_line()

            # show input prompt
            choice = get_user_input()

            clear_to_end_of_screen()

            # check if user wants to quit
            if choice == "q":
                return ["player_quits",""]

            if choice == "h":
                show_hint(room_data)
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
            move_cursor("up",3)
