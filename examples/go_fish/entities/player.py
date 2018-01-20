from engine.entity import Entity
from examples.go_fish.actions.draw_hand import DrawHand
from examples.go_fish.actions.end_turn import EndTurn
from examples.go_fish.actions.score import Score
from examples.go_fish.actions.start_turn import StartTurn

class Player(Entity):
  def get_default_children(self):
    return [
      DrawHand(),
      EndTurn(),
      Score(),
      StartTurn()
    ]

  def get_default_state(self):
    return { 'hand': [], 'score': 0 }
