def normalize_priority(min_priority, raw_priority):
  return min_priority + raw_priority / (1 + raw_priority)
