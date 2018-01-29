import random

def roll(dice={ 20: 1 }):
  result = 0

  for sides in dice:
    for count in range(dice[sides]):
      result += random.randint(1, sides)
  
  return result
