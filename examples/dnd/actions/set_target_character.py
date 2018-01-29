class SetTargetCharacter(Listener):
  def execute(self, diff):
    trigger_action = self.root.triggers[-1]['action']
    target_character_ids = trigger_action.get('target_character_ids')
    target_character_id = target_character_ids[0] if len(target_character_ids) == 1 else None
    self.parent.set('target_character_id', target_character_ids[0])

  def get_should_react(self, trigger_action, diff, is_preparation):
    return (
      not is_preparation
      and trigger_action.get_name() is 'Request'
      and trigger_action.get('key') is 'target_character_ids'
    )
