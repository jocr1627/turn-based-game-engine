
from engine.action import Action
from engine.entity import Entity
from engine.game import Game

class DnD(Game):
  def end_round(self):
    if self.get('round_number') == 2:
      self.set('is_in_progress', False)
