
from engine.game import Game
from examples.dnd.actions.plan_phase import PlanPhase

class DnD(Game):
  def __init__(self, characters, locations):
    character_ids = set([character.id for character in characters])
    location_ids = set([location.id for location in locations])
    state = { 'character_ids': character_ids, 'location_ids': location_ids }
    super().__init__(children=locations, state=state)

  def end_round(self):
    if self.get('round_number') == 5:
      self.set('is_in_progress', False)

  def get_default_children(self):
    return [PlanPhase()]
