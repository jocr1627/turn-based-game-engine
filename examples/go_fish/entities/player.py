from engine.entity import Entity
from examples.go_fish.actions.draw_hand import DrawHand
from examples.go_fish.actions.end_turn import EndTurn
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.actions.score import Score
from examples.go_fish.actions.start_turn import StartTurn

class Player(Entity):
  def get_default_reactions(self, game):
    return [
      MaxValueRequest,
      EndTurn,
      StartTurn
    ]

  def get_default_state(self, game):
    return { 'hand': [], 'is_player': True, 'score': 0 }
  
  def update(self, diffs):
    drawHand = DrawHand(self.game, self)
    drawHand.resolve()
    score = Score(self.game, self)
    score.resolve()
