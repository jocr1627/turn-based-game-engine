from copy import deepcopy

class State:
  def __init__(self, raw_state={}):
    self.raw_state = raw_state
  
  def __contains__(self, key):
    return key in self.raw_state

  def __get__(self, key):
    return self.raw_state[key] if key in self.raw_state else None
  
  def __getIn__(self, keys):
    state_slice = self.raw_state

    for key in keys:
      try:
        state_slice = state_slice[key]
      except IndexError:
        return None
      except KeyError:
        return None

    return state_slice

  def get(self, key):
    return deepcopy(self.__get__(key))
  
  def getIn(self, keys):
    return deepcopy(self.__getIn__(keys)) 

  def has(self, key):
    return self.__contains__(key)

  def hasIn(self, keys):
    state_slice = self.raw_state

    for key in keys:
      if key not in state_slice:
        return False
      
      state_slice = state_slice[key]
    
    return True

  def inspect(self, key, getter):
    state_slice = self.__get__(key)

    return getter(state_slice)
  
  def inspectIn(self, keys, getter):
    state_slice = self.__getIn__(keys)

    return getter(state_slice)
  
  def mutate(self, key, mutation):
    state_slice = self.__get__(key)
    mutation(state_slice)
  
  def mutateIn(self, keys, mutation):
    state_slice = self.__getIn__(keys)
    mutation(state_slice)

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

  def update(self, key, updater):
    state_slice = self.__get__(key)
    self.set(key, updater(state_slice))
  
  def updateIn(self, keys, updater):
    state_slice = self.__getIn__(keys)
    self.setIn(keys, updater(state_slice))
