from django.db import models


def game_profile_picture_path(instance, filename):
    return f'game_pics/{instance.game_name}/{filename}'


def game_rank_picture_path(instance, filename):
    return f'game_pics/{instance.game.game_name}/ranks/{instance.order}/{filename}'


class Game(models.Model):
    game_name = models.CharField(
        max_length=50,
        default="None")
    game_img = models.ImageField(
        upload_to=game_profile_picture_path,
        default='D:\pythonProject\ProjectDjango\FlexBook\static\Server_images\sticker.webp',
        blank=True,
        null=True)

    def __str__(self):
        return f"\nGame: {self.game_name}"


class Rank(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rank_value = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    rank_img = models.ImageField(
        upload_to=game_rank_picture_path,
        default='D:\pythonProject\ProjectDjango\FlexBook\static\Server_images\sticker.webp',
        blank=True,
        null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.game} - {self.rank_value}"


class GameRankAssociation(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    from_rank = models.ForeignKey(Rank, related_name='from_rank', on_delete=models.CASCADE,default=0)
    to_rank = models.ForeignKey(Rank, related_name='to_rank', on_delete=models.CASCADE,default=0)

    def __str__(self):
        return f"{self.from_rank} to {self.to_rank}"
