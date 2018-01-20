from engine.action import Action

class Give(Action):
  def execute(self, diff):
    card = self.get('card')
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]
    giver_hand = self.parent.update('hand', lambda hand: hand.remove(card))
    target_hand = target.update('hand', lambda hand: hand.append(card))
