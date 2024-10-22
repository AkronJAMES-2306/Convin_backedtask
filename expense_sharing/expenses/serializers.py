# expenses/serializers.py
from rest_framework import serializers
from .models import User
from .models import Expense

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def validate(self, data):
        if data['split_method'] == 'percentage':
            total_percentage = sum([p['percentage'] for p in data['participants']])
            if total_percentage != 100:
                raise serializers.ValidationError("Percentages must add up to 100.")
        return data
