from engine.action import Action

class ImpotentRage(Action):
  def execute(self, diff):
    name = self.parent.get('name')
    print(f'"ARRRGHH, WHY???!!!" - {name}')
