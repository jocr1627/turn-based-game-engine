from engine.action import Action

class Draw(Action):
  def execute(self, diff):
    card = self.game.get_in(['deck', -1])
    self.game.mutate('deck', lambda deck: deck.pop())
    self.parent.mutate('hand', lambda hand: hand.append(card))

  def get_is_valid(self, diff):
    return self.game.inspect('deck', lambda deck: len(deck) > 0)
