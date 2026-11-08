def show_hint(room_data):
    print (new_line + colorize("green","regular","normal", room_data[idx_room_hint]))
    move_cursor("up",3)

def handle_user_input(room_data, choice):
    if choice == "h":
        show_hint(room_data)
    # ...

def play_room(room_id, message_from_previous_room, isFirstRoom):
    # ...
    while True:
        # ...
        choice = input("Enter your choice: ")
        clear_to_end_of_screen()
        if choice == "h":
            handle_user_input(room_data, choice)
        # ...
