"""Aventura de texto: uma sala do jogo, com descricao, acoes e dica.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import time
import random

new_line = "\r\n"

def _action(name, message, new_room):
  return [name, message, new_room]

def extract_room_data(room_id):
  for room in room_data:
    if room[0] == room_id:
      return room
  return None

def show_room(room_data, message_from_previous_room):
  clear_screen()
  print(colorize("cyan","underline","high",(room_data[1]).upper()) + new_line)
  if message_from_previous_room != "":
    print(colorize("yellow","regular","normal", message_from_previous_room) + new_line)
  if room_data[2] != "":
    print(room_data[2])
    time.sleep(0.5)
  print("")

def show_actions(room_data):
  action_number = 1
  for action in room_data[3]:
    print(str(action_number) + ". " + action[0])
    action_number += 1

def play_room(room_id, message_from_previous_room, isFirstRoom):
  room_data = extract_room_data(room_id)
  if room_data is None:
    show_error("Program error: Room " + room_id + " not found.  Aborting game.")
    exit()
  show_room(room_data, message_from_previous_room)
  user_prompts = ["What do you want to do?", "What's next?", "Now what?", "And now?"]
  promptIdx = random.randrange(0,len(user_prompts)) if not isFirstRoom else 0
  print(user_prompts[promptIdx] + new_line)
  show_actions(room_data)
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
        return ["player_quits",""]
      if choice == "h":
        print(new_line + colorize("green","regular","normal", room_data[4]))
        move_cursor("up",3)
        continue
      try:
        choice = int(choice)
        if choice < 1 or choice > len(room_data[3]):
          show_error("Please enter a number between 1 and " + str(len(room_data[3])) + ".")
          move_cursor("up",4)
        else:
          choice_made = True
      except:
        show_error("")
        move_cursor("up",4)
    action = room_data[3][choice-1]
    if action[2] != "":
      return [action[2], action[1]]
    if action[1] != "":
      print("")
      print(colorize("blue","regular","high", action[1]))
      move_cursor("up",3)

def executar(sala, mensagem_anterior="", primeira_sala=False):
  """Joga a sala ate o jogador sair dela; devolve [proxima_sala, mensagem]. Ponto de entrada publico desta unidade."""
  return play_room(sala, mensagem_anterior, primeira_sala)
