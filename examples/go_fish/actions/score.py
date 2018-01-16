from engine.action import Action
from examples.go_fish.actions.discard import Discard

class Score(Action):
  name = 'Score'

  def execute(self):
    score = self.entity.state['score']
    new_score = score + 1
    self.entity.state['score'] = new_score
    hand = self.entity.state['hand']
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
      discard = Discard(self.game, self.entity, { 'card': card_to_remove })
      discard.resolve()
    
    return { self.entity.id: { 'score': (score, new_score) } }

  def get_is_valid(self):
    hand = self.entity.state['hand']

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
