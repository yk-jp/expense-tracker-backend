from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import TransactionSerializer
from utils.date import get_start_end_of_month
import datetime
import calendar
import simplejson as json
from decimal import Decimal 

@api_view(['POST'])
def get_month_all(request):
    print("body: ", json.dumps(request.data, indent=4))    
    
    this_month = get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))

    try:
        all_transactions_current_month = Transaction.objects.filter(t_date__range=(this_month["start"], this_month["end"])) 
        serializer = TransactionSerializer(
            all_transactions_current_month, many=True)
        
        print("get_month_all: ",json.dumps(serializer.data,indent=4))

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
            "result": serializer.data,
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