import datetime
import calendar


def get_start_end_of_month(year,month):
    return {
      "start": datetime.date(year,month,1),
      "end":datetime.date(year,month,1).replace(day = calendar.monthrange(year, month)[1])
    }
    
def get_date(year,month,day):
    return datetime.date(year,month,day)
  
def extract_year_and_month_and_day(date):
    data = date.split('-')
    return { "year" : data[0], "month" : data[1],  "day": data[2] }
     