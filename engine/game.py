from engine.action import Action
from engine.entity import Entity

class StartGame(Action):
  name = 'StartGame'

  def execute(self):
    diffs = self.options['executeFn']()
    is_in_progress = self.game.state['is_in_progress']
    self.game.state['is_in_progress'] = True
    game_diff = diffs[self.game.id] if self.game.id in diffs else {}
    game_diff['is_in_progress'] = (is_in_progress, True)
    diffs[self.game.id] = game_diff
  
    return diffs

  def get_is_valid(self):
    return not self.game.state['is_in_progress']

class EndGame(Action):
  name = 'EndGame'

  def execute(self):
    diffs = self.options['executeFn']()
    is_in_progress = self.game.state['is_in_progress']
    self.game.state['is_in_progress'] = False
    game_diff = diffs[self.game.id] if self.game.id in diffs else {}
    game_diff['is_in_progress'] = (is_in_progress, False)
    diffs[self.game.id] = game_diff

    return diffs

class StartRound(Action):
  name = 'StartRound'

  def execute(self):
    diffs = self.options['executeFn']()
    round_number = self.game.state['round_number']
    new_round_number = round_number + 1
    self.game.state['round_number'] = new_round_number
    game_diff = diffs[self.game.id] if self.game.id in diffs else {}
    game_diff['round_number'] = (round_number, new_round_number)
    diffs[self.game.id] = game_diff

    return diffs

class EndRound(Action):
  name = 'EndRound'

  def execute(self):
    return self.options['executeFn']()

class Game(Entity):
  def __init__(
    self,
    children=None,
    endGame=lambda: {},
    endRound=lambda: {},
    reactions=None,
    startGame=lambda: {},
    startRound=lambda: {},
    state=None
  ):
    self.endGameFn = endGame
    self.endRoundFn = endRound
    self.startGameFn = startGame
    self.startRoundFn = startRound
    self.triggers = []

    super().__init__(self, children, reactions, state)

  def run(self):
    self.state['is_in_progress'] = False
    self.state['round_number'] = 0
    startGame = StartGame(self, self, { 'executeFn': self.startGameFn })
    startGame.resolve()

    while self.state['is_in_progress']:
      startRound = StartRound(self, self, { 'executeFn': self.startRoundFn })
      startRound.resolve()
      endRound = EndRound(self, self, { 'executeFn': self.endRoundFn })
      endRound.resolve()
  
    endGame = EndGame(self, self, { 'executeFn': self.endGameFn })
    endGame.resolve()

  def update(self, diffs):
    self.state['is_in_progress'] = False
