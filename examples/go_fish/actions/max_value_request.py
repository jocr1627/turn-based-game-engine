import random
from engine.action import Phases
from engine.base_entity_listener import BaseEntityListener
from examples.go_fish.actions.request import Request

class MaxValueRequest(BaseEntityListener):
  def execute(self, diff):
    hand = self.parent.get('hand')
    hand_by_rank = {}

    for card in hand:
      rank = card['rank']

      if rank not in hand_by_rank:
        hand_by_rank[rank] = 0
      
      hand_by_rank[rank] += 1
    
    hand_by_rank = sorted(hand_by_rank.items(), key=lambda item: item[1], reverse=True)
    rank = hand_by_rank[0][0]
    other_player_ids = [player_id for player_id in self.game.get('player_ids') if player_id != self.parent.id]
    target_id = random.choice(other_player_ids)
    request_state = { 'rank': rank, 'request_class_name': self.get_name(), 'target_id': target_id }
    action = Request(parent=self.parent, state=request_state)
    action.resolve()

  def get_is_valid(self, diff):
    return (
      self.parent.id is self.game.get('active_player_id')
      and self.game.get('is_in_progress')
      and self.parent.inspect('hand', lambda hand: len(hand) > 0)
    )

  def get_should_react(self, diff):
    trigger = self.get_trigger()

    return (
      trigger.phase is Phases.EXECUTION
      and trigger.get_name() is 'StartTurn'
      and self.parent.id is self.game.get('active_player_id')
    )
