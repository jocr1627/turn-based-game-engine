from engine.base_entity_listener import BaseEntityListener

class UpdateMaxHpByConstitution(BaseEntityListener):
  def execute(self, diff):
    constitution,new_constitution = diff.get_in(['state', self.parent.id, 'attributes', 'constitution'])
    difference = new_constitution - constitution
    self.parent.update('max_hp', lambda max_hp: max(max_hp + 5 * difference, 1))

  def get_should_react(self, diff):
    return diff.has_in(['state', self.parent.id, 'attributes', 'constitution'])
