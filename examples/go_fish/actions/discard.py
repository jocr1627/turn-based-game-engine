from engine.action import Action

class Discard(Action):
  name = 'Discard'

  def execute(self, diff, options):
    card = self.get('card')
    hand = self.parent.get('hand')
    hand.remove(card)
    self.parent.set('hand', hand)

  def get_is_valid(self, options):
    return self.get('card') in self.parent.get('hand')
