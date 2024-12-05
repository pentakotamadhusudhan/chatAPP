from asgiref.sync import sync_to_async
import random
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
from django.db.models import Q
from .models import ChatModel
from .serializers import ChatPostSerializers


class ChatGetConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'counter_room'
        self.room_group_name = 'counter_group'
        self.to_user = self.scope.get('url_route', {}).get('kwargs', {}).get('to_user', None)
        self.from_user = self.scope.get('url_route', {}).get('kwargs', {}).get('from_user', None)

        print("from_user",self.from_user)
        print("to_user",self.to_user)
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the counter group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive a message from WebSocket (optional for incrementing or sending numbers)
    async def receive(self, text_data,to_user):
        self.toUserId  = to_user
        print("________ to user id :",self.toUserId)

        data = json.loads(text_data)
        action = data.get("message")
                

    # Receive message from the WebSocket group
    async def send_counter(self, event):
        queryset = await self.get_chat_data()
        await self.send(text_data=json.dumps({
                "data": queryset,
                "status": 200
            }))
    @sync_to_async
    def get_chat_data(self):
        queryset = ChatModel.objects.filter(Q(from_user=self.from_user, to_user=self.to_user) | Q(from_user=self.to_user, to_user=self.from_user))
        serializer = ChatPostSerializers(queryset, many=True)
        
        return serializer.data

        
        




class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'counter_room'
        self.room_group_name = 'counter_group'

        # Join the counter group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send a message to WebSocket indicating that the connection was established
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the counter group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive a message from WebSocket (optional for incrementing or sending numbers)
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "increment":
            # Logic for incrementing the counter
            counter = await self.get_counter()
            counter += 1
            await self.set_counter(counter)

            # Send updated counter to the WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_counter',
                    'counter': counter
                }
            )

    # Receive message from the WebSocket group
    async def send_counter(self, event):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        counter = f"{current_time}"
        # Send updated counter to WebSocket
        await self.send(text_data=json.dumps({
            'counter': counter
        }))

    async def get_counter(self):
        # You can implement persistent storage for the counter
        # For simplicity, using an in-memory counter:
        return 0  # Replace with actual counter retrieval logic (e.g., from a database or Redis)

    async def set_counter(self, counter):
        # You can implement persistent storage for the counter
        # For simplicity, we're not storing it, but this would be where you save the new counter value`~`
        pass    




class CounterConsumer(AsyncWebsocketConsumer):
    counter = 10
    async def connect(self):
        self.room_name = 'counter_room'
        self.room_group_name = 'counter_group'

        # Join the counter group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send a message to WebSocket indicating that the connection was established
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the counter group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive a message from WebSocket (optional for incrementing or sending numbers)
    async def receive(self, text_data):
       

        data = json.loads(text_data)
        action = data.get("action")
        if action == "minus":
            counter = await self.get_counter()
            counter  = 0
            await self.set_counter(counter)

            # Send updated counter to the WebSocket group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_counter',
                    'counter': counter
                }
            )
        else : 
            await self.send(text_data=json.dumps({
                'counter': self.counter
            }))           

    # Receive message from the WebSocket group
    async def send_counter(self, event):
        counter = random.randint(3, 1000)
        # Send updated counter to WebSocket
        await self.send(text_data=json.dumps({
            'counter': counter
        }))

    async def get_counter(self):
        # You can implement persistent storage for the counter
        # For simplicity, using an in-memory counter:
        return 0  # Replace with actual counter retrieval logic (e.g., from a database or Redis)

    async def set_counter(self, counter):
        # You can implement persistent storage for the counter
        # For simplicity, we're not storing it, but this would be where you save the new counter value`~`
        pass    
