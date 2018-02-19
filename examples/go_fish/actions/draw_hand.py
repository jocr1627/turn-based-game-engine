from engine.action import Phases
from engine.listener import Listener
from examples.go_fish.actions.draw  import Draw

class DrawHand(Listener):
  def execute(self, diff):
    for i in range(5):
      draw = Draw(parent=self.parent)
      draw.resolve()

  def get_is_valid(self, diff):
    return (
      self.game.inspect('deck', lambda deck: len(deck) > 0)
      and self.parent.inspect('hand', lambda hand: len(hand) == 0)
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()
    
    return (
      (trigger.phase is Phases.EXECUTION and trigger.get_name() is 'StartGame')
      or diff.inspect_in(
        ['state', self.parent.id, 'hand'],
        lambda hand_diff: hand_diff is not None and len(hand_diff[1]) == 0
      )
    )
