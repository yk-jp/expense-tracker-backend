from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import UserSerializer, CategorySerializer, TransactionSerializer
from .helper import get_start_end_of_month
import datetime
import calendar
from decimal import Decimal 

@api_view(['POST'])
def get_month_all(request):
    print("body: ",request.data)

    this_month = get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))
    all_transactions_current_month = Transaction.objects.filter(t_date__range=(this_month["start"], this_month["end"] )) 
    
    serializer = TransactionSerializer(
        all_transactions_current_month, many=True)
    
    print("get_month_all: ",serializer.data)
    return Response(serializer.data)

@api_view(['POST'])
def add_new_event(request):
    print("body: ", request.data)

    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        print("add_new_event: ", serializer.data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_stats(request):
    print("body: ", request.data)

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    
    this_month = get_start_end_of_month(current_year,current_month)
    all_transactions_current_month = Transaction.objects.filter(t_date__range=(this_month["start"], this_month["end"])) 
    
    all_transactions_current_month = TransactionSerializer(
        all_transactions_current_month, many=True).data
    
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
        
    print("get_stats: ", stats)
    return Response(stats, status=status.HTTP_201_CREATED)


