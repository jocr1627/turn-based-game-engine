from engine.listener import Listener

class SetTargetCharacter(Listener):
  def execute(self, diff):
    trigger_action = self.root.triggers[-2]['action']
    target_character_ids = trigger_action.get('target_character_ids')
    target_character_id = None

    if isinstance(target_character_ids, list) and len(target_character_ids) == 1:
      target_character_id = target_character_ids[0]

    self.parent.set('target_character_id', target_character_id)

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      not is_preparation
      and trigger_action.get_name() is 'Request'
      and trigger_action.get('key') is 'target_character_ids'
      and trigger_action.parent is self.parent
    )
