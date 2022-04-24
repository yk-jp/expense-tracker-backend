from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import User, Category, Transaction
from core.serializers import TransactionSerializer
from utils.date import get_start_end_of_month, get_date
from utils.stats import get_stats
import datetime
import calendar
import simplejson as json
import ast

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_month_all(request):
    print("body: ", json.dumps(request.data, indent=4))  
    
    user = request.user 
    
    this_month = datetime.date.today().strftime("%Y-%m").split("-")
    
    if request.data: this_month = get_start_end_of_month(int(request.data["year"]),int(request.data["month"]))
    else: this_month = get_start_end_of_month(int(this_month[0]),int(this_month[1]))
    
    print("this_month: ", this_month)
    
    try:
        all_transactions_month = user.transaction_set.filter(t_date__range=(this_month["start"], this_month["end"])) 
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
@permission_classes([IsAuthenticated])
def add_new_event(request):
    print("body: ", json.dumps(request.data, indent=4))
    
    user = request.user
    
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
                
            registered_event = user.transaction_set.create(**new_record) 
                
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
    print("body: ", json.dumps(id, indent=4))
    
    user = request.user 
    
    try:
       deleted_event = user.transaction_set.filter(pk=id).delete()

       print("deleted_event", json.dumps(deleted_event, indent=4))

    except Exception:
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
    print("body: ", json.dumps(request.data, indent=4))
    
    user = request.user 
    
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

    except Exception:
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
    print("body: ", json.dumps(request.data, indent=4))
    
    user = request.user 
    
    this_date = datetime.date.today().strftime("%Y-%m-%d")
    
    if request.data: this_date = get_date(int(request.data["year"]),int(request.data["month"]), int(request.data["day"]))
    
    print("this_date: ", this_date)
    
    try:
        all_transactions_selected_day = user.transaction_set.filter(t_date__range=(this_date, this_date)) 
        
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