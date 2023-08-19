from django.contrib.auth import get_user_model 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
import json
from .models import User,ChatRoom,ChatMessage

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):

        # create a room 
        self.room_name = self.scope['url_route']['kwargs']['other_user']
        self.room_group_name = 'chat_%s' %self.room_name



        # Add the user's unique channel to the group(same as chatroom): group_add requires 2 args- group name, channel name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name

        )

        
        # Accept the websocket connection (Here await means:Execute and wait for it to finish)
        await self.send({
            'type':'websocket.accept'
        })


       
    # Receive messages from websocket
    async def websocket_receive(self,event):

        received_data=event.get('text',None)
        received_data=json.loads(received_data)

        message = received_data['message']
        sent_by = received_data['sentBy']
        room_id = received_data['roomId']

        # Save new message
        new = await self.create_new_message(room_id=room_id, message=message, sent_by=sent_by)
        

        # Send message to the room_group(common): syntax= whom to send, what to send
        if message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat.message',
                    'message':message,
                    'sent_by':sent_by
                }

            )


        
    # Receive messages from room_group (includes the user who sent the message and all others whose channel is added in that group)
    async def chat_message(self,event):
        print('message',event)

        response={
            "sent_by":event['sent_by'],
            "message":event['message']
        }

         # Send message to websocket
        await self.send({
            'type':'websocket.send',
            'text': json.dumps(response)
        })




    async def websocket_disconnect(self,event):
        print("disconnected",event)

        # Leave a room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )



    # Query Database
    @database_sync_to_async
    def get_chatroom_id(self,chatroomId):
        qs = ChatRoom.objects.get(pk=chatroomId)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    # Save new messages
    @database_sync_to_async
    def create_new_message(self,room_id,sent_by,message):
        
        chat_room = ChatRoom.objects.get(pk=room_id)
        sent_by_user = User.objects.get(username = sent_by)
        qs = ChatMessage(room = chat_room,user=sent_by_user,message = message)
        qs.save()




    
    
    