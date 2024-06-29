from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FAQ, Chat, UserChat, Message
from .serializers import FAQSerializer, ChatSerializer, MessageSerializer


class FAQChildrenView(APIView):
    def get(self, request, parent_id):
        try:
            parent_node = FAQ.objects.get(pk=parent_id)
        except FAQ.DoesNotExist:
            return Response({'error': 'FAQ node not found'}, status=status.HTTP_404_NOT_FOUND)

        children = parent_node.get_children()
        serializer = FAQSerializer(children, many=True)
        return Response(serializer.data)


class FAQRootsView(APIView):
    def get(self, request):
        root_faqs = FAQ.objects.filter(parent__isnull=True)
        serializer = FAQSerializer(root_faqs, many=True)
        return Response(serializer.data)


class CreateChatView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Find an available support user
        support_user = self.get_available_support_user()
        if not support_user:
            return Response({'error': 'No available support users'}, status=status.HTTP_404_NOT_FOUND)

        # Create a new chat
        chat = Chat.objects.create()

        # Add both users to the chat
        UserChat.objects.create(user=user, chat=chat)
        UserChat.objects.create(user=support_user, chat=chat)

        return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)

    def get_available_support_user(self):
        # Example implementation: Find a support user with the least active chats
        support_users = User.objects.filter(groups__name='Support')  # Assuming support users are in the 'Support' group
        count_dict = UserChat.objects.filter(user__in=support_users).values('user').annotate(
            num_chats=Count('id')).order_by('num_chats')

        if not count_dict:
            return support_users[0]

        return support_users.filter(id=count_dict[0]['user']).first() if count_dict else None


class SendMessageView(APIView):
    def post(self, request):
        chat_id = request.data.get('chat_id')
        text = request.data.get('text')
        sender_id = request.data.get('sender_id')

        if not all([chat_id, text, sender_id]):
            return Response({'error': 'Chat ID, text, and sender ID are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return Response({'error': 'Sender not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the sender is part of the chat
        if not UserChat.objects.filter(chat=chat, user=sender).exists():
            return Response({'error': 'User is not a participant in the chat'}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(chat=chat, text=text, sender=sender)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class GetMessagesView(APIView):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(chat=chat).order_by('timestamp')
        return Response(MessageSerializer(messages, many=True).data, status=status.HTTP_200_OK)
