from engine.action import Action

class Draw(Action):
  name = 'Draw'

  def execute(self):
    deck = self.game.state.get('deck')
    card = deck.pop()
    diffs = self.game.state.set('deck', deck)
    hand = self.entity.state.get('hand')
    hand.append(card)

    return self.entity.state.set('hand', hand, diffs)

  def get_is_valid(self):
    return len(self.game.state.get('deck')) > 0
