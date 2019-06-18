from rest_framework import serializers
from .models import Ad

class AdSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='owner.username')    # without this, it only shows the primary key of the user
    class Meta:
        model = Ad
        fields = ('id','title', 'username', 'description', 'price', 'pub_date')
        #fields = '__all__'