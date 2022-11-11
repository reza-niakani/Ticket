from django.urls import path
from . import views

app_name='home'

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('register/',views.UserRegisterView.as_view(),name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
    path('profile/<int:user_id>/',views.ProfileView.as_view(),name='profile'),
    path('messages/',views.MessagesView.as_view(),name='messages'),
    path('chat/<int:ticket_id>/',views.ChatView.as_view(),name='chat'),
    path('answer/<int:ticket_id>/',views.AnswerView.as_view(),name='answer'),
]

