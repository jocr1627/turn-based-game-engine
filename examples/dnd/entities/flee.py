from engine.request import request
from examples.dnd.entities.ability import Ability, AbilityAction
from examples.dnd.utils.get_entities_in_range import get_entities_in_range
from examples.dnd.priorities import Priorities

class PrepareFlee(AbilityAction):
  def execute(self, diff):
    character = self.ability.character
    valid_character_ids = get_entities_in_range(character.location, 1, self.ability.other_character_filter)
    target_character_id_args = { 'action_id': self.ability.id, 'num_targets': 1, 'valid_ids': valid_character_ids }
    target_character_ids = request(self, character, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    target_character = self.hydrate_by_id(target_character_id)
    current_target_location_id = target_character.location.id
    neighbor_ids = [neighbor.id for neighbor in character.location.get_neighbors()]
    valid_location_ids = [location_id for location_id in neighbor_ids if location_id is not current_target_location_id]
    target_location_id_args = { 'action_id': self.ability.id, 'num_targets': 1, 'valid_ids': valid_location_ids }
    target_location_ids = request(self, character, 'target_location_ids', args=target_location_id_args)
    target_location_id = target_location_ids[0] if len(target_location_ids) > 0 else None
    resolve_args = { 'target_character_id': target_character_id, 'target_location_id': target_location_id }
    self.ability.set('resolve_args', resolve_args)

class ResolveFlee(AbilityAction):
  def execute(self, diff):
    character = self.ability.character
    name = character.get('name')
    current_location = character.location
    flee_location = self.hydrate_in(['resolve_args', 'target_location_id'])
    flee_location_name = flee_location.get('name')
    target_character = self.hydrate_in(['resolve_args', 'target_character_id'])
    target_character_name = target_character.get('name')
    target_location = target_character.location

    if target_location is flee_location:
      flee_location = current_location

    if flee_location is not current_location:
      character.move(flee_location.id)
      print(f'{name} fled from {target_character_name} to {flee_location_name}.')
    else:
      print(f'{name} stayed put.')

  def get_is_valid(self, diff):
    return self.ability.character.get('is_alive')

class Flee(Ability):
  matcher = r'^flee$'

  def get_initiative(self):
    return Priorities.FLEE

  def get_is_possible(self):
    return len(get_entities_in_range(self.character.location, 1, self.other_character_filter)) > 0

  def other_character_filter(self, entity):
    return entity.is_type('Character') and not entity is self.character

  def prepare(self):
    prepare_flee = PrepareFlee(parent=self)
    prepare_flee.resolve()

  def resolve(self):
    resolve_flee = ResolveFlee(parent=self, state={ 'resolve_args': self.get('resolve_args') })
    resolve_flee.resolve()
