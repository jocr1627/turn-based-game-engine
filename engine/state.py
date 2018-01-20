from copy import deepcopy

class State:
  def __init__(self, raw_state={}):
    self.raw_state = raw_state
  
  def __contains__(self, key):
    return key in self.raw_state

  def get(self, key):
    return deepcopy(self.raw_state[key]) if key in self.raw_state else None
  
  def getIn(self, keys):
    state_slice = self.raw_state

    for key in keys:
      if key not in state_slice:
        return None
      
      state_slice = state_slice[key]
    
    return deepcopy(state_slice) 

  def has(self, key):
    return self.__contains__(key)

  def hasIn(self, keys):
    state_slice = self.raw_state

    for key in keys:
      if key not in state_slice:
        return False
      
      state_slice = state_slice[key]
    
    return True

  def set(self, key, value):
    self.raw_state[key] = value
  
  def setIn(self, keys, value):
    if len(keys) == 0:
      return

    state_slice = self.raw_state

    for key in keys[0:-1]:
      if key not in state_slice:
        state_slice[key] = {}
      
      state_slice = state_slice[key]
  
    state_slice[keys[-1]] = value
