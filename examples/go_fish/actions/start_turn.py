from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener

class StartTurn(BaseEntityListener):
  def execute(self, diff):
    self.game.set('active_player_id', self.parent.id)

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return trigger.phase is Phases.EXECUTION and trigger.get_name() is 'StartRound'
