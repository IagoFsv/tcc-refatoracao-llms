def show_room(room_id, message_from_previous_room, isFirstRoom):
  room_data = get_room_data(room_id)
  if room_data is None:
    show_error("Program error: Room " + room_id + " not found.  Aborting game.")
    exit()

  clear_screen()
  print(colorize("cyan", "underline", "high", room_data[idx_room_name].upper()) + new_line)
  if message_from_previous_room != "":
    print(colorize("yellow", "regular", "normal", message_from_previous_room) + new_line)
    time.sleep(1)

  print(room_data[idx_room_description])
  time.sleep(0.5)
  print("")

  user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
  if isFirstRoom:
    promptIdx = 0
  else:
    promptIdx = random.randrange(0, len(user_prompts))

  print(user_prompts[promptIdx] + new_line)

  action_number = 1
  for action in room_data[idx_room_actions]:
    print(str(action_number) + ". " + action[idx_action_name])
    action_number += 1

  print("")
  print("h: hint")
  print("q: quit")
  print("")

  return

def executar(sala, mensagem_anterior="", primeira_sala=False):
  """Joga a sala ate o jogador sair dela; devolve [proxima_sala, mensagem]. Ponto de entrada publico desta unidade."""
  return play_room(sala, mensagem_anterior, primeira_sala)
