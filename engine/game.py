from engine.action import Action
from engine.action_stack import ActionStack
from engine.entity import Entity

class StartGame(Action):
  def execute(self, diff):
    self.game.start_game()
    self.game.set('is_in_progress', True)

  def get_is_valid(self, diff):
    return not self.game.get('is_in_progress')

class EndGame(Action):
  def execute(self, diff):
    self.game.end_game()
    self.game.set('is_in_progress', False)

class StartRound(Action):
  def execute(self, diff):
    self.game.start_round()
    round_number = self.game.get('round_number')
    self.game.set('round_number', round_number + 1)

class EndRound(Action):
  def execute(self, diff):
    self.game.end_round()

class Game(Entity):
  def __init__(self, children=[], getters={}, state={}):
    self.action_stack = ActionStack()
    self.descendants = {}
    self.diffs = []
    self.listeners = {}

    super().__init__(children=children, game=self, getters=getters, state=state)

  def end_game(self):
    return

  def end_round(self):
    return

  def run(self):
    self.set('is_in_progress', False)
    self.set('round_number', 0)
    start_game = StartGame(parent=self)
    start_game.resolve()

    while self.get('is_in_progress'):
      start_round = StartRound(parent=self)
      start_round.resolve()
      end_round = EndRound(parent=self)
      end_round.resolve()
  
    end_game = EndGame(parent=self)
    end_game.resolve()

  def start_game(self):
    return

  def start_round(self):
    return
