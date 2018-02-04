from examples.go_fish.actions.user_input_request import UserInputRequest
from examples.go_fish.entities.player import Player

class HumanPlayer(Player):
  def get_request_class(self):
    return UserInputRequest
