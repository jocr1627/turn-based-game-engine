from itertools import groupby
import random
from engine.request import request
from examples.dnd.actions.clear_interrupt import ClearInterrupt
from examples.dnd.actions.enforce_rest import EnforceRest
from examples.dnd.actions.interrupt import Interrupt
from examples.dnd.actions.set_target_character import SetTargetCharacter
from examples.dnd.actions.update_critical_chance_by_guile import UpdateCriticalChanceByGuile
from examples.dnd.actions.update_max_hp_by_constitution import UpdateMaxHpByConstitution
from examples.dnd.actions.update_max_mp_by_willpower import UpdateMaxMpByWillpower
from examples.dnd.entities.ability import Ability
from examples.dnd.entities.advance import Advance
from examples.dnd.entities.attack import Attack
from examples.dnd.entities.base_character import BaseCharacter
from examples.dnd.entities.equip import Equip
from examples.dnd.entities.flee import Flee
from examples.dnd.entities.idle import Idle
from examples.dnd.entities.move import Move
from examples.dnd.entities.rest import Rest
from examples.dnd.entities.weapons.fists import Fists
from examples.dnd.utils.roll import roll

def get_max_hp(level, constitution, is_health_based):
  base_health = 20 if is_health_based else 10
  
  return base_health + 2 * level + 5 * constitution

def get_max_mp(willpower, is_health_based):
  base_mana = 4 if is_health_based else 6

  return base_mana + willpower

class Character(BaseCharacter):
  parent_alias = 'location'

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
    max_mp=None,
    weapon=None
  ):
    abilities = self.get_default_abilities() + abilities
    abilities_map = {}

    for ability_name,abilities in groupby(abilities, key=lambda ability: ability.get_name()):
      abilities = list(abilities)

      if len(abilities) > 1:
        print(f'Warning: More than 1 {ability_name} ability was specified. Defaulting to last value.')
  
      abilities_map[ability_name] = abilities[-1]

    children = list(abilities_map.values()) + inventory  + [default_weapon]
    ability_ids_map = {
      ability_name: ability.id for ability_name,ability in abilities_map.items()
      if isinstance(ability, Ability)
    }
    passive_ability_ids_map = {
      ability_name: ability.id for ability_name,ability in abilities_map.items()
      if not isinstance(ability, Ability)
    }

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
    weapon_id = weapon.id if weapon is not None else None
    state = {
      'abilities': ability_ids_map,
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
      'passive_abilities': passive_ability_ids_map,
      'weapon_id': weapon_id
    }

    super().__init__(children=children, parent=location, state=state)

  def get_default_abilities(self):
    return [
      Advance(),
      Attack(),
      Equip(),
      Flee(),
      Idle(),
      Move(),
      Rest()
    ]

  def get_default_children(self):
    return [
      ClearInterrupt(),
      EnforceRest(),
      Interrupt(),
      UpdateCriticalChanceByGuile(),
      UpdateMaxHpByConstitution(),
      UpdateMaxMpByWillpower(),
      SetTargetCharacter()
    ]
  
  def get_default_getters(self):
    return {
      'ability_id': self.get_ability_id,
      'critical_factor': self.get_critical_factor,
      'is_critical': self.get_is_critical,
      'is_flanking': self.get_is_flanking,
      'physical_defense_modifier': self.get_physical_defense_modifier,
      'roll': self.get_roll,
      'target_character_ids': self.get_target_character_ids,
      'target_location_ids': self.get_target_location_ids,
      'weapon_attack_modifier': self.get_weapon_attack_modifier,
      'weapon_damage': self.get_weapon_damage
    }
  
  def get_default_state(self):
    return {
      'abilities': {},
      'active_ability_id': None,
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
      'is_alive': True,
      'level': 1,
      'max_hp': 1,
      'max_mp': 0,
      'mp': 0,
      'name': self.get_name(),
      'passive_abilities': {},
      'target_character_id': None,
      'weapon_id': None
    }

  def get_ability_id(self, args):
    ability_ids = [
      ability.id for ability in self.hydrate('abilities').values()
      if ability.get_is_possible(self)
    ]

    return random.choice(ability_ids)

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
    weapon = self.get_weapon()
    weapon_attribute_caps = weapon.get('attribute_caps')
    attributes = self.get('attributes')
    weapon_attack_modifier = weapon.get('attack_modifier')

    for attribute,cap in weapon_attribute_caps.items():
      attribute_score = attributes[attribute]
      weapon_attack_modifier += min(attribute_score, cap) if cap is not None else attribute_score

    return weapon_attack_modifier

  def get_weapon_damage(self, args):
    weapon = self.get_weapon()
    damage_modifier = weapon.get('damage_modifier')
    damage = (args['roll'] + damage_modifier)
    
    if args['is_critical']:
      damage *= args['critical_factor']

    return round(damage)

  def validate_parent(self, parent):
    if not parent.is_type('Location'):
      raise ValueError(f'Invalid parent for {self.__class__.__name__}. Expected Location but got {parent.__class__.__name__}.')
