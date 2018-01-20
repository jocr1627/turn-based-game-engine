from engine.action import Action
from engine.entity import Entity

class StartGame(Action):
  def execute(self, diff):
    if hasattr(self.root, 'start_game'):
      self.root.start_game()

    self.root.set('is_in_progress', True)

  def get_is_valid(self):
    return not self.root.get('is_in_progress')

class EndGame(Action):
  def execute(self, diff):
    if hasattr(self.root, 'end_game'):
      self.root.end_game()

    self.root.set('is_in_progress', False)

class StartRound(Action):
  def execute(self, diff):
    if hasattr(self.root, 'start_round'):
      self.root.start_round()

    round_number = self.root.get('round_number')
    self.root.set('round_number', round_number + 1)

class EndRound(Action):
  def execute(self, diff):
    if hasattr(self.root, 'end_round'):
      self.root.end_round()

class Game(Entity):
  def run(self):
    self.triggers = []
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
