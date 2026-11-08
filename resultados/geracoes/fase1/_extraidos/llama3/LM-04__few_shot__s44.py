def show_hint(room_data):
    print(new_line + colorize("green","regular","normal", room_data[idx_room_hint]))

def play_room(room_id, message_from_previous_room, isFirstRoom):
    # ...
    while True:
        # ...
        if choice == "h":
            show_hint(room_data)
            move_cursor("up",3)
            continue
        # ...
