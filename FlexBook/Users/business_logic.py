import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm,UserProfilePictureForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import CustomUser, Client
from datetime import datetime
from django.utils import timezone
from .verification import user_valid
from .user_services import get_timezone_from_ip


@user_valid
@login_required
@require_POST
def user_private_data_saver(request):
    """Getting data from POST request and updating user data in DB"""
    new_name = request.POST.get('new_name')
    new_email = request.POST.get('new_email')
    new_birthday = request.POST.get('new_birthday')

    picture_data = request.FILES.get('user_profile_picture')

    now = timezone.now()
    try:
        new_first_name = new_name.split(' ')[0]
        new_second_name = new_name.split(' ')[1]
    except IndexError:
        new_first_name = new_name
        new_second_name = ''

    new_birth_day = timezone.make_aware(datetime.strptime(new_birthday, "%Y-%m-%d"))

    # Обновляем данные профиля пользователя
    current_user, created = CustomUser.objects.update_or_create(
        username=request.user.username,
        defaults={
            'email': new_email if not CustomUser.objects.filter(email=new_email).first() else request.user.email,
            'first_name': new_first_name,
            'second_name': new_second_name,
            'birth_day': new_birth_day,
            'age': now.year - new_birth_day.year - ((now.month, now.day) < (new_birth_day.month, new_birth_day.day)),
            'user_profile_pictures':picture_data if picture_data else request.user.user_profile_pictures
        }
    )


    if created:
        messages.success(request, 'Your data has been successfully updated.')
    else:
        messages.success(request, 'Your data has been successfully created.')

    return redirect('profile_page')


@require_POST
def register_button(request):
    """Registration logic for registration button"""
    form_data = request.POST.copy()
    form_data['timezone'] = get_timezone_from_ip(request.META.get('REMOTE_ADDR'))
    form = CustomUserCreationForm(form_data)
    if form.is_valid():
        user = form.save()
        Client.objects.create(
            user=user,
            client_payment_data='None',
            trust_points=0,
            client_info='Client'
        )

        login(request, user)
        messages.success(request, 'Registration successful. You are now logged in.')
    else:
        messages.error(request, 'Registration failed. Please check the form.')
    return redirect('index_page')


@user_valid
@require_POST
def login_button(request):
    """Login logic for users"""
    email = request.POST.get("L_email")
    password = request.POST.get("L_password")
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        user = None
    if user is not None and check_password(password, user.password):
        try:
            user_client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            user_client = None
        if user_client is None:
            Client.objects.create(
                user=user,
                client_payment_data='None',
                trust_points=0,
                client_info='Client'
            )
        else:
            pass
        login(request, user)
        messages.success(request, 'Login successful.')
    else:
        messages.error(request, 'Login failed. Invalid email or password.')
    return redirect('index_page')


