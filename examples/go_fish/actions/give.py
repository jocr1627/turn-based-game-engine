from engine.action import Action

class Give(Action):
  name = 'Give'

  def execute(self):
    card = self.options['card']
    target = self.options['target']
    giver_hand = self.entity.state.get('hand')
    giver_hand.remove(card)
    diffs = self.entity.state.set('hand', giver_hand)
    target_hand = target.state.get('hand')
    target_hand.append(card)

    return target.state.set('hand', target_hand, diffs)
