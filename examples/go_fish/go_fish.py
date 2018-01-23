import random
from engine.game import Game
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.actions.user_input_request import UserInputRequest

entity_class_list = [
  MaxValueRequest,
  UserInputRequest
]
entity_classes = { clazz.get_name(): clazz for clazz in entity_class_list }

class GoFish(Game):
  def __init__(self, players):
    player_ids = set([player.id for player in players])
    super().__init__(children=players, entity_classes=entity_classes, state={ 'player_ids': player_ids })
  
  def end_round(self):
    players = self.hydrate('player_ids')
    are_cards_in_hands = any(
      map(
        lambda player: player.inspect('hand', lambda hand: len(hand) > 0),
        players
      )
    )
    is_in_progress = (
      len(players) > 1
      and (
        self.inspect('deck', lambda deck: len(deck) > 0)
        or are_cards_in_hands
      )
    )

    self.set('is_in_progress', is_in_progress)

  def get_default_state(self):
    suites = ['clubs', 'diamonds', 'hearts', 'spades']
    deck = [{ 'suite': suite, 'rank': rank } for rank in range(13) for suite in suites]
    random.shuffle(deck)

    return { 'active_player_id': None, 'deck': deck, 'player_ids': set() }
