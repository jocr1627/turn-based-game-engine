from engine.action import Phases
from engine.destroy_entity import DestroyEntity
from engine.listener import Listener

class DestroyDurationEffect(DestroyEntity):
  def get_should_react(self, diff):
    starting_round_number = self.get('starting_round_number')

    return self.game.get('round_number') == starting_round_number + 3

class DurationEffect(Listener):
  def get_default_children(self):
    return deep_merge(
      super().get_default_children(),
      [DestroyDurationEffect(trigger_types=[('StartRound', Phases.EXECUTION)])]
    )
