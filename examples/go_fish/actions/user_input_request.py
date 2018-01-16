from engine.action import Action
from examples.go_fish.actions.request import Request

class UserInputRequest(Action):
  name = 'UserInputRequest'

  def execute(self):
    print(self.entity.state['hand'])
    rank = int(input(f'What card should {self.entity.id} request? '))
    players = self.game.get_players()
    other_player_ids = [player.id for player in players if player.id != self.entity.id]
    target = None

    while target is None:
      target_id = int(input(f'From which player? '))

      if target_id == self.entity.id:
        print(f'You cannot request a card from yourself. Options include: {other_player_ids} Try again.')
      else:
        target_matches = [player for player in players if player.id == target_id]

        if len(target_matches) == 0:
          print(f'No matches found for player {target_id}. Options include: {other_player_ids} Try again.')
        else:
          target = target_matches[0]
  
    action = Request(self.game, self.entity, { 'rank': rank, 'request_class': self.__class__, 'target': target })
    action.resolve()

    return {}

  def get_is_valid(self):
    return (
      self.entity is self.game.state['active_player']
      and self.game.state['is_in_progress']
    )

  def get_should_react(self, trigger_action, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'StartTurn'
      and self.entity is self.game.state['active_player']
    )
