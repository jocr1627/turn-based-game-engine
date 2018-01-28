from engine.listener import Listener
from examples.go_fish.actions.draw  import Draw

class DrawHand(Listener):
  def execute(self, diff):
    for i in range(5):
      draw = Draw(parent=self.parent)
      draw.resolve()

  def get_is_valid(self):
    return (
      self.root.inspect('deck', lambda deck: len(deck) > 0)
      and self.parent.inspect('hand', lambda hand: len(hand) == 0)
    )

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      (not is_preparation and trigger_action.get_name() is 'StartGame')
      or diff.inspect_in(
        ['state', self.parent.id, 'hand'],
        lambda hand_diff: hand_diff is not None and len(hand_diff[1]) == 0
      )
    )
