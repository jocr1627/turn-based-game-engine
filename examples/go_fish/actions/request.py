from engine.action import Action
from examples.go_fish.actions.respond import Respond

class Request(Action):
  name = 'Request'

  def execute(self, diff, options):
    rank = self.get('rank')
    target_id = self.get('target_id')
    request_class = options['request_class']
    target = self.root.descendants[target_id]
    respond = Respond(parent=target, state={ 'rank': rank, 'requestor_id': self.parent.id })
    respond.resolve(options={'request_class': request_class})
  
  def get_is_cycle(self):
    return False

  def get_is_valid(self, options):
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]

    return (
      self.parent.id is self.root.get('active_player_id')
      and target.inspect('hand', lambda hand: len(hand) > 0)
      and self.root.get('is_in_progress')
    )
