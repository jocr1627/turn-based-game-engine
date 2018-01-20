import random
from engine.game import Game

class GoFish(Game):
  def __init__(self, players):
    player_ids = [player.id for player in players]
    super().__init__(children=players, state={ 'player_ids': player_ids })
  
  def end_round(self):
    player_ids = self.get('player_ids')
    players = [self.descendants[player_id] for player_id in player_ids]
    are_cards_in_hands = any(map(lambda player: len(player.get('hand')) > 0, players))
    is_in_progress = len(players) > 1 and (len(self.get('deck')) > 0 or are_cards_in_hands)
    self.set('is_in_progress', is_in_progress)

  def get_default_state(self):
    suites = ['clubs', 'diamonds', 'hearts', 'spades']
    deck = [{ 'suite': suite, 'rank': rank } for rank in range(13) for suite in suites]
    random.shuffle(deck)

    return { 'active_player_id': None, 'deck': deck, 'player_ids': [] }
