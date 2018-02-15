from engine.base_entity_listener import BaseEntityListener

class Interrupt(BaseEntityListener):
  def execute(self, diff):
    self.parent.set('has_taken_damage', True)

  def get_should_react(self, diff):
    hp_diff = diff.get_in(['state', self.parent.id, 'hp'])

    return (
      hp_diff is not None
      and hp_diff[1] < hp_diff[0]
    )
