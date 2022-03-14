from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import UserSerializer, CategorySerializer, TransactionSerializer


@api_view(['GET'])
def getData(request):
    all_transactions_current_month = Transaction.objects.all()

    serializer = TransactionSerializer(all_transactions_current_month, many=True)

    return Response(serializer.data)

# @api_view(['POST'])
# def postData(request):

#     return Response()
