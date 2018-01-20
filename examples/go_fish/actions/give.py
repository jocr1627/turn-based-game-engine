from engine.action import Action

class Give(Action):
  name = 'Give'

  def execute(self, diff, options):
    card = self.get('card')
    target_id = self.get('target_id')
    target = self.root.descendants[target_id]
    giver_hand = self.parent.get('hand')
    giver_hand.remove(card)
    self.parent.set('hand', giver_hand)
    target_hand = target.get('hand')
    target_hand.append(card)
    target.set('hand', target_hand)
