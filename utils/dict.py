

def remove_key_of_none(d_dict):
  for key in d_dict:
    if d_dict[key] == '' or d_dict[key] == None:
      d_dict.pop(key, None)
      
  return d_dict
  
  
  