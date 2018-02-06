from engine.listener import Listener

class UpdateCriticalChanceByGuile(Listener):
  def execute(self, diff):
    guile,new_guile = diff.get_in(['state', self.parent.id, 'attributes', 'guile'])
    difference = new_guile - guile
    self.parent.update('critical_chance', lambda critical_chance: min(max(critical_chance + 0.05 * difference, 0), 1))

  def get_should_react(self, diff):
    return diff.has_in(['state', self.parent.id, 'attributes', 'guile'])
