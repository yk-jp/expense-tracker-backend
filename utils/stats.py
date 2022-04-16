from decimal import Decimal 


def get_stats(event_data):
  stats = {
      "Income": 0,
      "Expense": 0,
      "Balance": 0
  }
    
  for transaction in event_data:
      if transaction["event"] == "Income":
          stats = {
              **stats,
              "Income": Decimal(stats["Income"]) + Decimal(transaction["amount"]),
              "Balance": Decimal(stats["Balance"]) + Decimal(transaction["amount"])
          }
      else:
            stats = {
              **stats,
              "Expense": Decimal(stats["Expense"]) + Decimal(transaction["amount"]),
              "Balance": Decimal(stats["Balance"]) - Decimal(transaction["amount"])
          } 
  
  return stats


def get_stats_with_category(event_data):
  stats = {
      "Income": 0,
      "Expense": 0,
      "Balance": 0,
      "category":{}
  }
    
  for transaction in event_data:
      if transaction["event"] == "Income":
          stats = {
              **stats,
              "Income": Decimal(stats["Income"]) + Decimal(transaction["amount"]),
              "Balance": Decimal(stats["Balance"]) + Decimal(transaction["amount"])
          }
      else:
            stats_category = stats["category"]
            
            if transaction["category"] not in stats_category:
                stats_category = {
                    **stats_category,
                    transaction["category"]: Decimal(transaction["amount"])
                }
            else: 
                stats_category = {
                    **stats_category,
                    transaction["category"]: Decimal(stats_category[transaction["category"]]) + Decimal(transaction["amount"])
                }

            stats = {
              **stats,
              "Expense": Decimal(stats["Expense"]) + Decimal(transaction["amount"]),
              "Balance": Decimal(stats["Balance"]) - Decimal(transaction["amount"]),
              "category":stats_category
          } 
  
  return stats