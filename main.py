import sys
from examples.dnd.dnd import DnD
from examples.dnd.actions.plan_impotent_rage import PlanImpotentRage
from examples.dnd.entities.character import Character
from examples.go_fish.actions.end_turn import EndTurn
from examples.go_fish.actions.max_value_request import MaxValueRequest
from examples.go_fish.actions.start_turn import StartTurn
from examples.go_fish.actions.user_input_request import UserInputRequest
from examples.go_fish.entities.player import Player
from examples.go_fish.go_fish import GoFish

def go_fish(): 
  game = GoFish()
  player_reactions = [
    [
      EndTurn,
      StartTurn,
      UserInputRequest
    ],
    [
      EndTurn,
      StartTurn,
      MaxValueRequest
    ]
  ]
  players = [Player(game, reactions=reactions) for reactions in player_reactions]

  for player in players:
    game.add_child(player)

  game.run()

  players = game.get_players()
  hands = [player.state['hand'] for player in players]
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
        print('you done fucked up.', rank, hand_by_rank[rank])

    hands_by_rank.append(hand_by_rank)

  print('Hands should be empty:')

  for hand_by_rank in hands_by_rank:
    print(hand_by_rank)

  print('There should be no cards left:', total)

  scores = [player.state['score'] for player in players]

  print('Scores should add up to 13:', scores)

def dnd():
  game = DnD()
  character_states = [
    {
      'actions': {
        'rage': PlanImpotentRage
      },
      'charisma': 5,
      'initiative': 0,
      'name': 'Nigel',
      'planned_actions': []
    },
    {
      'actions': {
        'rage': PlanImpotentRage
      },
      'charisma': 2,
      'initiative': 0,
      'name': 'John',
      'planned_actions': []
    }
  ]
  characters = [Character(game, state=state) for state in character_states]

  for character in characters:
    game.add_child(character)

  game.run()

game_name = sys.argv[1] if len(sys.argv) > 1 else None

if game_name == 'dnd':
  dnd()
else:
  go_fish()
