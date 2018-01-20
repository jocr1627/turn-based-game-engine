from engine.action import Action

class Draw(Action):
  def execute(self, diff):
    card = self.root.getIn(['deck', -1])
    self.root.mutate('deck', lambda deck: deck.pop())
    self.parent.mutate('hand', lambda hand: hand.append(card))

  def get_is_valid(self):
    return self.root.inspect('deck', lambda deck: len(deck) > 0)
