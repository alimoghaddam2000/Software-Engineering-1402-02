from django.urls import path

from .views import FAQChildrenView, FAQRootsView, CreateChatView, SendMessageView, GetMessagesView

urlpatterns = [
    path('faq/<int:parent_id>/children/', FAQChildrenView.as_view(), name='faq-children'),
    path('faq/roots/', FAQRootsView.as_view(), name='faq-roots'),
    path('create-chat/', CreateChatView.as_view(), name='create-chat'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('get-messages/<int:chat_id>/', GetMessagesView.as_view(), name='get-messages'),
]
