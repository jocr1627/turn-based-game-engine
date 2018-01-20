from engine.action import Action
from examples.go_fish.actions.respond import Respond

class Request(Action):
  def execute(self, diff):
    rank = self.get('rank')
    request_class_name = self.get('request_class_name')
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]
    respond_state = { 'rank': rank, 'request_class_name': request_class_name, 'requestor_id': self.parent.id }
    respond = Respond(parent=target, state=respond_state)
    respond.resolve()

  def get_is_valid(self):
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]

    return (
      self.parent.id is self.root.get('active_player_id')
      and target.inspect('hand', lambda hand: len(hand) > 0)
      and self.root.get('is_in_progress')
    )
