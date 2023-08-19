from django.urls import path
from . import views

urlpatterns=[

    path("",views.index, name="index"),
    path("login", views.login_view, name="login_view"),
    path("register", views.register, name = "register"),
    path("logout", views.logout_view, name="logout_view"),
    path("error", views.error, name="error"),
    path("search_contact/<str:person>",views.search_contact, name = "search_contact"),
    path("create_contact/<str:person>",views.create_contact, name = "create_contact"),
    path("found/<str:person>",views.found, name = "found"),
    path("<int:room_name>", views.chatroom, name="chatroom"),

]


