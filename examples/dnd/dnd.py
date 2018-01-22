
from engine.action import Action
from engine.entity import Entity
from engine.game import Game
from examples.dnd.actions.plan_advance import PlanAdvance
from examples.dnd.actions.plan_attack import PlanAttack
from examples.dnd.actions.plan_flee import PlanFlee
from examples.dnd.actions.plan_move import PlanMove

entity_class_list = [
  PlanAdvance,
  PlanAttack,
  PlanFlee,
  PlanMove
]
entity_classes = { clazz.get_name(): clazz for clazz in entity_class_list }

class DnD(Game):
  def __init__(self, characters, locations):
    character_ids = set([character.id for character in characters])
    location_ids = set([location.id for location in locations])
    state = { 'character_ids': character_ids, 'location_ids': location_ids }
    super().__init__(children=locations, entity_classes=entity_classes, state=state)

  def end_round(self):
    if self.get('round_number') == 2:
      self.set('is_in_progress', False)
