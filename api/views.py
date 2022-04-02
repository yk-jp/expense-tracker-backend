from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from core.models import User, Category, Transaction
from core.serializers import UserSerializer, CategorySerializer, TransactionSerializer

@api_view(['GET'])
def getData(request):
    all_transactions_current_month = Transaction.objects.all()

    serializer = TransactionSerializer(
        all_transactions_current_month, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def transaction_register(request):
    print(request.data)
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)