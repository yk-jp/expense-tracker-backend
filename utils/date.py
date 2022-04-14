import datetime
import calendar


def get_start_end_of_month(year,month):
    return {
      "start": datetime.date(year,month,1),
      "end":datetime.date(year,month,1).replace(day = calendar.monthrange(year, month)[1])
    }
    
def get_date(year,month,day):
    return datetime.date(year,month,day)