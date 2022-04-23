from rest_framework import serializers
from .models import User, Category, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    ) 
    
    def create(self,validated_data):
        category = validated_data["category"]
        
        return Transaction.objects.create(**validated_data)
   
    class Meta:
        model = Transaction
        fields = '__all__'
