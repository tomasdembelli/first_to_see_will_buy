from rest_framework import serializers
from .models import Ad, Message
from django.contrib.auth.models import User



class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    #messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = ('id','title',)
        #fields = ('__all__', 'username')


class AdDetailSerializer(AdSerializer):
    username = serializers.StringRelatedField(source='owner.username', read_only=True)    # without this, it only shows the primary key of the user
    messages = MessageSerializer(many=True, read_only=True)


    class Meta:
        model = Ad
        fields = ('id','title', 'username', 'description', 'price', 'pub_date', 'messages')
        #fields = ('__all__', 'username', 'messages')


class UserSerializer(serializers.ModelSerializer):
    #ads = serializers.PrimaryKeyRelatedField(many=True, queryset=Ad.objects.only('title'))
    ads = AdSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'ads')
        #fields = '__all__'
