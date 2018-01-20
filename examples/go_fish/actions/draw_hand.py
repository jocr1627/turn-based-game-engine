from engine.listener import Listener
from examples.go_fish.actions.draw  import Draw

class DrawHand(Listener):
  name = 'DrawHand'

  def execute(self, diff, options):
    for i in range(5):
      draw = Draw(parent=self.parent)
      draw.resolve()

  def get_is_valid(self, options):
    return (
      len(self.root.get('deck')) > 0
      and len(self.parent.get('hand')) == 0
    )

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      (not is_preparation and trigger_action.name is 'StartGame')
      or (
        diff.hasIn(['state', self.parent.id, 'hand'])
        and len(diff.getIn(['state', self.parent.id, 'hand'])[1]) == 0
      )
    )
