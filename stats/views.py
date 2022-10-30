from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import User, Category, Transaction
from core.serializers import TransactionSerializer
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import simplejson as json
from django.core.cache import cache
from utils import db_config, date_helper, stats_helper


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_stats_month(request):
    print("body: ", json.dumps(request.data, indent=4))  
    user = request.user
    
    month_data = datetime.date.today().strftime("%Y-%m").split("-")
    
    if request.data: month_data = date_helper.get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))
    else: month_data = date_helper.get_start_end_of_month(int(month_data[0]),int(month_data[1]))
    
    print("month: ", month_data)
    
    try:
        all_transactions_month =  None
        cached_all_transactions_month = cache.get(db_config.CACHE_KEYS.transactions_month_all(user.id,month_data["start"].strftime("%Y"), month_data["start"].strftime("%m")))
        
        if cached_all_transactions_month:
            all_transactions_month = cached_all_transactions_month
        else:
            all_transactions_month = user.transaction_set.filter(
                date__range=(month_data["start"], month_data["end"])) 
            all_transactions_month = TransactionSerializer(
                all_transactions_month, many=True).data
            
            cache.set(db_config.CACHE_KEYS.transactions_month_all(user.id, month_data["start"].strftime("%Y"),month_data["start"].strftime("%m")), all_transactions_month)
        
        stats = stats_helper.get_stats_with_category(all_transactions_month)
        
        print("get_stats: ", json.dumps(stats,indent=4))
        
    except Exception as e:
        print(e)
        return Response(
          {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
          },
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    return Response({
        "result": stats,
        "message":"successfully fetched",
        "is_success": True
    })
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stats_recent_one_year(request):
    print("body: ", json.dumps(request.data, indent=4))  
    user = request.user
    
    current_date = datetime.date.today().strftime("%Y-%m").split("-")
    month_data = date_helper.get_start_end_of_month(int(current_date[0]),int(current_date[1]))
    current_date_end = month_data["end"]
    
    date_one_year_before_current = month_data["start"] - relativedelta(years=1)
    
    print(date_one_year_before_current) 
     
    try:
        all_transactions_recent_one_year = user.transaction_set.filter(
            date__range=(date_one_year_before_current, current_date_end)) 
        all_transactions_recent_one_year = TransactionSerializer(
            all_transactions_recent_one_year, many=True).data
        
        stats = stats_helper.get_stats_recent_one_year(all_transactions_recent_one_year)
        
        print("get_stats: ", json.dumps(stats,indent=4))
        
    except Exception as e:
        print(e)
        return Response(
          {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
          },
          status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    return Response({
        "result": stats,
        "message":"successfully fetched",
        "is_success": True
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_category_stats(request, name):
    print("params: ", json.dumps(name, indent=4))  
    user = request.user

    month_data = datetime.date.today().strftime("%Y-%m").split("-")
    
    if request.data: month_data = date_helper.get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))
    else: month_data = date_helper.get_start_end_of_month(int(month_data[0]),int(month_data[1]))
        
    try:
        transactions_current_month_category = user.transaction_set.filter(
        date__range=(month_data["start"], month_data["end"]), category__name=name
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

    stats = stats_helper.get_stats(transactions_current_month_category)
       
    print("get_stats_category: ", json.dumps(stats,indent=4))
    
    return Response({
        "result": stats,
        "message":"successfully fetched",
        "is_success": True
    })
