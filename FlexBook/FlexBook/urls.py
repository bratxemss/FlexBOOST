"""
URL configuration for FlexBook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from Users.views import logout_user,index_page, settings_page, profile_page,\
    history_page,ban,orders_page
from Users.business_logic import register_button,login_button,user_private_data_saver
from Games.views import games_page
from Games.business_logic import get_game_rank_by_game_id, buy_boost, accept_order
from News.views import news_page
from Messages.views import messenger_page
from Messages.business_logic import send_message

urlpatterns = [
    path('admin/', admin.site.urls, name='admin_page'),
    path('', index_page, name='index_page'),
    path('log_out', logout_user, name='logout_user'),
    path('register_button', register_button, name='register_button'),
    path('login_button',login_button,name='login_button'),
    path('profile', profile_page, name='profile_page'),
    path('settings', settings_page, name='settings_page'),
    path('games_page', games_page, name='games_page'),
    path('history_page', history_page, name='history_page'),
    path('messenger_page', messenger_page, name='messenger_page'),
    path('news_page', news_page, name='news_page'),
    path('user_data_save', user_private_data_saver, name='user_data_save'),
    path('ban', ban, name='ban_page'),
    path('orders_page',orders_page,name='orders_page'),
    path('game_ranks',get_game_rank_by_game_id,name='game_ranks'),
    path('buy-boost/', buy_boost, name='buy_boost'),
    path('accept_order/', accept_order, name='accept_order'),
    path('send_message/', send_message, name='send_message'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)