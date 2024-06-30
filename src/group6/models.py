from django.contrib.auth.models import User
from django.db import models


class FAQ(models.Model):
    text = models.TextField(max_length=64, null=False)
    parent = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True)

    def get_children(self):
        return list(self.faq_set.all())


class Chat(models.Model):
    pass


class UserChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField(max_length=64)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # Adding a timestamp for message ordering
