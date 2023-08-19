# Let's Chat



### Introduction

This is a chat application built using django’s third party library **Django Channels**.

Channels wraps Django’s native asynchronous view support, allowing Django projects to handle not only HTTP, but protocols that require long-running connections too - WebSockets, MQTT, chatbots, amateur radio, and more.

It does this while preserving Django’s synchronous and easy-to-use nature, allowing you to choose how you write your code - synchronous in a style like Django views, fully asynchronous, or a mixture of both. On top of this, it provides integrations with Django’s auth system, session system, and more, making it easier than ever to extend your HTTP-only project to other protocols.

---

### Installation

To setup a django project using channels the channel package has to be installed. This can be done using the following command:

```pip install channels```

After that add 'channels' to INSTALLED_APPS tuple in settings.py

--------------------------------------------------

### Django channels request cycle
Using Channels, now you will have two types of requests to handle, the http requests and the websocket requests.

When the request arrives from the client, it will pass through an Interface server, a server that understands the ASGI (Asynchronous Server Gateway Interface) protocol. It will redirect the request to an ASGI router, where it is checked : if it’s a http request, it is sent to its respective view, and if it is a websocket request, and it is sent to its consumer, which is very similar to a view.

In the following sections, we will see these components that integrate the new request cycle with Channels.

#### ASGI server
Nowadays the Django framework uses a WSGI (Web Server Gateway Interface), which is an interface for python applications to handle Http requests. But to work with asynchronous applications, we need to use another interface, which is ASGI (Asynchronous Server Gateway Interface), that can handle websocket requests as well.
You will have to use a server that uses this approach. Good for us that Andrew Goodwin, the creator of Channels, made as well a server called Daphne. To handle this protocol as well.

Daphne already comes with Channels, so you won’t need to install it.

---
### Integrating request cycle with channels
1.  A Channels routing configuration is an ASGI application that is similar to a Django URLconf, in that it tells Channels what code to run when an HTTP request is received by the Channels server. The following changes need to be made in <projectname>/asgi.py:

```mysite/asgi.py
  import os

  from channels.routing import ProtocolTypeRouter
  from django.core.asgi import get_asgi_application

  os.environ.setdefault('DJANGO_SETTINGS_MODULE,'mysite.settings')

  application = ProtocolTypeRouter({

    "http": get_asgi_application(),
    # Just HTTP for now. (We can add other protocols later.)

})
```



This root routing configuration specifies that when a connection is made to the Channels development server:

  - The ProtocolTypeRouter will first inspect the type of connection. If it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.

 - The AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user, similar to how Django’s AuthenticationMiddleware populates the request object of a view function with the currently authenticated user. Then the connection will be given to the URLRouter.
- The URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns.

2). It is also required to point to the channels at the root routing configuration. The following change has to be made in projectname/settings.py:


```ASGI_APPLICATION = 'mysite.asgi.application'```

   And that's it! with channels in the installed apps it will take control over the *runserver* command replacing standard Django development with Channels development server. It's time to create a few views and urls for our chat application.

 -----


# Overview 
Project-name : new
 app-name    : chat

Contents of chat-app -

- urls.py   :Includes all the url routings to render specific views. 

- views.py  : All of the views for our chat application is defined in this file. The following views have been created- 
    - Login_view: To log a user in

    - Logout_view: To log a user out
    - Register : Registers a new user.
    - index view: This is a default view that will be rendered as soon as a user logs in. A list of user's contacts is displayed. Double-clicking the user's name will take the user to a specific chatroom inorder to chat with that particular person
    - chatroom : This view will enable the user to chat to a specific person within a chat room. As soon as this view is enabled, a websocket connection is established to allow long-time communication between client and server.
    - search_contact : This view enables to search for a specific contact.
    - create_contact : This view enables the creation of new contacts.
    - error : Renders the error page.
    - Inaddition a search_contact view is defined for our API calls.  
 - models.py : The models are defined here. Our chat application requires 3 different models namely-
    - User : To create a user object.
    - ChatRoom : Enable the creation of a unique id between two persons that binds them together as required to create distinct and unique chatrooms.
     - ChatMessages : Used to store all the chat messages communicated among different users in different chatrooms.

- admin.py : All the models are registered here to enable the creation of objects through the admin panel.


- templates: All the html pages are kept within a single folder whose name resembles the app name.
- static : The scripts and css files are stored within a single folder whose name resembles the app name within this folder




---

### Creating a websocket

A websocket is a bidirectional, persistent communication channel between a client and a server initiated over HTTP. 

The client establishes a WebSocket connection through a process known as the WebSocket handshake. This process starts with the client sending a regular HTTP request to the server. An Upgrade header is included in this request which informs the server that the client wishes to establish a WebSocket connection.

- To open a websocket connection on the client side:
  `var socket=newWebSocket('ws://websocket.example.com'); `

**Note:** Websocket urls use ws scheme, for https it uses wss scheme.

- If the server supports the WebSocket protocol, it will agree to the upgrade and will communicate this through the Upgrade header in the response.

- Once the connection has been established, the open event will be fired on your WebSocket instance on the client side.
- Now that the handshake is complete the initial HTTP connection is replaced by a WebSocket connection that uses the same underlying TCP/IP connection. At this point, either party can start sending data.

#### Websocket events and actions:
- There are four main Web Socket API events. Each of the events are handled by implementing the functions like onopen, onmessage, onclose and onerror functions respectively :

1. **Open**   : Once the connection has been established between the client and the server, the open event is fired from Web Socket instance.
`socket.onopen=async function(e){
    console.log("socket was opened")`

