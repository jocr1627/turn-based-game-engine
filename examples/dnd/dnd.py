
from engine.game import Game
from examples.dnd.actions.plan_phase import PlanPhase

class DnD(Game):
  def __init__(self, characters, regions):
    character_ids = set([character.id for character in characters])
    region_ids = set([region.id for region in regions])
    state = { 'character_ids': character_ids, 'region_ids': region_ids }

    super().__init__(children=regions, state=state)

  def end_round(self):
    if self.get('round_number') == 5:
      self.set('is_in_progress', False)

  def get_default_children(self):
    return [PlanPhase()]
