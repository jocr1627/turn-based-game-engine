from engine.action import Action

class Discard(Action):
  def execute(self, diff):
    card = self.get('card')
    self.parent.update('hand', lambda hand: hand.remove(card))

  def get_is_valid(self):
    card = self.get('card')

    return self.parent.inspect('hand', lambda hand: card in hand)
