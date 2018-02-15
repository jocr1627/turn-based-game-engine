
from engine.game import Game
from examples.dnd.actions.end_round import EndRound
from examples.dnd.actions.plan_phase import PlanPhase
from examples.dnd.actions.resolve_phase import ResolvePhase
from examples.dnd.actions.start_round import StartRound

class DnD(Game):
  def __init__(self, characters, regions):
    character_ids = set([character.id for character in characters])
    region_ids = set([region.id for region in regions])
    state = { 'character_ids': character_ids, 'region_ids': region_ids }

    super().__init__(children=regions, state=state)

  def run(self):
    self.set('is_in_progress', True)
    self.set('round_number', 0)

    while self.get('is_in_progress'):
      start_round = StartRound(parent=self)
      start_round.resolve()
      plan_phase = PlanPhase(parent=self)
      plan_phase.resolve()
      resolve_phase = ResolvePhase(parent=self)
      resolve_phase.resolve()
      end_round = EndRound(parent=self)
      end_round.resolve()
