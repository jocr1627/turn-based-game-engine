
from engine.action import Action
from engine.entity import Entity
from engine.game import Game
from examples.dnd.actions.plan_impotent_rage import PlanImpotentRage
from examples.dnd.actions.plan_whistle import PlanWhistle

entity_classes = {
  PlanImpotentRage.get_name(): PlanImpotentRage,
  PlanWhistle.get_name(): PlanWhistle
}

class DnD(Game):
  def __init__(self, characters):
    character_ids = [character.id for character in characters]
    state = { 'character_ids': character_ids }
    super().__init__(children=characters, entity_classes=entity_classes, state=state)

  def end_round(self):
    if self.get('round_number') == 2:
      self.set('is_in_progress', False)
