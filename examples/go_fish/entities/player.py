from engine.entity import Entity
from examples.go_fish.actions.draw_hand import DrawHand
from examples.go_fish.actions.end_turn import EndTurn
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.actions.score import Score
from examples.go_fish.actions.start_turn import StartTurn

class Player(Entity):
  def get_default_reactions(self):
    return [
      MaxValueRequest,
      EndTurn,
      StartTurn
    ]

  def get_default_state(self):
    return { 'hand': [], 'is_player': True, 'score': 0 }
  
  def update(self, game, diffs):
    drawHand = DrawHand(game, self)
    drawHand.resolve()
    score = Score(game, self)
    score.resolve()
