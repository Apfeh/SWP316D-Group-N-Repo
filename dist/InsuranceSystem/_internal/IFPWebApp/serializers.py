from rest_framework import serializers
from .models import InsuredPerson

class InsuredPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuredPerson
        fields = '__all__'
        