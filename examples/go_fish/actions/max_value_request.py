import random
from engine.action import Action
from examples.go_fish.actions.request import Request

class MaxValueRequest(Action):
  name = 'MaxValueRequest'

  def execute(self):
    hand = self.entity.state.get('hand')
    hand_by_rank = {}

    for card in hand:
      rank = card['rank']

      if rank not in hand_by_rank:
        hand_by_rank[rank] = 0
      
      hand_by_rank[rank] += 1
    
    hand_by_rank = sorted(hand_by_rank.items(), key=lambda item: item[1], reverse=True)
    rank = hand_by_rank[0][0]
    other_players = [player for player in self.game.get_players() if player.id != self.entity.id]
    target = random.choice(other_players)
    action = Request(self.game, self.entity, { 'rank': rank, 'request_class': self.__class__, 'target': target })
    action.resolve()

    return {}

  def get_is_valid(self):
    return (
      self.entity.id is self.game.state.get('active_player')
      and self.game.state.get('is_in_progress')
    )

  def get_should_react(self, trigger_action, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'StartTurn'
      and self.entity.id is self.game.state.get('active_player')
    )
