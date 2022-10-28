from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import User
from core.serializers import CategorySerializer
from django.core.exceptions import ValidationError
from django.core.cache import cache
import simplejson as json
from utils import db_config


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_category_all(request, type):
  user = request.user
  category_all = None
  
  cache_key = db_config.CACHE_KEYS.create_category_key(str(user.id), type)
  
  try:
    cached_category_all = cache.get(cache_key)
    if cached_category_all:
      category_all = cached_category_all 
    else:
      category_all = user.category_set.filter(category_type=type)
      category_all = CategorySerializer(category_all, many=True).data
      cache.set(cache_key, category_all)
  
  except Exception as e:
    print(e)
    return Response(
      {   
          "message":"Failed to fetch data. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
     
  return Response(
      {
          "result": {
            "category_all": category_all
          },
          "message": "successfully fetched",
          "is_success": True
      })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
  print("body: ", json.dumps(request.data, indent=4)) 
  
  user = request.user
  
  new_record = {
    **request.data,
    "user": user.id
  } 
  
  cache_key = db_config.CACHE_KEYS.create_category_key(str(user.id), request.data["category_type"])
  
  try:
    new_category = CategorySerializer(data = new_record) 
    
    if new_category.is_valid() and new_category.create_validation():
      user.category_set.create(**new_record)
      # delete cache
      cache.delete(cache_key)
      
    else:
        return Response(
            {
            "message": {
                **new_category.errors
            },
            "is_success" : False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
  
  except (ValueError,ValidationError) as e:
    raise e
    return Response(
      {   
          "message": e.args[0],
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 

  except Exception as e:
    raise e
    return Response(
      {   
          "message":"Failed to register new category. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully registered",
          "is_success": True
      })
 
 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, type, id):
  print("body: ", json.dumps(request.data, indent=4)) 
  
  user = request.user 
  
  new_record = {
      **request.data,
      "user": user.id
  }
  
  cache_key = db_config.CACHE_KEYS.create_category_key(str(user.id), type)
   
  try:
    new_category = CategorySerializer(data = new_record) 
    
    if new_category.is_valid() and new_category.update_validation(id):
      user.category_set.filter(pk=id).update(**new_record)
      # delete cache
      cache.delete(cache_key)
       
    else:
        return Response(
            {
            "message": {
                **new_category.errors
            },
            "is_success" : False
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
  
  except (ValueError,ValidationError) as e:
    raise e
    return Response(
      {   
          "message": e.args[0],
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 

  except Exception as e:
    raise e
    return Response(
      {   
          "message":"Failed to update category. Please try again",
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully updated",
          "is_success": True
      })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request,type, id):
  user = request.user 
  cache_key = db_config.CACHE_KEYS.create_category_key(str(user.id), type)
  
  try:
    user.category_set.filter(pk=id).delete()
    # delete cache
    cache.delete(cache_key)
  
  except Exception as e:
    return Response(
      {   
          "message":'Failed to delete data. Please try again',
          "is_success":False
      },
      status=status.HTTP_500_INTERNAL_SERVER_ERROR
      ) 
    
  return Response(
      {
          "message": "successfully deleted",
          "is_success": True
      })
  