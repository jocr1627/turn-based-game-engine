from engine.action import Action
from examples.go_fish.actions.draw  import Draw

class DrawHand(Action):
  name = 'DrawHand'

  def execute(self):
    for i in range(5):
      draw = Draw(self.game, self.entity)
      draw.resolve()
    
    return {}

  def get_is_valid(self):
    return (
      len(self.game.state.get('deck')) > 0
      and len(self.entity.state.get('hand')) == 0
    )
