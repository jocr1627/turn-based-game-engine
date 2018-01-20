from engine.action import Action

class Discard(Action):
  name = 'Discard'

  def execute(self, diff, options):
    card = self.get('card')
    self.parent.mutate('hand', lambda hand: hand.remove(card))

  def get_is_valid(self, options):
    card = self.get('card')

    return self.parent.inspect('hand', lambda hand: card in hand)
