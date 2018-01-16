from engine.action import Action

class CharacterAction(Action):
  name = 'CharacterAction'

  def get_priority(self):
    return self.entity.state['initiative']
