"""Aventura de texto: uma sala do jogo, com descricao, acoes e dica.

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

import time
import random

new_line = "\r\n"

def _action(name, message, new_room):
  return [name, message, new_room]

def basement_dark():
  return ["basement_dark", "basement storage room",
    "You're not sure how you got here. It is quite dark and there's water dripping in the distance.   \n"
    "There's a door to your left and a door to your right.  There's also a chest in the corner with a  \n"
    "strange hum coming from it.",
    [_action("Open the left door", "The left door is locked.", ""),
    _action("Open the right door", "The right door is locked.", ""),
    _action("Open the chest", "The chest is locked.", ""),
    _action("Flick the light switch on the wall", "The lights are now on.", "basement_light")],
    "Any option is safe."]

def upstairs_unlocked():
  return ["upstairs_unlocked", "Upstairs Living Room", "",
    [_action("Open the front door", "", "player_wins"),
    _action("Check out the grandfather clock", "The clock appears to be broken.", ""),
    _action("Open the closet", closet_action, "player_dies"),
    _action("Go back downstairs", "You make your way back down the spiral stair case.", "basement_library_3"),
    _action("Play the piano", piano_action, "")],
    "A click by the front door?  You're almost there.  Only one thing left to do!"]

room_data = [basement_dark(), upstairs_unlocked()]

# Restante do código...
