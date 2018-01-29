from engine.entity import Entity
from examples.dnd.actions.plan_attack import PlanAttack
from examples.dnd.actions.plan_turn import PlanTurn
from examples.dnd.actions.set_target_character import SetTargetCharacter
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
    guile = attributes['guile'] if 'guile' in attributes else 0
    max_hp = max_hp if max_hp is not None else get_max_hp(level, constitution, is_health_based)
    weapon_id = weapon.id if weapon is not None else None
    state = {
      'abilities': abilities,
      'armor_id': armor_id,
      'attributes': attributes,
      'critical_chance': min(0.05 * (1 + guile), 1),
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
      SetTargetCharacter(),
      TakeTurn(),
    ]
  
  def get_default_getters(self):
    return {
      'is_critical': self.get_is_critical,
      'is_flanking': self.get_is_flanking,
      'plan_action_class_name': self.get_plan_action_class_name,
      'roll': self.get_roll,
      'target_character_ids': self.get_target_character_ids,
      'target_location_ids': self.get_target_location_ids,
      'weapon_attack_bonus': self.get_weapon_attack_bonus,
      'weapon_damage': self.get_weapon_damage
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
      'critical_chance': 0.05,
      'default_weapon_id': None,
      'hp': 1,
      'inventory': [],
      'level': 1,
      'max_hp': 1,
      'name': self.get_name(),
      'planned_action_id': None,
      'target_character_id': None,
      'weapon_id': None
    }
  
  def get_is_critical(self, args):
    critical_chance = self.get('critical_chance')
    roll = args['roll']

    return round(1 - roll / 20, 2) < critical_chance
  
  def get_is_flanking(self, args):
    target_character_id = args['target_character_id']
    target_character = self.hydrate_by_id(target_character_id)
    target_id_of_target = target_character.get('target_character_id')

    return target_id_of_target is not self.id
  
  def get_plan_action_class_name(self, args):
    return 'PlanAttack'

  def get_roll(self, args):
    dice = args['dice'] if dice in 'args' else None
  
    return roll(dice)

  def get_target_character_ids(self, args):
    return args['valid_ids'][0:args['num_targets']]

  def get_target_location_ids(self, args):
    return args['valid_ids'][0:args['num_targets']]

  def get_weapon(self):
    return self.hydrate('weapon_id') if self.get('weapon_id') is not None else self.hydrate('default_weapon_id')

  def get_weapon_attack_bonus(self, args):
    weapon = self.get_weapon()
    weapon_attribute_caps = weapon.get('attribute_caps')
    attributes = self.get('attributes')
    weapon_attack_bonus = weapon.get('attack_modifier')

    for attribute,cap in weapon_attribute_caps.items():
      attribute_score = attributes[attribute]
      weapon_attack_bonus += min(attribute_score, cap) if cap is not None else attribute_score

    return weapon_attack_bonus

  def get_weapon_damage(self, args):
    weapon = self.get_weapon()
    damage_modifier = weapon.get('damage_modifier')
    args['dice'] = weapon.get('dice')
    args['roll_type'] = 'damage'
    damage = self.get_roll(args) + damage_modifier

    if args['is_critical']
      damage *= 2

    return damage
