from engine.deep_merge import deep_merge
from engine.listener import Listener
from examples.go_fish.actions.request import Request

class UserInputRequest(Listener):
  def execute(self, diff):
    print(self.parent.get('hand'))
    rank = None

    while rank is None:
      try:
        input_value = input(f'What card should {self.parent.id} request? ')
        rank = int(input_value)

        if rank < 0 or rank > 12:
          rank = None
          raise ValueError
      except ValueError:
        print(f'{input_value} is not a valid rank')

    player_ids = self.game.get('player_ids')
    other_player_ids = [player_id for player_id in player_ids if player_id != self.parent.id]
    is_target_found = False

    while not is_target_found:
      target_id = int(input(f'From which player? '))

      if target_id == self.parent.id:
        print(f'You cannot request a card from yourself. Options include: {other_player_ids} Try again.')
      elif target_id not in other_player_ids:
        print(f'No matches found for player {target_id}. Options include: {other_player_ids} Try again.')
      else:
        is_target_found = True
  
    request_state = { 'rank': rank, 'request_class_name': self.get_name(), 'target_id': target_id }
    action = Request(parent=self.parent, state=request_state)
    action.resolve()

  def get_default_trigger_types(self):
    return deep_merge(
      super().get_default_trigger_types(),
      ['StartTurn']
    )

  def get_is_valid(self, diff):
    return (
      self.parent.id is self.game.get('active_player_id')
      and self.game.get('is_in_progress')
    )

  def get_should_react(self, diff):    
    return self.parent.id is self.game.get('active_player_id')
