from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import User, Category, Transaction
from core.serializers import TransactionSerializer
from utils.date import get_start_end_of_month
from utils.stats import get_stats, get_stats_with_category
import datetime
import calendar
import simplejson as json


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats_month(request):
    print('auth ',request.user)
    user = request.user
    
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    
    try:
        this_month = get_start_end_of_month(current_year,current_month)
        
        all_transactions_current_month = user.transaction_set.filter(
            t_date__range=(this_month["start"], this_month["end"])) 
        
        all_transactions_current_month = TransactionSerializer(
            all_transactions_current_month, many=True).data
    except Exception:
        return Response(
          {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
          },
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    stats = get_stats_with_category(all_transactions_current_month)
        
    print("get_stats: ", json.dumps(stats,indent=4))
    
    return Response({
        "result": stats,
        "message":"successfully fetched",
        "is_success": True
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_stats(request, name):
    print("params: ", json.dumps(name, indent=4))  
    user = request.user

    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    this_month = get_start_end_of_month(current_year,current_month)
        
    try:
        transactions_current_month_category = user.transaction_set.filter(
        t_date__range=(this_month["start"], this_month["end"]), category__name=name
        ) 
        transactions_current_month_category = TransactionSerializer(
            transactions_current_month_category, many=True).data
        
        print("get_stats_category: ", json.dumps(transactions_current_month_category,indent=4))
    except Exception:
        return Response(
          {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
          },
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 

    stats = get_stats(transactions_current_month_category)
       
    print("get_stats_category: ", json.dumps(stats,indent=4))
    
    return Response({
        "result": stats,
        "message":"successfully fetched",
        "is_success": True
    })
