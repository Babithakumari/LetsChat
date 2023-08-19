from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import User,ChatMessage,ChatMessageManager,ChatRoom
from django.db import IntegrityError
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def index(request):
    my_contacts = ChatRoom.objects.filter(Q(first_person = request.user) | Q(second_person = request.user))
   
   
    return render(request, "chat/index.html",{
        'contacts':my_contacts
    })




def chatroom(request,room_name):
    previous_msg = ChatMessage.objects.filter(room=room_name).order_by("-timestamp")[:30]
    previous_msg= reversed(previous_msg)
    room_members = ChatRoom.objects.get(pk =  room_name )
    

   
    if room_members.first_person == request.user:
        other_user = room_members.second_person
    else:
        other_user = room_members.first_person




    return render(request,"chat/chatroom.html",{
        'room_name':room_name,
        'username':request.user,
        'previous_msg':previous_msg,
        'other_user':other_user
        
    })


def create_contact(request,person):
    current_user_obj=User.objects.get(username=request.user)
    person_obj=User.objects.get(username=person)
    new_room = ChatRoom(first_person = current_user_obj,second_person=person_obj)
    new_room.save()
    return JsonResponse({"status":"success"},status=200)




def search_contact(request,person):

    # Check if person exists
    try:
        person_obj = User.objects.get(username = person)
    except User.DoesNotExist:
        return JsonResponse({"status":"failure"},status=404)

        


    # Check if search person and current person are not same
    current_user_obj = User.objects.get(username = request.user)
    if person_obj==current_user_obj:
        return JsonResponse({"status":"failure"},status=404)

        


    #Check if chatroom exists
    chatroom_obj = ChatRoom.objects.filter(first_person__in=[person_obj,current_user_obj], second_person__in = [person_obj,current_user_obj])
    if chatroom_obj.exists():
        return JsonResponse({"status":"success"},status=200)

    else:
        return JsonResponse({"status":"pending"},status=404)

def error(request):
    return render(request, "chat/error.html")

def found(request,person):
    current_user_obj=User.objects.get(username=request.user)
    person_obj=User.objects.get(username=person)
    chatroom_obj = ChatRoom.objects.filter(first_person__in=[person_obj,current_user_obj], second_person__in = [person_obj,current_user_obj])
    return render(request,"chat/index.html",{
            "contacts":chatroom_obj
    })

           
def login_view(request):

    #Post
    if request.method == 'POST':
        #attempt to sign the user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)

        #check if authentication is successfull
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request,"chat/login.html",{
                "message":"Invalid username and/or password"
            })


    #Get method
    else:
        return render(request,"chat/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_view"))

def register(request):
    # Submit a form
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")

