from decimal import Decimal 
from datetime import datetime

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

def get_stats_recent_one_year(event_data):
    
    stats_all = {}
    
    stats = {
      "Income": 0,
      "Expense": 0,
      "Balance": 0,
    } 
    
    for transaction in event_data:
        transaction_date = transaction["date"]
        month_data = transaction_date.split("-")
        month_data = f"{month_data[0]}-{month_data[1]}"
        
        if month_data not in stats_all:
           stats_all[month_data] = stats 
           
        if transaction["event"] == "Income":
            stats_all[month_data] = {
                **stats_all[month_data],
                "Income": Decimal(stats_all[month_data]["Income"]) + Decimal(transaction["amount"]),
                "Balance": Decimal(stats_all[month_data]["Balance"]) + Decimal(transaction["amount"])
            }
        else:
            stats_all[month_data] = {
                **stats_all[month_data],
                "Expense": Decimal(stats_all[month_data]["Expense"]) + Decimal(transaction["amount"]),
                "Balance": Decimal(stats_all[month_data]["Balance"]) - Decimal(transaction["amount"])
            } 
    
    return stats_all