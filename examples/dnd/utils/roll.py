import random

def roll(dice={ 20: 1 }):
  result = 0

  for sides in dice:
    for count in dice[sides]:
      result += randint(1, sides)
  
  return result
