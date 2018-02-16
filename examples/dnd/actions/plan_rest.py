from examples.dnd.actions.plan import Plan
from examples.dnd.actions.rest import Rest

class PlanRest(Plan):
  def get_is_possible(character):
    return character.get('mp') < character.get('max_mp')

  def execute(self, diff):
    rest = Rest(parent=self.parent)
    self.parent.set('planned_action_id', rest.id)
