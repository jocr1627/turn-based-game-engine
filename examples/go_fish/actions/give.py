from engine.action import Action

class Give(Action):
  name = 'Give'

  def execute(self, diff, options):
    card = self.get('card')
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]
    giver_hand = self.parent.mutate('hand', lambda hand: hand.remove(card))
    target_hand = target.mutate('hand', lambda hand: hand.append(card))
