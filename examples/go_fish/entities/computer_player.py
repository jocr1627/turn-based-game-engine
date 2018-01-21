from engine.entity import Entity
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.entities.player import Player

class ComputerPlayer(Player):
  def __init__(self):
    super().__init__([MaxValueRequest()])
