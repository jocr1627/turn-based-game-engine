from engine.action import Action

class Draw(Action):
  name = 'Draw'

  def execute(self, diff, options):
    deck = self.root.get('deck')
    card = deck.pop()
    self.root.set('deck', deck)
    hand = self.parent.get('hand')
    hand.append(card)
    self.parent.set('hand', hand)

  def get_is_valid(self, options):
    return len(self.root.get('deck')) > 0
