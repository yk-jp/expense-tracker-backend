from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import TransactionSerializer
from utils.date import get_start_end_of_month, get_date
from utils.stats import get_stats
import datetime
import calendar
import simplejson as json


@api_view(['POST'])
def get_month_all(request):
    print("body: ", json.dumps(request.data, indent=4))    
    
    this_month = datetime.date.today().strftime("%Y-%m").split("-")
    
    if request.data: this_month = get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))
    else: this_month = get_start_end_of_month(int(this_month[0]),int(this_month[1]))
    
    print("this_month: ", this_month)
    
    try:
        all_transactions_month = Transaction.objects.filter(t_date__range=(this_month["start"], this_month["end"])) 
        all_transactions_month = TransactionSerializer(
            all_transactions_month, many=True).data
        
        print("get_month_all: ",json.dumps(all_transactions_month,indent=4))

    except Exception:
        return Response(
        {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
        
    stats = get_stats(all_transactions_month)
    
    print("get_month_all stats: ", json.dumps(stats,indent=4))
     
    return Response(
        {
            "result": {
                "all_transactions":all_transactions_month,
                "stats":stats
            },
            "message": "successfully fecthed",
            "is_success": True
        })

@api_view(['POST'])
def add_new_event(request):
    print("body: ", json.dumps(request.data, indent=4))    

    serializer = TransactionSerializer(data=request.data)
    
    if serializer.is_valid():
        print("add_new_event: ", json.dumps(serializer.data, indent=4))
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_day_event(request):
    print("body: ", json.dumps(request.data, indent=4))
    
    this_date = datetime.date.today().strftime("%Y-%m-%d")
    
    if request.data: this_date = get_date(int(request.data["year"]),int(request.data["month"]), int(request.data["day"]))
    
    print("this_date: ", this_date)
    
    try:
        all_transactions_selected_day = Transaction.objects.filter(t_date__range=(this_date, this_date)) 
        
        all_transactions_selected_day = TransactionSerializer(
            all_transactions_selected_day, many=True).data
        
        print("get_day_event: ", json.dumps(all_transactions_selected_day,indent=4))

    except Exception:
        return Response(
        {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    return Response(
        {
            "result": all_transactions_selected_day,
            "message": "successfully fecthed",
            "is_success": True
        })
    
