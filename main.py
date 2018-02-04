import cProfile
import sys
from examples.dnd.dnd import DnD
from examples.dnd.entities.character import Character
from examples.dnd.entities.location import Location
from examples.dnd.entities.armor.iron_armor import IronArmor
from examples.dnd.entities.armor.robe import Robe
from examples.dnd.entities.weapons.stone_sword import StoneSword
from examples.go_fish.go_fish import GoFish
from examples.go_fish.actions.draw_hand import DrawHand
from examples.go_fish.actions.end_turn import EndTurn
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.actions.score import Score
from examples.go_fish.actions.start_turn import StartTurn
from examples.go_fish.actions.user_input_request import UserInputRequest
from examples.go_fish.entities.computer_player import ComputerPlayer
from examples.go_fish.entities.human_player import HumanPlayer

def go_fish():
  players = [HumanPlayer(), ComputerPlayer()]
  game = GoFish(players)
  game.run()

  hands = [player.get('hand') for player in game.hydrate('player_ids')]
  hands_by_rank = []
  total = 0

  for hand in hands:
    hand_by_rank = {}

    for card in hand:
      rank = card['rank']

      if rank not in hand_by_rank:
        hand_by_rank[rank] = 0

      hand_by_rank[rank] += 1
      total += 1

      if hand_by_rank[rank] >= 4:
        print('you done messed up.', rank, hand_by_rank[rank])

    hands_by_rank.append(hand_by_rank)

  print('Hands should be empty:')

  for hand_by_rank in hands_by_rank:
    print(hand_by_rank)

  print('There should be no cards left:', total)

  scores = [player.get('score') for player in players]

  print('Scores should add up to 13:', scores)

def dnd():
  bar = Location('bar')
  door = Location('door', [bar])
  stairs = Location('stairs', [bar])
  upstairs = Location('upstairs', [stairs])
  locations = [
    bar,
    door,
    stairs,
    upstairs
  ]
  character_configs = [
    {
      'armor': Robe(),
      'attributes': {
        'constitution': 1,
        'dexterity': 2,
        'strength': 1
      },
      'name': 'Nigel',
      'location': stairs,
      'weapon': StoneSword()
    },
    {
      'armor': IronArmor(),
      'attributes': {
        'constitution': 1,
        'dexterity': 1,
        'strength': 2
      },
      'name': 'John',
      'location': bar,
      'weapon': StoneSword()
    }
  ]
  characters = [Character(**config) for config in character_configs]
  game = DnD(characters, locations)
  game.run()

game_name = sys.argv[1] if len(sys.argv) > 1 else None

if game_name == 'dnd':
  if 'profile' in sys.argv:
    cProfile.run('dnd()', sort='cumtime')
  else:
    dnd()
else:
  if 'profile' in sys.argv:
    cProfile.run('go_fish()', sort='cumtime')
  else:
    go_fish()
