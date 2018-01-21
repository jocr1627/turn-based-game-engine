from engine.entity import Entity
from examples.go_fish.actions.user_input_request import UserInputRequest
from examples.go_fish.entities.player import Player

class HumanPlayer(Player):
  def __init__(self):
    super().__init__([UserInputRequest()])
