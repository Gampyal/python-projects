



#recursive search algorithm
def recursive_search(list, item):
  if len(list) == 0:
    return False
  
  if list[0] == item:
    return True
  
  remaining_list = list[1:]
  
  return recursive_search(remaining_list, item)