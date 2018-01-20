from engine.action import Action
from examples.go_fish.actions.draw import Draw
from examples.go_fish.actions.give import Give

class Respond(Action):
  name = 'Respond'

  def execute(self, diff, options):
    requested_rank = self.get('rank')
    requestor_id = self.get('requestor_id')
    request_class = options['request_class']
    requestor = self.root.descendants[requestor_id]
    hand = self.parent.get('hand')
    matching_cards = [card for card in hand if card['rank'] == requested_rank]

    if len(matching_cards) > 0:
      give = Give(parent=self.parent, state={ 'card': matching_cards[0], 'target_id': requestor_id })
      give.resolve()
      request = request_class(parent=requestor)
      request.resolve()
    else:
      draw = Draw(parent=requestor)
      draw.resolve()
