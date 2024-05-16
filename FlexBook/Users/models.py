from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator,MinValueValidator
from djmoney.models.fields import MoneyField
from timezone_field import TimeZoneField
from Games.models import Game,GameRankAssociation
from FlexBook.settings import DEFAULT_IMAGE

def user_profile_picture_path(instance, filename):
    return f'profile_pics/{instance.username}/{filename}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=50,default="None")
    second_name = models.CharField(max_length=50,default="None")
    registration_time = models.DateTimeField(default=timezone.now)
    birth_day = models.DateTimeField(default=timezone.now)
    age = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)
    user_profile_pictures = models.ImageField(upload_to=user_profile_picture_path,
                                               default=DEFAULT_IMAGE)
    timezone = TimeZoneField(default='UTC')

    def __str__(self):
        return f"{self.username, self.email}"


class Client(models.Model):
    CLIENT = 'Client'
    BOOSTER = 'Booster'
    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (BOOSTER, 'Booster'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    client_payment_data = models.CharField(max_length=150, default="None")
    trust_points = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    games = models.ManyToManyField(Game, blank=True)
    client_info = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)

    def __str__(self):
        return f"{self.user}"


class Payment(models.Model):
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR')
    payment_date = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    client = models.ForeignKey(Client, related_name='client_orders', on_delete=models.CASCADE)
    booster = models.ForeignKey(Client, related_name='booster_orders', on_delete=models.CASCADE)
    order_data = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50,default="Pending")
    order_payment_data = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return f"ORDER DATA \n" \
                f"CLIENT:{self.client}\n BOOSTER:{self.booster}\n" \
                f"DATA: {self.order_data}\n" \
                f"ORDER STATUS: {self.order_status}\n" \
               f"PAYMENT DATA:{self. order_payment_data}"


class GameOrder(models.Model):
    client = models.ForeignKey(Client, related_name='game_client_orders', on_delete=models.CASCADE)
    order_data = models.DateTimeField(default=timezone.now)
    GameRankAssociation = models.ForeignKey(GameRankAssociation, on_delete=models.CASCADE, null=True)
    order_status = models.CharField(max_length=50, default="Pending")
    order_payment_value = MoneyField(max_digits=10, decimal_places=2, default_currency='EUR', default=0)
    order_payment_description = models.CharField(max_length=299, default="None")

    def __str__(self):
        return f"{self.client}, Data:{self.order_data},{self.GameRankAssociation}"
