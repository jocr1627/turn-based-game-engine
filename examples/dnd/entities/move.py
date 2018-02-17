from engine.action import Action
from engine.request import request
from examples.dnd.entities.ability import Ability
from examples.dnd.priorities import Priorities

class PrepareMove(Action):
  def execute(self, diff):
    neighbor_ids = list(self.parent.parent.parent.get('neighbor_ids'))
    target_location_id_args = { 'action_id': self.parent.id, 'num_targets': 1, 'valid_ids': neighbor_ids }
    target_location_ids = request(self, self.parent.parent, 'target_location_ids', args=target_location_id_args)
    target_location_id = target_location_ids[0] if len(target_location_ids) > 0 else None
    resolve_args = { 'target_location_id': target_location_id }
    self.parent.set('resolve_args', resolve_args)

class ResolveMove(Action):
  def execute(self, diff):
    target_location = self.hydrate_in(['resolve_args', 'target_location_id'])
    target_location.add_child(self.parent.parent)
    name = self.parent.parent.get('name')
    target_location_name = target_location.get('name')
    print(f'{name} moved to {target_location_name}.')

  def get_is_valid(self, diff):
    return self.parent.parent.get('is_alive')

class Move(Ability):
  matcher = r'move'

  def get_initiative(self):
    return Priorities.NO_ROLL_ACTION

  def get_is_possible(self):
    return len(self.parent.parent.get('neighbor_ids')) > 0

  def prepare(self):
    prepare_move = PrepareMove(parent=self)
    prepare_move.resolve()

  def resolve(self):
    resolve_move = ResolveMove(parent=self, state={ 'resolve_args': self.get('resolve_args') })
    resolve_move.resolve()
