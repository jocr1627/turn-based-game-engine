from engine.action import Action, Phases

class Request(Action):
  def execute(self, diff):
    args = self.get('args')
    key = self.get('key')
    value = self.parent.getters[key](args)
    self.set(key, value)
  
  def get_should_terminate(self, diff):
    trigger = self.get_trigger()

    return (
      self.get('requestor_id') == trigger.id
      and self.phase is Phases.EXECUTION
    )

def request(requestor, entity, key, args={}):
  state={ 'args': args, 'key': key, 'requestor_id': requestor.id }
  request = Request(parent=entity, state=state)
  request.resolve()

  return request.get(key)
