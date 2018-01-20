from engine.listener import Listener
from examples.go_fish.actions.request import Request

class UserInputRequest(Listener):
  name = 'UserInputRequest'

  def execute(self, diff, options):
    print(self.parent.get('hand'))
    rank = int(input(f'What card should {self.parent.id} request? '))
    player_ids = self.root.get('player_ids')
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
  
    action = Request(parent=self.parent, state={ 'rank': rank, 'target_id': target_id })
    action.resolve(options={ 'request_class': self.__class__ })

    return {}

  def get_is_valid(self, options):
    return (
      self.parent.id is self.root.get('active_player_id')
      and self.root.get('is_in_progress')
    )

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'StartTurn'
      and self.parent.id is self.root.get('active_player_id')
    )
