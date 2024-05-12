from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import News
from Users.verification import user_is_buster, user_valid


@user_is_buster
@user_valid
@login_required
def news_page(request,**kwargs):

    print(News.objects.get())
    return render(request, 'News_page.html',{**kwargs})