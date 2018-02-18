from engine.request import request
from examples.dnd.entities.ability import Ability, AbilityAction
from examples.dnd.entities.base_character import BaseCharacter
from examples.dnd.utils.get_entities_in_range import get_entities_in_range
from examples.dnd.priorities import Priorities

class PrepareAdvance(AbilityAction):
  def execute(self, diff):
    character = self.ability.character
    valid_character_ids = get_entities_in_range(character.location, 1, self.ability.other_character_filter)
    target_character_id_args = { 'action_id': self.ability.id, 'num_targets': 1, 'valid_ids': valid_character_ids }
    target_character_ids = request(self, character, 'target_character_ids', args=target_character_id_args)
    target_character_id = target_character_ids[0] if len(target_character_ids) > 0 else None
    target_character = self.hydrate_by_id(target_character_id)
    resolve_args = { 'original_target_location_id': target_character.location.id, 'target_character_id': target_character_id }
    self.ability.set('resolve_args', resolve_args)

class ResolveAdvance(AbilityAction):
  def execute(self, diff):
    character = self.ability.character
    name = character.get('name')
    current_location = character.location
    original_target_location = self.hydrate_in(['resolve_args', 'original_target_location_id'])
    target_character = self.hydrate_in(['resolve_args', 'target_character_id'])
    target_character_name = target_character.get('name')
    target_location = target_character.location
    neighbors = current_location.hydrate('neighbor_ids')
    possible_locations = [current_location] + neighbors
    advance_location = target_location if target_location in possible_locations else original_target_location
    advance_location_name = advance_location.get('name')

    if advance_location is not current_location:
      advance_location.add_child(character)
      print(f'{name} advanced on {target_character_name} to {advance_location_name}.')
    else:
      print(f'{name} stayed put.')

  def get_is_valid(self, diff):
    return self.ability.character.get('is_alive')

class Advance(Ability):
  matcher = r'^advance$'

  def get_initiative(self):
    return Priorities.ADVANCE

  def get_is_possible(self):
    return len(get_entities_in_range(self.character.location, 1, self.other_character_filter)) > 0

  def other_character_filter(self, entity):
    return entity.is_type('Character') and not entity is self.character

  def prepare(self):
    prepare_advance = PrepareAdvance(parent=self)
    prepare_advance.resolve()

  def resolve(self):
    resolve_advance = ResolveAdvance(parent=self, state={ 'resolve_args': self.get('resolve_args') })
    resolve_advance.resolve()
