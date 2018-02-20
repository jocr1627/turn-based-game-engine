from engine.action import Action

class Request(Action):
  def execute(self, diff):
    args = self.get('args')
    key = self.get('key')
    value = self.parent.getters[key](args)
    self.set(key, value)

def request(requestor, entity, key, args={}):
  state={ 'args': args, 'key': key, 'requestor_id': requestor.id }
  request = Request(parent=entity, state=state)
  request.resolve()

  return request.get(key)
