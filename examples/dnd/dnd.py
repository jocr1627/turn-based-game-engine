
from engine.action import Action
from engine.entity import Entity
from engine.game import Game

class DnD(Game):
  def update(self, diffs):
    if self.state.get('round_number') == 2:
      self.state.set('is_in_progress', False)
