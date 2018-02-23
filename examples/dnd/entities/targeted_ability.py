from examples.dnd.entities.ability import Ability

class TargetedAbility(Ability):
  def get_is_possible(self):
    return len(self.get_valid_target_ids()) > 0 and super().get_is_possible()

  def get_targets(self):
    return None

  def get_valid_target_ids(self):
    return []
