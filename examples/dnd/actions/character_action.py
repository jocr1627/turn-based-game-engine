from engine.action import Action

class CharacterAction(Action):
  def get_priority(self):
    return self.entity.state.get('initiative')
