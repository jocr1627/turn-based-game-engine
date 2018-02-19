from engine.listener import Listener
from examples.go_fish.actions.discard import Discard

class Score(Listener):
  def execute(self, diff):
    hand = self.parent.get('hand')
    hand_by_rank = {}

    for card in hand:
      rank = card['rank']

      if rank not in hand_by_rank:
        hand_by_rank[rank] = 0
      
      hand_by_rank[rank] += 1

    hand_by_rank = sorted(hand_by_rank.items(), key=lambda item: item[1], reverse=True)
    rank_to_discard = hand_by_rank[0][0]
    matching_cards = [card for card in hand if card['rank'] == rank_to_discard]

    for i in range(4):
      card_to_remove = matching_cards[i]
      discard = Discard(parent=self.parent, state={ 'card': card_to_remove })
      discard.resolve()

    score = self.parent.get('score')
    self.parent.set('score', score + 1)

  def get_is_valid(self, diff):
    hand = self.parent.get('hand')

    if len(hand) < 4:
      return False

    hand_by_rank = {}

    for card in hand:
      rank = card['rank']

      if rank not in hand_by_rank:
        hand_by_rank[rank] = 0
      
      hand_by_rank[rank] += 1

    hand_by_rank = sorted(hand_by_rank.items(), key=lambda item: item[1], reverse=True)

    return hand_by_rank[0][1] >= 4
  
  def get_should_react(self, diff):
    return diff.inspect_in(
      ['state', self.parent.id, 'hand'],
      lambda hand_diff: hand_diff is not None and len(hand_diff[1]) > len(hand_diff[0])
    )
