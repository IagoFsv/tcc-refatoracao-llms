def _show_room_name(room_data):
  print(colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line)

def _show_message_from_previous_room(message_from_previous_room):
  if message_from_previous_room != "":
    print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
    time.sleep(1)

def _show_room_description(room_data):
  if room_data[idx_room_description] != "":
    print(room_data[idx_room_description])
    time.sleep(0.5)

def _show_room_actions(room_data):
  action_number = 1
  for action in room_data[idx_room_actions]:
    print(str(action_number) + ". " + action[idx_action_name])
    action_number += 1

def _show_quit_and_hint_options():
  print("")
  print("h: hint")
  print("q: quit")
  print("")

def _get_user_input(room_data):
  while True:
    # clear previous input
    clear_to_end_of_line()

    # show input prompt
    choice = input("Enter your choice: ")

    clear_to_end_of_screen()

    # check if user wants to quit
    if choice == "q":
      return "player_quits"

    if choice == "h":
      print(new_line + colorize("green", "regular", "normal", room_data[idx_room_hint]))
      move_cursor("up", 3)
      continue

    # make sure input is a number between 1 and the number of options
    try:
      choice = int(choice)
      if choice < 1 or choice > len(room_data[idx_room_actions]):
        show_error("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
        move_cursor("up", 4)
      else:
        return choice
    except:
      # ignore error
      show_error("")
      move_cursor("up", 4)

def _handle_user_choice(room_data, choice):
  action = room_data[idx_room_actions][choice-1]
  if action[idx_action_new_room] != "":
    return [action[idx_action_new_room], action[idx_action_message]]
  if action[idx_action_message] != "":
    print("")
    print(colorize("blue", "regular", "high", action[idx_action_message]))
    move_cursor("up", 3)

def play_room(room_id, message_from_previous_room, isFirstRoom):
  room_data = get_room_data(room_id)
  if room_data == None:
    show_error("Program error: Room " + room_id + " not found.  Aborting game.")
    exit()

  clear_screen()

  _show_room_name(room_data)
  _show_message_from_previous_room(message_from_previous_room)
  _show_room_description(room_data)

  print("")

  user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
  if isFirstRoom:
    promptIdx = 0
  else:
    promptIdx = random.randrange(0, len(user_prompts))

  print(user_prompts[promptIdx] + new_line)

  _show_room_actions(room_data)

  _show_quit_and_hint_options()

  choice = _get_user_input(room_data)
  while choice == "q":
    return ["player_quits", ""]

  choice = _get_user_input(room_data)
  return _handle_user_choice(room_data, choice)
