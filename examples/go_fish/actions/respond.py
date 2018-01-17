from engine.action import Action
from examples.go_fish.actions.draw import Draw
from examples.go_fish.actions.give import Give

class Respond(Action):
  name = 'Respond'

  def execute(self):
    requested_rank = self.options['rank']
    request_class = self.options['request_class']
    requestor = self.options['requestor']
    hand = self.entity.state.get('hand')
    matching_cards = [card for card in hand if card['rank'] == requested_rank]

    if len(matching_cards) > 0:
      give = Give(self.game, self.entity, { 'card': matching_cards[0], 'target': requestor })
      give.resolve()
      request = request_class(self.game, requestor)
      request.resolve()
    else:
      draw = Draw(self.game, requestor)
      draw.resolve()
    
    return {}
