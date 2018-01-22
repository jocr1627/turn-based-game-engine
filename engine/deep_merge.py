def deep_merge(obj1, obj2):
  if type(obj1) is not type(obj2):
    raise ValueError(f'Mismatched object types {obj1} and {obj2}')
  elif type(obj1) is list:
    return obj1 + obj2
  elif type(obj1) is set:
    return set(list(obj1) + list(obj2))
  elif type(obj1) is dict:
    result = obj1

    for key,value in obj2.items():
      if (type(value) is list or type(value) is set or type(value) is dict) and key in obj1:
        result[key] = deep_merge(obj1[key], value)
      else:
        result[key] = value
    
    return result
  else:
    return obj2
