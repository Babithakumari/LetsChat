from django.contrib.auth.models import AbstractUser

from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class User(AbstractUser):
    pass

class ChatRoom(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user1")
    second_person = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "user2")

    class Meta:
        unique_together = ['first_person','second_person']

    def ____str___(self):
        return self.id

class ChatMessageManager(models.Manager):
    def by_room(self,room):
        data_set = ChatMessage.objects.filter(room=room).order_by("-timestamp")

class ChatMessage(models.Model):
    """
    Messages sent by each user to a specific chatroom
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "sender")
    room = models.ForeignKey(ChatRoom, on_delete = models.CASCADE)
    message = models.TextField(unique=False,blank = False,default = "")
    timestamp = models.DateTimeField(auto_now_add=True)    

    objects = ChatMessageManager()

    def ____str___(self):
        return self.message
