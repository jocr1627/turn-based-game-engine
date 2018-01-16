import random
from engine.game import Game

class GoFish(Game):
  def get_default_state(self, game):
    suites = ['clubs', 'diamonds', 'hearts', 'spades']
    deck = [{ 'suite': suite, 'rank': rank } for rank in range(13) for suite in suites]
    random.shuffle(deck)

    return { 'active_player': None, 'deck': deck }
  
  def get_players(self):
    return [child for child in self.children.values() if 'is_player' in child.state and child.state['is_player']]
  
  def update(self, diffs):
    players = self.get_players()
    are_cards_in_hands = any(map(lambda player: len(player.state['hand']) > 0, players))
    self.state['is_in_progress'] = len(players) > 1 and (len(self.state['deck']) > 0 or are_cards_in_hands)
