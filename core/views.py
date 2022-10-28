from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache


@api_view(['GET'])
def cache_clear(request):
    cache.clear() 
    
    return Response({
          "result": {
              "message": "cache is cleared"
          },
          "is_success": True
    })
