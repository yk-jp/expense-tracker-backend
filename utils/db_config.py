

class CacheKeys(object):
  # keys
  CATEGORY_ALL = '-category_all'
  TRANSACTIONS_MONTH_ALL = '-transactions_month_all'
  TRANSACTIONS_SELECTED_DAY_ALL = '-transactions_selected_day_all'
   
  _instance = None

  def __new__(self):
    if not self._instance:
      self._instance = super(CacheKeys, self).__new__(self)
    
    return self._instance
   
  def transactions_month_all(self, user_id, year, month):
    return f'{user_id}-{year}-{month}' + self.TRANSACTIONS_MONTH_ALL
 
  def transactions_selected_day_all(self, user_id, year, month, day):
    return f'{user_id}-{year}-{month}-{day}' + self.TRANSACTIONS_SELECTED_DAY_ALL
 
 
CACHE_KEYS = CacheKeys()