2. **Message** : Message event happens usually when the server sends some data. Messages sent by the server to the client can include plain text messages, binary data or images. Whenever the data is sent, the onmessage function is fired.
`socket.onmessage=async function(e){
    console.log("hello")`

3. **Close** : Close event marks the end of the communication between server and the client. Closing the connection is possible with the help of onclose event.This can also happen due to poor connectivity.
`socket.onclose=async function(e){
    console.log("The websocket closed unexpectantly!")`

4. **Error** : Error marks for some mistake, which happens during the communication. 
`socket.onerror=async function(e){
    console.log('error',e)
}`


- There are two main Websocket actions-

1. **send()** : This action is usually preferred for some communication with the server, which includes sending messages, which includes text files, binary data or images.
```socket.send(data)```

2. **close ()** : This method stands for goodbye handshake. It terminates the connection completely and no data can be transferred until the connection is re-established. 
```socket.close();```
---
### Creating a consumer:
When Django accepts an HTTP request, it consults the root URLconf to lookup a view function, and then calls the view function to handle the request. Similarly, when Channels accepts a WebSocket connection, it consults the root routing configuration to lookup a consumer, and then calls various functions on the consumer to handle events from the connection.

Consumers are counterparts to django views.
A consumer is a subclass of either *channels.consumer.AsyncConsumer* or *channels.consumer.SyncConsumer*. For this project I have used channels.consumer.AsyncConsumer.


Channels maps WebSocket connections to a consumer class. A few methods are defined on the consumer class namely:

1.**websocket_connect:** 
As soon as a new client connects via a WebSocket this method receives a connection request.It is important to accept the connection request. If the connection request is not accepted the websocket will close immediately.

2.**websocket_receive:** Each message the client sends on the socket gets sent across the websocket_receive.These are just messages received from the browser; remember that channels are one-direction.The receive channel can echo the message back to the same websocket(same client).

3.**websocket_disconnect:** Finally, when the client disconnects, a message is sent to websocket_disconnect. When that happens, we’ll remove the client from the “room”.

We need to create a routing configuration for the chat app that has a route to the consumer. A new file called chat/routing.py is created and the websocket url patterns are included. An example of how routing.py might look like:

```
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('chat/<str:abc>', consumers.ChatConsumer.as_asgi()),
]
```

We call the as_asgi() classmethod in order to get an ASGI application that will instantiate an instance of our consumer for each user-connection.

#### Routing to consumers
Once our routing.py is created, we also need to point the root routing configuration to the chat/routing.py. This following change is made in asgi.py :
```
  application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
```




---
### Enable Channel layers
We need to have multiple instances of the same ChatConsumer be able to talk to each other. Channels provides a channel layer abstraction that enables this kind of communication between consumers.

A channel layer provides the following abstractions:
- A channel is a mailbox where messages can be sent to. Each channel has a name. Anyone who has the name of a channel can send a message to the channel.
- A group is a group of related channels. A group has a name. Anyone who has the name of a group can add/remove a channel to the group by name and send a message to all channels in the group. It is not possible to enumerate what channels are in a particular group.

**Note**: Every consumer instance has an automatically generated unique channel name, and so can be communicated with via a channel layer.



We will use a channel layer that uses Redis as its backing store. To start a Redis server on port 6379, run the following command:

```
 docker run -p 6379:6379 -d redis:5
```

We need to install channels_redis so that Channels knows how to interface with Redis. Run the following command:

```
python3 -m pip install channels_redis
```

Before we can use a channel layer, we must configure it. Edit the mysite/settings.py file and add a CHANNEL_LAYERS setting to the bottom. It should look like:

```
#mysite/settings.py
#Channels
ASGI_APPLICATION = 'mysite.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

#### Setting group-names and room-names 
In our chat application we want to have multiple instances of ChatConsumer in the same room communicate with each other. To do that we will have each ChatConsumer add its channel to a group whose name is based on the room name(The room name will be a unique id between two persons,taken from the url, that is generated by the model ChatRoom where the two persons are the members). group name allows us to associate all users within a chatroom. We will soon understand the use of group names in a bit. 


```
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(AsyncConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
```
- self.room_name and self.room_group_name enable the creation of a room name and a groupname
- group_add requires two positional arguments: group name and channelname and thus adds the particular channel to a group.
-self.accept() accepts a connection.

#### Broadcasting messages
The final task is to broadcast the message to every other user present in a particular chatroom. This is done with the help of groups as shown :


 ```
  #Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message3
            }
        )

    #Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
  ```







When a user posts a message, a JavaScript function will transmit the message over WebSocket to a ChatConsumer. The ChatConsumer will receive that message and forward it to the group corresponding to the room name. Every ChatConsumer in the same group (and thus in the same room) will then receive the message from the group and forward it over WebSocket back to JavaScript, where it will be appended to the chat log.

---


### Distinctiveness and Complexity:
Django is an already established framework in the market, but it is synchronous and nowadays with the high demand for real time applications, It could not be left behind. Django channels comes into play to solve this issue. Django channels makes our work easier when working with asynchronous requests. Django channels extend the built-in capacities of Django beyond HTTP by taking advantage of ASGI,spiritual successor to WSGI.

Django channels work in a similar way to Django and without disrupting Django's functionalities in any way and rather expands its reach.Channels provides, a fast point-to-point and broadcast messaging between application instances. This extended functionality has allowed me to create chat-applications with great ease thereby exploring various fundamental concepts such as difference between ASGI and WSGI, building consumers and corresponding routes, understanding websockets, enabling channel-layers, etc.









