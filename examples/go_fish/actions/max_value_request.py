import random
from engine.listener import Listener
from examples.go_fish.actions.request import Request

class MaxValueRequest(Listener):
  name = 'MaxValueRequest'

  def execute(self, diff, options):
    hand = self.parent.get('hand')
    hand_by_rank = {}

    for card in hand:
      rank = card['rank']

      if rank not in hand_by_rank:
        hand_by_rank[rank] = 0
      
      hand_by_rank[rank] += 1
    
    hand_by_rank = sorted(hand_by_rank.items(), key=lambda item: item[1], reverse=True)
    rank = hand_by_rank[0][0]
    other_player_ids = [player_id for player_id in self.root.get('player_ids') if player_id != self.parent.id]
    target_id = random.choice(other_player_ids)
    action = Request(parent=self.parent, state={ 'rank': rank, 'target_id': target_id })
    action.resolve(options={ 'request_class': self.__class__ })

    return {}

  def get_is_valid(self, options):
    return (
      self.parent.id is self.root.get('active_player_id')
      and self.root.get('is_in_progress')
      and len(self.parent.get('hand')) > 0
    )

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      not is_preparation
      and trigger_action.name is 'StartTurn'
      and self.parent.id is self.root.get('active_player_id')
    )
