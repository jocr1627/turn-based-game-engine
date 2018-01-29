from engine.action import Action

class Request(Action):
  def execute(self, diff):
    args = self.get('args')
    key = self.get('key')
    value = self.parent.getters[key](args)
    self.set(key, value)

def request(entity, key, args={}):
  request = Request(parent=entity, state={ 'args': args, 'key': key })
  request.resolve()

  return request.get(key)
