from engine.action import Action
from examples.dnd.entities.ability import Ability
from examples.dnd.priorities import Priorities

class PrepareEquip(Action):
  def execute(self, diff):
    name = self.parent.parent.get('name')
    inventory = self.parent.parent.hydrate('inventory')
    inventory_weapons = [item for item in inventory if isinstance(item, Weapon)]
    location_weapons = []

    for child in self.parent.parent.parent.children.values():
      if isinstance(child, Weapon):
        location_weapons.append(child)

    inventory_weapon_names = [weapon.get('name').lower() for weapon in inventory_weapons]
    location_weapon_names = [weapon.get('name').lower() for weapon in location_weapons]
    possible_weapons = []

    while len(possible_weapons) == 0:
      weapon_name = input(f'Enter the name of weapon {name} would like to equip: ')

      if weapon_name in inventory_weapon_names:
        possible_weapons += [weapon for weapon in inventory_weapons if weapon.get('name').lower() == weapon_name]
      if weapon_name in location_weapon_names:
        possible_weapons += [weapon for weapon in location_weapons if weapon.get('name').lower() == weapon_name]
      
      if len(possible_weapons) == 0:
        print(f'No weapons matched the name {weapon_name}. Options include: {inventory_weapon_names} in {name}\'s inventory and {location_weapon_names} in the nearby area. Try again.')

    weapon = None
    
    if len(possible_weapons) == 1:
      weapon = possible_weapons[0]
    else:
      possible_weapons_by_id = { weapon.id: weapon for weapon in possible_weapons }
      possible_weapon_descriptions = [(weapon.id, weapon.parent.get('name')) for weapon in possible_weapons]

      while weapon is None:
        weapon_id = input(f'Multiple weapons have the name {weapon_name}. Options include: {possible_weapon_descriptions} Enter the id of the desired weapon: ')
        
        try:
          weapon_id = int(weapon_id)

          if weapon_id in possible_weapons_by_id:
            weapon = possible_weapons_by_id[weapon_id]
          else:
            print(f'{weapon_id} does not match any known weapons.')
        except ValueError:
          print(f'{weapon_id} is not a valid id. Try again.')

    resolve_args = { 'weapon_id', weapon.id }
    self.parent.set('resolve_args', resolve_args)

class ResolveEquip(Action):
  def execute(self, diff):
    name = self.parent.parent.get('name')
    weapon = self.hydrate('weapon_id')
    weapon_id = weapon.id if weapon is not None else None
    weapon_name = weapon.get('name') if weapon is not None else 'nothing'
    self.parent.parent.set('weapon_id', weapon_id)
    print(f'{name} equipped {weapon_name}.')

  def get_is_valid(self, diff):
    return self.parent.parent.get('is_alive')

class Equip(Ability):
  matcher = r'^equip$'

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def prepare(self):
    prepare_equip = PrepareEquip(parent=self)
    prepare_equip.resolve()

  def resolve(self):
    resolve_equip = ResolveEquip(parent=self, state={ 'resolve_args': self.get('resolve_args') })
    resolve_equip.resolve()
