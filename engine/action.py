class Action:
  name = 'Action'

  def __init__(self, game, entity, options={}):
    self.game = game
    self.entity = entity
    self.options = options

  def execute(self):
    return {}

  def get_is_cycle(self):
    return any(map(lambda trigger: self.entity is trigger['action'].entity and self.name is trigger['action'].name, self.game.triggers))

  def get_is_valid(self):
    return True

  def get_priority(self):
    return 0
  
  def get_should_react(self, trigger_action, is_preparation):
    return False

  def handle_reactions(self, is_preparation=False):
    reaction_queue = []

    for entity in self.game.get_descendants():
      for reaction_class in entity.reactions:
        reaction = reaction_class(self.game, entity)
  
        if not reaction.get_is_cycle() and reaction.get_should_react(self, is_preparation):
          reaction_queue.append(reaction)
    
    reaction_queue = sorted(reaction_queue, key=lambda reaction: reaction.get_priority(), reverse=True)

    for reaction in reaction_queue:
      reaction.resolve()

  def resolve(self):
    if not self.get_is_valid():
      return
    
    self.game.triggers.append({ 'action': self, 'is_preparation': True })
    self.handle_reactions(is_preparation=True)
    self.game.triggers.pop()

    if not self.get_is_valid():
      return

    self.game.triggers.append({ 'action': self, 'is_preparation': False })
    diffs = self.execute()
    self.game.update(diffs)

    for entity in self.game.get_descendants():
      entity.update(diffs)

    self.handle_reactions()
    self.game.triggers.pop()
