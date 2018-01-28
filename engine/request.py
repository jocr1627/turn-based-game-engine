class Request(Action):
  def execute(self, diff):
    args = self.get('args')
    key = self.get('key')
    value = self.parent.getters[key](args)
    self.set(key, value)
