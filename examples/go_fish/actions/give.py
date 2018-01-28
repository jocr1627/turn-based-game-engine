from engine.action import Action

class Give(Action):
  def execute(self, diff):
    card = self.get('card')
    target = self.hydrate('target_id')
    giver_hand = self.parent.mutate('hand', lambda hand: hand.remove(card))
    target_hand = target.mutate('hand', lambda hand: hand.append(card))
