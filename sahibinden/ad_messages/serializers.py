from rest_framework import serializers
from .models import Ad
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    ads = serializers.PrimaryKeyRelatedField(many=True, queryset=Ad.objects.only('title'))

    class Meta:
        model = User
        fields = ('id', 'username', 'ads')


class AdSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='owner.username')    # without this, it only shows the primary key of the user

    class Meta:
        model = Ad
        fields = ('id','title', 'username', 'description', 'price', 'pub_date')
        #fields = '__all__'