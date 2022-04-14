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