from engine.action import Action
from examples.go_fish.actions.respond import Respond

class Request(Action):
  name = 'Request'

  def execute(self):
    rank = self.options['rank']
    request_class = self.options['request_class']
    target = self.options['target']
    respond = Respond(self.game, target, { 'rank': rank, 'request_class': request_class, 'requestor': self.entity })
    respond.resolve()

    return {}
  
  def get_is_cycle(self):
    return False

  def get_is_valid(self):
    return (
      self.entity is self.game.state['active_player']
      and len(self.options['target'].state['hand']) > 0
      and self.game.state['is_in_progress']
    )
