from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import UserSerializer, CategorySerializer, TransactionSerializer
import datetime
import calendar


@api_view(['POST'])
def get_month_all(request):
    print("get_month_all: ",request.data)

    year = int(request.data["year"])
    month = int(request.data["month"])
    
    start_of_month = datetime.date(year,month,1) 
    end_of_month = datetime.date(year,month,1).replace(day = calendar.monthrange(year, month)[1])

    all_transactions_current_month = Transaction.objects.filter(t_date__range=(start_of_month, end_of_month)) 
    
    serializer = TransactionSerializer(
        all_transactions_current_month, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)