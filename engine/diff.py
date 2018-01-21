from engine.state import State

class Diff(State):
  def __init__(self):
    super().__init__({ 'children': {}, 'state': {} })
