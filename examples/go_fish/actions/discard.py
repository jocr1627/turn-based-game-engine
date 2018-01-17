from engine.action import Action

class Discard(Action):
  name = 'Discard'

  def execute(self):
    card = self.options['card']
    hand = self.entity.state.get('hand')
    hand.remove(card)

    return self.entity.state.set('hand', hand)

  def get_is_valid(self):
    return self.options['card'] in self.entity.state.get('hand')
