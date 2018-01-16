from copy import deepcopy
from engine.action import Action

class Discard(Action):
  name = 'Discard'

  def execute(self):
    hand = self.entity.state['hand']
    previous_hand = deepcopy(hand)
    hand.remove(self.options['card'])

    return { self.entity.id: { 'hand': (previous_hand, hand) } }

  def get_is_valid(self):
    return self.options['card'] in self.entity.state['hand']
