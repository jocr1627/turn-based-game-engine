from engine.deep_merge import deep_merge
from engine.destroy_entity import DestroyEntity
from engine.listener import Listener

class DestroyDurationEffect(Listener):
  def execute(self, diff):
    destroy_entity = DestroyEntity(parent=self.game, state={ 'entity_id': self.parent.id })
    destroy_entity.resolve()

  def get_should_react(self, diff):
    starting_round_number = self.parent.get('starting_round_number')

    return self.game.get('round_number') == starting_round_number + 3

class DurationEffect(Listener):
  def get_default_children(self):
    return deep_merge(
      super().get_default_children(),
      [DestroyDurationEffect(trigger_types=['StartRound'])]
    )
