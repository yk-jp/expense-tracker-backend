from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import User, Category, Transaction
from core.serializers import TransactionSerializer
import datetime
import calendar
import simplejson as json
from django.core.cache import cache
from utils import db_config, stats_helper, date_helper

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_month_all(request):
    user = request.user 
    
    this_month = datetime.date.today().strftime("%Y-%m").split("-")
    
    if request.data: this_month = date_helper.get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))
    else: this_month = date_helper.get_start_end_of_month(int(this_month[0]),int(this_month[1]))
    
    try:
        all_transactions_month =  None
        cached_all_transactions_month = cache.get(db_config.CACHE_KEYS.transactions_month_all(user.id,request.data["year"],request.data["month"]))
        
        if cached_all_transactions_month:
            all_transactions_month = cached_all_transactions_month
        else:
            all_transactions_month = user.transaction_set.filter(date__range=(this_month["start"], this_month["end"])) 
            all_transactions_month = TransactionSerializer(all_transactions_month, many=True).data
            cache.set(db_config.CACHE_KEYS.transactions_month_all(user.id,request.data["year"],request.data["month"]), all_transactions_month)
        
        stats = stats_helper.get_stats(all_transactions_month)
        
    except Exception as e:
        return Response(
        {
            "message":"Failed to fetch data. Please try to refresh the page",
            "is_success":False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
        
   
     
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
@permission_classes([IsAuthenticated])
def add_new_event(request):
    user = request.user
    
    new_record = {
        **request.data,
        "user": user.id
    }
    
    try:
        new_event = TransactionSerializer(data = new_record)
        if new_event.is_valid():
            new_record = {
                    **new_record,
                    "category": Category.objects.get(pk=request.data["category"])
            }
            registered_event = user.transaction_set.create(**new_record) 
            
            date_data = date_helper.extract_year_and_month_and_day(new_record["date"])
            cache.delete(db_config.CACHE_KEYS.transactions_month_all(user.id,date_data["year"],date_data["month"]))
            # delete cache for the day
            cache.delete(db_config.CACHE_KEYS.transactions_selected_day_all(user.id,date_data["year"], date_data["month"], date_data["day"]))
            
        else:
            return Response(
                {
                "message": {
                    **new_event.errors
                },
                "is_success" : False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            { 
                "message": "successfully registered",
                "is_success": True
            },
                status=status.HTTP_201_CREATED
            )
    
    except Exception as e:
        raise e
        return Response(
                {
                "message": "Failed to register new record. Please try again",
                "is_success" : False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, id):
    user = request.user 
    
    data = {
        **request.data #date
    }
    
    try:
       deleted_event = user.transaction_set.filter(pk=id).delete()
       
       date_data = date_helper.extract_year_and_month_and_day(data["date"])
       cache.delete(db_config.CACHE_KEYS.transactions_month_all(user.id, date_data["year"],date_data["month"]))
       # delete cache for the day
       cache.delete(db_config.CACHE_KEYS.transactions_selected_day_all(user.id,date_data["year"], date_data["month"], date_data["day"]))

    except Exception as e:
        return Response(
        {
            "message":"Failed to delete data. Please try to refresh the page",
            "is_success":False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    return Response(
        {
            "message": "successfully deleted",
            "is_success": True
        })
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request,id):
    user = request.user 

    prev_date = request.data.pop('prev_date', None)
    
    new_record = {
        **request.data,
        "user": user.id
    }
    
    try:
        new_event = TransactionSerializer(data = new_record)
        if new_event.is_valid():
            if Category.objects.filter(pk=request.data["category"]).exists():
                new_record = {
                        **new_record,
                        "category": Category.objects.get(pk=request.data["category"])
                    }
                
            user.transaction_set.filter(pk=id).update(**new_record)
            date_data = date_helper.extract_year_and_month_and_day(prev_date)
            cache.delete(db_config.CACHE_KEYS.transactions_month_all(user.id, date_data["year"],date_data["month"]))
            # delete cache for the day
            cache.delete(db_config.CACHE_KEYS.transactions_selected_day_all(user.id,date_data["year"], date_data["month"], date_data["day"]))
                
        else:
            return Response(
                {
                "message": {
                    **new_event.errors
                },
                "is_success" : False
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        return Response(
        {
            "message":"Failed to update data. Please try to refresh the page",
            "is_success":False
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
    
    return Response(
        {
            "message": "successfully updated",
            "is_success": True
        })
     
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_day_event(request):
    user = request.user 
    
    this_date = datetime.date.today().strftime("%Y-%m-%d")
    
    if request.data: this_date = date_helper.get_date(int(request.data["year"]),int(request.data["month"]), int(request.data["day"]))
    
    try:
        all_transactions_selected_day =  None
        cached_all_transactions_selected_day = cache.get(db_config.CACHE_KEYS.transactions_selected_day_all(user.id,request.data["year"],request.data["month"], request.data["day"]))
            
        if cached_all_transactions_selected_day:
            all_transactions_selected_day  = cached_all_transactions_selected_day
        else:
            all_transactions_selected_day = user.transaction_set.filter(date__range=(this_date, this_date)) 
            all_transactions_selected_day = TransactionSerializer(
            all_transactions_selected_day, many=True).data
                
            cache.set(db_config.CACHE_KEYS.transactions_selected_day_all(user.id,request.data["year"],request.data["month"], request.data["day"]), all_transactions_selected_day)
            
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