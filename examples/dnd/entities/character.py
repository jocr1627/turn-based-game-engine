from engine.entity import Entity
from examples.dnd.actions.plan_attack import PlanAttack
from examples.dnd.actions.plan_turn import PlanTurn
from examples.dnd.actions.take_turn import TakeTurn
from examples.dnd.entities.weapons.fists import Fists
from examples.dnd.utils.roll import roll

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
    default_weapon=Fists(),
    inventory=[],
    is_health_based=True,
    level=1,
    location=None,
    max_hp=None,
    weapon=None
  ):
    children = inventory + [default_weapon]

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
      'default_weapon_id': default_weapon.id,
      'hp': max_hp,
      'inventory': [item.id for item in inventory],
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
  
  def get_default_getters(self):
    return {
      'plan_action_class_name': self.get_plan_action_class_name,
      'roll': self.get_roll,
    }
  
  def get_default_state(self):
    return {
      'abilities': [
        'PlanAdvance',
        'PlanAttack',
        'PlanEquip',
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
      'default_weapon_id': None,
      'hp': 1,
      'inventory': [],
      'level': 1,
      'max_hp': 1,
      'name': self.get_name(),
      'planned_action_id': None,
      'weapon_id': None
    }
  
  def get_plan_action_class_name(self, args):
    return 'PlanAttack'

  def get_roll(self, args):
    return roll()

  def get_weapon(self):
    return self.hydrate('weapon_id') if self.get('weapon_id') is not None else self.hydrate('default_weapon_id')
