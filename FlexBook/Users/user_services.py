from django.contrib.auth.decorators import login_required


@login_required
def get_current_user(request):
    user = request.user
    return {'user': user.username}

def get_timezone_from_ip(ip_address):
    from requests import get
    url = f"http://ip-api.com/json/{ip_address}"
    response = get(url)
    data = response.json()
    timezone = data.get('timezone', 'Europe/Tallinn')
    return timezone