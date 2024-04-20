from django.contrib.auth import logout

from Games.business_logic import get_game_rank_by_game_id
from .verification import user_valid, user_is_buster
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from Users.user_services import get_current_user
from Users.models import CustomUser,GameOrder
from Games.models import Game


@login_required
def ban(request):
    user = request.user
    if user.banned:
        return render(request, 'For_banned.html')
    else:
        return redirect('index_page')


@user_is_buster
@user_valid
def index_page(request, **kwargs):
    """Redirecting user depending on authenticated"""
    if request.user.is_authenticated:
        user = CustomUser.objects.get(username=get_current_user(request)['user'])
        return render(request, 'Main_Page.html',{'user': user, **kwargs})
    else:
        return render(request, 'Main_Registration_Page.html')


@user_is_buster
@user_valid
@login_required
def settings_page(request,**kwargs):
    return render(request, 'Settings.html',{**kwargs})


@user_is_buster
@user_valid
@login_required
def profile_page(request,**kwargs):
    """Rendering and sending data to 'Profile.html' """
    user = CustomUser.objects.get(username=get_current_user(request)['user'])
    registration_data = user.registration_time.strftime("%Y-%m-%d")
    birth_day = user.birth_day.strftime("%Y-%m-%d")
    return render(request, 'Profile.html',{'username': user.username,'first_name':user.first_name,
                                           'second_name':user.second_name,'reg_data':registration_data,'age':user.age,
                                           'birth_day':birth_day,'banned':user.banned,'email':user.email,
                                           'admin':user.is_superuser,**kwargs})


@user_is_buster
@user_valid
@login_required
def history_page(request, **kwargs):
    return render(request, 'History_page.html',{**kwargs})


@user_is_buster
@user_valid
@login_required
def orders_page(request, **kwargs):
    orders = GameOrder.objects.all()
    return render(request, 'Orders_page.html',{"Orders":orders, **kwargs})


@user_valid
def logout_user(request):
    """Logout logic for user"""
    logout(request)
    return redirect('index_page')

