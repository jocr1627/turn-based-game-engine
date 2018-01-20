from engine.action import Action
from examples.go_fish.actions.draw import Draw
from examples.go_fish.actions.give import Give

class Respond(Action):
  def execute(self, diff):
    requested_rank = self.get('rank')
    request_class_name = self.get('request_class_name')
    requestor = self.hydrate('requestor_id')
    hand = self.parent.get('hand')
    matching_cards = [card for card in hand if card['rank'] == requested_rank]

    if len(matching_cards) > 0:
      give = Give(parent=self.parent, state={ 'card': matching_cards[0], 'target_id': requestor.id })
      give.resolve()
      request_class = self.root.entity_classes[request_class_name]
      request = request_class(parent=requestor)
      request.resolve()
    else:
      draw = Draw(parent=requestor)
      draw.resolve()
