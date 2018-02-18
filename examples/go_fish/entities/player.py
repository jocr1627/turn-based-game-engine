from engine.deep_merge import deep_merge
from engine.entity import Entity
from examples.go_fish.actions.draw_hand import DrawHand
from examples.go_fish.actions.end_turn import EndTurn
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.actions.score import Score
from examples.go_fish.actions.start_turn import StartTurn

class Player(Entity):
  def get_default_children(self):
    return deep_merge(
      super().get_default_children(),
      [
        DrawHand(),
        EndTurn(),
        Score(),
        StartTurn(),
        self.get_request_class()(),
      ]
    )

  def get_default_state(self):
    return { 'hand': [], 'score': 0 }

  def get_request_class(self):
    return MaxValueRequest
