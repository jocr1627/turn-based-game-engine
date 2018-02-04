from engine.action import Action
from examples.dnd.actions.equip import Equip
from examples.dnd.entities.weapons.weapon import Weapon

class PlanEquip(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    equip = Equip(parent=self.parent)
    inventory = self.parent.hydrate('inventory')
    inventory_weapons = [item for item in inventory if isinstance(item, Weapon)]
    location_weapons = []

    for child in self.parent.parent.children.values():
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

    equip.set('weapon_id', weapon.id)
    self.parent.set('planned_action_id', equip.id)
