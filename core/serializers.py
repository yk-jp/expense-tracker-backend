from rest_framework import serializers
from .models import User, Category, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    def create_validation(self):
        new_data = self.data
        
        if Category.objects.filter(user=new_data["user"], name=new_data["name"],category_type=new_data["category_type"]).exists():
            raise serializers.ValidationError('{name} already exists in the {category_type} event. Try different name'.format(**new_data))
        
        return True
    
    def update_validation(self, id):
        new_data = self.data
        
        if Category.objects.filter(user=new_data["user"], name=new_data["name"],category_type=new_data["category_type"]).exclude(pk=id).exists():
            raise serializers.ValidationError('{name} already exists in the {category_type} event. Try different name'.format(**new_data))
        
        return True
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
     
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
        return Transaction.objects.create(**validated_data)
   
    class Meta:
        model = Transaction
        fields = '__all__'
