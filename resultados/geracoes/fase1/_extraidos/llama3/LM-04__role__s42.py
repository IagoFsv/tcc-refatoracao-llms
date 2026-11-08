def show_room_info(room):
  clear_screen()
  print(colorize("cyan", "underline", "high", room[idx_room_name].upper()) + new_line)
  if room[idx_room_description] != "":
    print(room[idx_room_description])
    time.sleep(0.5)
  print("")

def show_actions(room, isFirstRoom):
  action_number = 1
  for action in room[idx_room_actions]:
    print(str(action_number) + ". " + action[idx_action_name])
    action_number += 1
  print("")
  print("h: hint")
  print("q: quit")
  print("")

def show_hint(room):
  print(new_line + colorize("green", "regular", "normal", room[idx_room_hint]))
  move_cursor("up", 3)

def show_action_message(action):
  if action[idx_action_message] != "":
    print("")
    print(colorize("blue", "regular", "high", action[idx_action_message]))
    move_cursor("up", 3)

def executar(sala, mensagem_anterior="", primeira_sala=False):
  """Joga a sala ate o jogador sair dela; devolve [proxima_sala, mensagem]. Ponto de entrada publico desta unidade."""
  room_data = get_room_data(sala)
  if (room_data == None):
    show_error ("Program error: Room " + sala + " not found.  Aborting game.")
    exit()
  show_room_info(room_data)
  if mensagem_anterior != "":
    print(colorize("yellow", "regular", "normal", mensagem_anterior) + new_line)
    time.sleep(1)
  user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
  if primeira_sala:
    promptIdx = 0
  else:
    promptIdx = random.randrange(0,len(user_prompts))
  print(user_prompts[promptIdx] + new_line)
  show_actions(room_data, primeira_sala)
  while True:
    choice_made = False
    while not choice_made:
      clear_to_end_of_line()
      choice = input("Enter your choice: ")
      clear_to_end_of_screen()
      if choice == "q":
        return ["player_quits",""]
      if choice == "h":
        show_hint(room_data)
        continue
      try:
        choice = int(choice)
        if choice < 1 or choice > len(room_data[idx_room_actions]):
          show_error ("Please enter a number between 1 and " + str(len(room_data[idx_room_actions])) + ".")
          move_cursor("up",4)
        else:
          choice_made = True
      except:
        show_error ("")
        move_cursor("up",4)
    action = room_data[idx_room_actions][choice-1]
    if action[idx_action_new_room] != "":
      return [action[idx_action_new_room], action[idx_action_message]]
    show_action_message(action)
    move_cursor("up",3)
