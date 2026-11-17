def show_room_name(room_data):
  clear_screen()
  print(colorize("cyan", "underline", "high", (room_data[idx_room_name]).upper()) + new_line)

def show_room_description(room_data):
  if room_data[idx_room_description] != "":
    print(room_data[idx_room_description])
    time.sleep(0.5)

def show_room_actions(room_data):
  action_number = 1
  for action in room_data[idx_room_actions]:
    print(str(action_number) + ". " + action[idx_action_name])
    action_number += 1

def show_quit_and_hint_options():
  print("")
  print("h: hint")
  print("q: quit")
  print("")

def handle_user_input(room_data, previous_message, first_room):
  user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
  if first_room:
    promptIdx = 0
  else:
    promptIdx = random.randrange(0, len(user_prompts))
  print(user_prompts[promptIdx] + new_line)
  show_room_actions(room_data)
  print("")
  print("")

def play_room(room_id, message_from_previous_room, isFirstRoom):
  room_data = get_room_data(room_id)
  if room_data is None:
    show_error("Program error: Room " + room_id + " not found.  Aborting game.")
    exit()
  show_room_name(room_data)
  if message_from_previous_room != "":
    print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
    time.sleep(1)
  show_room_description(room_data)
  handle_user_input(room_data, message_from_previous_room, isFirstRoom)
  return play_room(room_id, "", False)

def run(room, previous_message="", first_room=False):
  return play_room(room, previous_message, first_room)
