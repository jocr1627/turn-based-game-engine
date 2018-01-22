from engine.entity import Entity
from examples.dnd.actions.plan_turn import PlanTurn
from examples.dnd.actions.take_turn import TakeTurn

def get_max_hp(level, constitution, is_health_based):
  base_health = 20 if is_health_based else 10
  
  return base_health + 2 * level + 5 * constitution

class Character(Entity):
  def __init__(
    self,
    name,
    abilities=[],
    armor=None,
    attributes={},
    is_health_based=True,
    level=1,
    location=None,
    max_hp=None,
    weapon=None
  ):
    children = []
    
    if armor is not None:
      children.append(armor)
  
    if weapon is not None:
      children.append(weapon)

    armor_id = armor.id if armor is not None else None
    constitution = attributes['constitution'] if 'constitution' in attributes else 0
    max_hp = max_hp if max_hp is not None else get_max_hp(level, constitution, is_health_based)
    weapon_id = weapon.id if weapon is not None else None
    state = {
      'abilities': abilities,
      'armor_id': armor_id,
      'attributes': attributes,
      'hp': max_hp,
      'level': level,
      'max_hp': max_hp,
      'name': name,
      'weapon_id': weapon_id
    }
    super().__init__(children=children, parent=location, state=state)

  def get_default_children(self):
    return [
      PlanTurn(),
      TakeTurn(),
    ]
  
  def get_default_state(self):
    return {
      'abilities': [
        'PlanAdvance',
        'PlanAttack',
        'PlanFlee',
        'PlanMove'
      ],
      'armor_id': None,
      'attributes': {
        'charisma': 0,
        'constitution': 0,
        'dexterity': 0,
        'guile': 0,
        'intellect': 0,
        'spirit': 0,
        'strength': 0,
        'willpower': 0
      },
      'hp': 1,
      'level': 1,
      'max_hp': 1,
      'name': self.get_name(),
      'planned_action_id': None,
      'weapon_id': None
    }
