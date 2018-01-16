from engine.action import Action

class Give(Action):
  name = 'Give'

  def execute(self):
    card = self.options['card']
    target = self.options['target']
    self.entity.state['hand'].remove(card)
    target.state['hand'].append(card)

    return {
      self.entity.id: { 'hand': () },
      target.id: { 'hand': () }
    }
