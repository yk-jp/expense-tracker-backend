from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import UserSerializer, CategorySerializer, TransactionSerializer
from .helper import get_start_end_of_month
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
        return Response({
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

@api_view(['GET'])
def get_stats(request):
    print("body: ", json.dumps(request.data, indent=4))  

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    
    try:
        this_month = get_start_end_of_month(current_year,current_month)
        all_transactions_current_month = Transaction.objects.filter(t_date__range=(this_month["start"], this_month["end"])) 
        
        all_transactions_current_month = TransactionSerializer(
            all_transactions_current_month, many=True).data
    except Exception:
        return Response({
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    stats = {
        "Income": 0,
        "Expense": 0,
        "Balance": 0
    }
    
    for transaction in all_transactions_current_month:
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
        
    print("get_stats: ", json.dumps(stats,indent=4))
    
    return Response({
        "result": stats,
        "message":"successfully fetched",
        "is_success": True
    })


