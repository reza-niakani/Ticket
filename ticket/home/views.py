from django.shortcuts import render, redirect, get_object_or_404
from .froms import UserLoginForm, UserRegisterForm, TiketForm, AnswerMessageForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Ticket


# only for login user and Display the login form
class HomeView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, 'home/home.html', {'form': form})


class UserRegisterView(View):
    form_class = UserRegisterForm
    templates_class = 'home/register.html'

    # Disable registration for users who have already registered
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'your are logged in and you cant do this')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    # Display UserRegisterForm for registration
    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, {'form': form})

    # Save the input information in the user model to create a new user account
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'your account is successfuly created', 'success')
            return redirect('home:home')
        return render(request, self.templates_class, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    templates_name = 'home/home.html'

    # To avoid frequent connection to the database and connect to the database only when needed
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    # Disable login for users who have already logined
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'your are logged in befor')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    # Display UserLoginForm for Login
    def get(self, request):
        form = self.form_class
        return render(request, self.templates_name, {'form': form})

    # Checking user input information and user login if correct
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'your successfuly loged in', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:profile', request.user.id)
            messages.error(request, 'your password or username isnot correct', 'danger')
        return render(request, self.templates_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'your logout is successfuly done', 'success')
        return redirect('home:home')


class ProfileView(LoginRequiredMixin, View):
    """
        Checking the type of user (admin and normal user)
         and if it is an admin,
         all users' messages will be displayed,
          and if it is a normal user,
           it will display the user's own messages.
    """

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        if request.user.is_superuser:
            uticket = Ticket.objects.all()
            messages.success(request, 'hello you are admin, welcome to your profile', 'success')
        else:
            uticket = user.uticket.filter(user=user)
            messages.success(request, 'hello you are user,welcome to you are profile', 'success')
        return render(request, 'home/profile.html', {'uticket': uticket})


class MessagesView(LoginRequiredMixin, View):
    form_class = TiketForm

    # Display TiketForm for create message
    def get(self, request):
        form = self.form_class
        return render(request, 'home/message.html', {'form': form})

    # Save the input information in the Ticket model to create a new message
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.superuser = request.user
            new_message.title = cd['title']
            new_message.body = cd['body']
            new_message.save()
            messages.success(request, 'your messages is successfuly sended wait for your answer', 'success')
            return redirect('home:profile', request.user.id)
        return render(request, 'home/message.html', {'form': form})


class ChatView(LoginRequiredMixin, View):

    # For user that be admin to close the chat and end that message
    def setup(self, request, *args, **kwargs):
        self.ticket_instance = get_object_or_404(Ticket, pk=kwargs['ticket_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        Ticket_answer = self.ticket_instance.Tanswer.filter(is_answer=False)
        close = False
        if request.user.is_superuser:
            close = True
        return render(request, 'home/chat.html',
                      {'ticket': self.ticket_instance, 'Ticket_answer': Ticket_answer, 'close': close})


class AnswerView(LoginRequiredMixin, View):
    form_class = AnswerMessageForm

    # Calling the desired message using ticket ID
    def setup(self, request, *args, **kwargs):
        self.ticket_instance = get_object_or_404(Ticket, pk=kwargs['ticket_id'])
        return super().setup(request, *args, **kwargs)

    # Display AnswerMessageForm for answer to  desired message
    def get(self, request, *args, **kwargs):
        return render(request, 'home/answer.html', {'form': self.form_class})

    # Save the input answer in the Ticket model to create a new message after check the user is logged in
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.ticket = self.ticket_instance
            answer.save()
            messages.success(request, 'your answer is successfully submit', 'success')
            return redirect('home:chat', self.ticket_instance.id)
