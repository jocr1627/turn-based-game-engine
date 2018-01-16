from copy import deepcopy
from engine.action import Action

class Draw(Action):
  name = 'Draw'

  def execute(self):
    card = self.game.state['deck'].pop()
    hand = self.entity.state['hand']
    previous_hand = deepcopy(hand)
    hand.append(card)

    return { self.entity.id: { 'hand': (previous_hand, hand) } }

  def get_is_valid(self):
    return len(self.game.state['deck']) > 0
