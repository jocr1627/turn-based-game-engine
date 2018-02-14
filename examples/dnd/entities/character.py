import random
from engine.entity import Entity
from engine.request import request
from examples.dnd.actions.set_target_character import SetTargetCharacter
from examples.dnd.actions.take_turn import TakeTurn
from examples.dnd.actions.update_critical_chance_by_guile import UpdateCriticalChanceByGuile
from examples.dnd.actions.update_max_hp_by_constitution import UpdateMaxHpByConstitution
from examples.dnd.actions.update_max_mp_by_willpower import UpdateMaxMpByWillpower
from examples.dnd.entities.weapons.fists import Fists
from examples.dnd.utils.roll import roll

def get_max_hp(level, constitution, is_health_based):
  base_health = 20 if is_health_based else 10
  
  return base_health + 2 * level + 5 * constitution

def get_max_mp(willpower, is_health_based):
  base_mana = 4 if is_health_based else 6

  return base_mana + willpower

class Character(Entity):
  def __init__(
    self,
    name,
    abilities={},
    armor=None,
    attributes={},
    default_weapon=Fists(),
    inventory=[],
    is_health_based=True,
    level=1,
    location=None,
    max_hp=None,
    max_mp=None,
    passive_abilities=[],
    weapon=None
  ):
    children = inventory + passive_abilities + [default_weapon]

    if armor is not None:
      children.append(armor)
    if weapon is not None:
      children.append(weapon)

    armor_id = armor.id if armor is not None else None
    constitution = attributes['constitution'] if 'constitution' in attributes else 0
    guile = attributes['guile'] if 'guile' in attributes else 0
    max_hp = max_hp if max_hp is not None else get_max_hp(level, constitution, is_health_based)
    willpower = attributes['willpower'] if 'willpower' in attributes else 0
    max_mp = max_mp if max_mp is not None else get_max_mp(willpower, is_health_based)
    passive_ability_ids = [ability.id for ability in passive_abilities]
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
      'max_mp': max_mp,
      'mp': max_mp,
      'name': name,
      'passive_ability_ids': passive_ability_ids,
      'weapon_id': weapon_id
    }

    super().__init__(children=children, parent=location, state=state)

  def get_default_children(self):
    return [
      UpdateCriticalChanceByGuile(),
      UpdateMaxHpByConstitution(),
      UpdateMaxMpByWillpower(),
      SetTargetCharacter(),
      TakeTurn(),
    ]
  
  def get_default_getters(self):
    return {
      'critical_factor': self.get_critical_factor,
      'is_critical': self.get_is_critical,
      'is_flanking': self.get_is_flanking,
      'plan_action_class_name': self.get_plan_action_class_name,
      'physical_defense_modifier': self.get_physical_defense_modifier,
      'roll': self.get_roll,
      'target_character_ids': self.get_target_character_ids,
      'target_location_ids': self.get_target_location_ids,
      'weapon_attack_modifier': self.get_weapon_attack_modifier,
      'weapon_damage': self.get_weapon_damage
    }
  
  def get_default_state(self):
    return {
      'abilities': {
        'PlanAdvance': {},
        'PlanAttack': {},
        'PlanEquip': {},
        'PlanFlee': {},
        'PlanMove': {},
        'PlanRest': {},
      },
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
      'max_mp': 0,
      'mp': 0,
      'name': self.get_name(),
      'passive_ability_ids': [],
      'planned_action_id': None,
      'target_character_id': None,
      'weapon_id': None
    }

  def get_critical_factor(self, args):
    return 2
  
  def get_is_critical(self, args):
    critical_chance = self.get('critical_chance')
    base_roll = args['base_roll']

    return round(1 - base_roll / 20, 2) < critical_chance
  
  def get_is_flanking(self, args):
    target_character_id = args['target_character_id']
    target_character = self.hydrate_by_id(target_character_id)
    target_id_of_target = target_character.get('target_character_id')

    return target_id_of_target is not self.id
  
  def get_plan_action_class_name(self, args):
    if self.get('mp') == 0:
      return 'PlanRest'
    
    abilities = self.get('abilities')

    return random.choice(list(abilities.keys()))

  def get_physical_defense_modifier(self, args):
    armor = self.hydrate('armor_id')
    dexterity_cap = armor.get('dexterity_cap')
    dexterity = self.get_in(['attributes', 'dexterity'])
    
    return armor.get('modifier') + min(dexterity, dexterity_cap)

  def get_roll(self, args):  
    roll_result = roll(args['dice']) if 'dice' in args else roll()

    return (roll_result, roll_result)

  def get_target_character_ids(self, args):
    return args['valid_ids'][0:args['num_targets']]

  def get_target_location_ids(self, args):
    return args['valid_ids'][0:args['num_targets']]

  def get_weapon(self):
    return self.hydrate('weapon_id') if self.get('weapon_id') is not None else self.hydrate('default_weapon_id')

  def get_weapon_attack_modifier(self, args):
    weapon_id = args['weapon_id']
    weapon = self.hydrate_by_id(weapon_id)
    weapon_attribute_caps = weapon.get('attribute_caps')
    attributes = self.get('attributes')
    weapon_attack_modifier = weapon.get('attack_modifier')

    for attribute,cap in weapon_attribute_caps.items():
      attribute_score = attributes[attribute]
      weapon_attack_modifier += min(attribute_score, cap) if cap is not None else attribute_score

    return weapon_attack_modifier

  def get_weapon_damage(self, args):
    weapon_id = args['weapon_id']
    weapon = self.hydrate_by_id(weapon_id)
    damage_modifier = weapon.get('damage_modifier')
    damage = (args['roll'] + damage_modifier)
    
    if args['is_critical']:
      damage *= args['critical_factor']

    return round(damage)
