from engine.listener import Listener

class DurationEffect(Listener):
  def get_should_terminate(self, diff):
    starting_round_number = self.get('starting_round_number')

    return self.game.get('round_number') == starting_round_number + 2
