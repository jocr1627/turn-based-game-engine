import random
import re
from engine.action import Action
from examples.dnd.entities.player import Player

def sort_tied_actions(actions):
  print(f'The following characters have tied for initiative:')
  
  for action in actions:
    print(action.parent.get('name'), action.get_name(), action.id)

  num_actions = len(actions)
  actions_by_id = { action.id: action for action in actions }
  action_ids = [action.id for action in actions]
  sorted_actions = None

  while sorted_actions is None:
    string_input = input('Enter action resolution order by id ("skip" for random): ')
    
    if re.match(r'^s(kip)?$', string_input):
      random.shuffle(actions)
      sorted_actions = actions
      break
    
    string_input = [value for value in string_input.split(',') if len(value) > 0]
    num_input = len(string_input)

    if num_input != num_actions:
      print(f'Expected {num_actions} ids, but got {num_input}. Try again.')
      continue

    is_valid = True
    sorted_actions = []

    for raw_action_id in string_input:
      try:
        action_id = int(raw_action_id)

        if action_id not in actions_by_id:
          sorted_actions = None
          print(f'{action_id} does not correspond to a valid action id. Options include: {action_ids} Try again.')
          break

        sorted_actions.append(actions_by_id[action_id])
      except ValueError:
        sorted_actions = None
        print(f'{raw_action_id} is not a valid action id. Options include: {action_ids} Try again.')
        break
    
    if sorted_actions is not None and not all(map(lambda action: action in sorted_actions, actions)):
      sorted_actions = None
      print(f'Not all action ids were specified. Ids include: {action_ids} Try again.')
  
  return sorted_actions

class ResolvePhase(Action):
  def execute(self, diff):
    actions_by_initiative = {}

    for character in self.game.get_characters():
      ability = character.get_active_ability()

      if ability is not None:
        initiative = ability.get_initiative()

        if initiative not in actions_by_initiative:
          actions_by_initiative[initiative] = []
        
        actions_by_initiative[initiative].append(ability)

    actions_by_initiative = sorted(actions_by_initiative.items(), key=lambda item: item[0], reverse=True)
    action_queue = []

    for initiative,sub_queue in actions_by_initiative:
      if len(sub_queue) > 1:
        npc_actions = [action for action in sub_queue if not isinstance(action.parent, Player)]

        if len(npc_actions) > 1:
          npc_actions = sort_tied_actions(npc_actions)
  
        player_actions = [action for action in sub_queue if isinstance(action.parent, Player)]

        if len(player_actions) > 1:
          player_actions = sort_tied_actions(player_actions)

        sub_queue = player_actions + npc_actions

      action_queue += sub_queue

    for action in action_queue:
      action.resolve()
