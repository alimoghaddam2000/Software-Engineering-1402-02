from rest_framework import serializers
from .models import FAQ, Chat, UserChat, Message


class FAQSerializer(serializers.ModelSerializer):
    is_leaf = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'text', 'parent', 'is_leaf']

    def get_is_leaf(self, obj):
        return obj.get_children() == []


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id']


class UserChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChat
        fields = ['id', 'user', 'chat']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()  # To get a string representation of the user

    class Meta:
        model = Message
        fields = ['id', 'chat', 'text', 'sender', 'timestamp']
